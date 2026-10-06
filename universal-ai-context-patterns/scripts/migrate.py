#!/usr/bin/env python3
"""
migrate.py — Migrate per-project ICM data to universal memory.

Usage:
    python migrate.py                        # Migrate all projects found under HOME
    python migrate.py --project /path/to/p  # Migrate a single project
    python migrate.py --dry-run             # Preview without writing

Reads from:  <project>/.universal-mwp/icm/preference-signals.json
             <project>/.universal-mwp/icm/preference-rules.yaml
             <project>/.universal-mwp/icm/decision-log.md
Writes to:   ~/.ai-context/memory/icm/preferences.db

After successful migration, renames source files to *.migrated so they
are not re-processed. Does not delete them.
"""

import argparse
import json
import re
import sqlite3
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml

DB_PATH = Path.home() / ".ai-context" / "memory" / "icm" / "preferences.db"
LEGACY_DIR = Path.home() / ".ai-context" / "memory" / "icm" / "legacy"
MWP_FOLDER = ".universal-mwp"
SIGNALS_FILE = "icm/preference-signals.json"
RULES_FILE = "icm/preference-rules.yaml"
DECISIONS_FILE = "icm/decision-log.md"

# Known signal_type → action mappings
SIGNAL_TYPE_MAP = {
    "approval_granted": "approved",
    "implicit_accept": "approved",
    "rejection": "denied",
    "correction": "denied",
    "correction_persistent": "denied",
    "guardrail": "denied",
    "process_improvement": "deferred",
}

# Keywords that reliably indicate auto_approve
APPROVE_KEYWORDS = {"auto", "approve", "proceed", "skip", "allow"}
# Keywords that reliably indicate auto_deny
DENY_KEYWORDS = {"deny", "reject", "block"}
# "never" alone is ambiguous — only deny if paired with an action word
DENY_STRONG = {"never do", "never apply", "never use", "never run"}


def check_dependencies():
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("ERROR: PyYAML is required.")
        print("Install it with: pip install pyyaml")
        raise SystemExit(1)


def find_projects(root: Path) -> list[Path]:
    """Find all .universal-mwp folders with icm data under root."""
    return [p.parent for p in root.rglob(f"{MWP_FOLDER}/icm/preference-signals.json")]


def migrate_signals(
    conn: sqlite3.Connection,
    project_path: Path,
    dry_run: bool
) -> dict:
    """Returns stats dict with read/insert/duplicate/unmapped counts."""
    signals_path = project_path / MWP_FOLDER / SIGNALS_FILE
    if not signals_path.exists():
        return {"read": 0, "insert": 0, "duplicate": 0, "unmapped": 0, "unmapped_types": []}

    with open(signals_path, encoding="utf-8") as f:
        data = json.load(f)

    # Handle both formats: bare list [] or {"signals": [...]}
    signals = data if isinstance(data, list) else data.get("signals", [])

    stats = {"read": len(signals), "insert": 0, "duplicate": 0,
             "unmapped": 0, "unmapped_types": [], "migrated_ids": set()}

    if not signals:
        return stats

    project_name = project_path.name
    inserted_ids = set()

    for count, sig in enumerate(signals):
        sig_id = sig.get("id", "")
        task_label = sig.get("task", "")
        signal_type = sig.get("signal_type", "")

        # Fix #2: unique task_id — prefer sig id, compose with label+count to avoid collisions
        task_id = sig_id or (f"{task_label}:{count}" if task_label else f"migrated-{count}")

        action, unmapped = _map_signal_type_to_action(signal_type)
        if unmapped:
            stats["unmapped"] += 1
            if signal_type not in stats["unmapped_types"]:
                stats["unmapped_types"].append(signal_type)

        context_json = json.dumps({
            "observation": sig.get("observation", ""),
            "signal_type": signal_type,
            "task_label": task_label,
            "dimensions": sig.get("dimensions", {}),
            "migrated_id": sig_id,
            "unmapped_signal_type": signal_type if unmapped else None,
        })

        task_type = sig.get("dimensions", {}).get("task_type", "unknown")
        risk_level = sig.get("dimensions", {}).get("risk_assigned", "unknown")
        created_at = sig.get("date", datetime.now(timezone.utc).date().isoformat())

        # Fix #7: dry-run detects duplicates explicitly
        if dry_run:
            if task_id in inserted_ids:
                stats["duplicate"] += 1
            else:
                inserted_ids.add(task_id)
                stats["insert"] += 1
                if sig_id:
                    stats["migrated_ids"].add(sig_id)
        else:
            try:
                conn.execute("""
                    INSERT INTO signals
                    (project_path, project_name, task_id, task_type, risk_level,
                     action, confidence, context_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(project_path), project_name, task_id,
                    task_type, risk_level, action,
                    1.0, context_json, created_at
                ))
                stats["insert"] += 1
                if sig_id:
                    stats["migrated_ids"].add(sig_id)
            except sqlite3.IntegrityError:
                stats["duplicate"] += 1

    return stats


def migrate_rules(
    conn: sqlite3.Connection,
    project_path: Path,
    dry_run: bool,
    migrated_signal_ids: set = None
) -> dict:
    """Returns stats dict with read/insert/duplicate counts."""
    rules_path = project_path / MWP_FOLDER / RULES_FILE
    if not rules_path.exists():
        return {"read": 0, "insert": 0, "duplicate": 0}

    with open(rules_path, encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or []

    # Fix #1: handle mapping {"version": "1.0", "rules": [...]} or bare list
    if isinstance(loaded, dict):
        rules = loaded.get("rules", [])
    else:
        rules = loaded

    if not isinstance(rules, list):
        rules = []

    stats = {"read": len(rules), "insert": 0, "duplicate": 0}

    if not rules:
        return stats

    project_pattern = str(project_path)

    for count, rule in enumerate(rules):
        rule_id = rule.get("id", f"migrated-rule-{count}")
        prefer = rule.get("prefer", "")
        notes = rule.get("notes", "")

        when = rule.get("when", {})
        if isinstance(when, str):
            when = {"situation": when}

        # Fix #5: preserve prefer + notes verbatim in condition_json
        # so no instruction text is lost regardless of derived action
        condition = json.dumps({
            "situation": when.get("situation", ""),
            **{k: v for k, v in when.items() if k != "situation"},
            "prefer": prefer,
            "notes": notes,
        })

        action, low_confidence = _map_prefer_to_action(prefer)
        confidence = float(rule.get("confidence", 0.8))
        based_on = rule.get("based_on", [])

        # Fix #8: validate based_on against migrated signal IDs
        if migrated_signal_ids and based_on:
            resolved = [sid for sid in based_on if sid in migrated_signal_ids]
            dangling = [sid for sid in based_on if sid not in migrated_signal_ids]
            if dangling:
                print(f"  WARNING: rule '{rule_id}' references unknown signal(s): "
                      f"{dangling} — signal_count capped to resolved citations")
            signal_count = max(1, len(resolved))
        else:
            signal_count = max(1, len(based_on)) if based_on else 1

        # Fix #5: if mapping confidence is low, flag rule for human review
        pending_review = 1 if low_confidence else 0

        if dry_run:
            stats["insert"] += 1
        else:
            try:
                conn.execute("""
                    INSERT INTO rules
                    (rule_id, project_pattern, condition_json, action,
                     confidence, signal_count, pending_review)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule_id, project_pattern, condition,
                    action, confidence, signal_count, pending_review
                ))
                stats["insert"] += 1
            except sqlite3.IntegrityError:
                stats["duplicate"] += 1

    return stats


def migrate_decision_log(
    conn: sqlite3.Connection,
    project_path: Path,
    dry_run: bool
) -> int:
    """Fix #3: migrate decision-log.md entries into decisions table."""
    log_path = project_path / MWP_FOLDER / DECISIONS_FILE
    if not log_path.exists():
        return 0

    content = log_path.read_text(encoding="utf-8")
    project_name = project_path.name
    count = 0

    blocks = re.split(r'\n(?=## \d{4}-\d{2}-\d{2})', content.strip())

    parsed_any = False
    for block in blocks:
        date_match = re.match(r'## (\d{4}-\d{2}-\d{2})\s*[—-]\s*(.+)', block)
        if not date_match:
            continue

        created_at = date_match.group(1)
        task_id = date_match.group(2).strip()

        decision_match = re.search(r'[-*]\s*Decision:\s*(.+)', block)
        basis_match = re.search(r'[-*]\s*Basis:\s*(.+)', block)

        decision = decision_match.group(1).strip() if decision_match else "unknown"
        reasoning = basis_match.group(1).strip() if basis_match else None

        rule_id = None
        if reasoning:
            rule_match = re.search(r'(rule-[\w-]+)', reasoning)
            if rule_match:
                rule_id = rule_match.group(1)

        if not dry_run:
            try:
                conn.execute("""
                    INSERT INTO decisions
                    (project_path, task_id, rule_id, decision, reasoning, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (str(project_path), task_id, rule_id, decision, reasoning, created_at))
                count += 1
                parsed_any = True
            except sqlite3.IntegrityError:
                pass
        else:
            count += 1
            parsed_any = True

    # Fallback: nothing parsed, insert summary row and preserve file
    if not parsed_any and not dry_run:
        conn.execute("""
            INSERT OR IGNORE INTO decisions
            (project_path, task_id, rule_id, decision, reasoning)
            VALUES (?, ?, NULL, ?, ?)
        """, (
            str(project_path),
            f"legacy-log-{project_name}",
            "legacy",
            f"Legacy decision-log.md carried over from {project_name}. "
            f"Original preserved at legacy/{project_name}-decision-log.md"
        ))
        count = 1

    if not dry_run:
        LEGACY_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(log_path, LEGACY_DIR / f"{project_name}-decision-log.md")
        log_path.rename(log_path.with_suffix(".md.migrated"))

    return count


def _map_signal_type_to_action(signal_type: str) -> tuple[str, bool]:
    """Returns (action, was_unmapped). Defaults to 'deferred' not 'approved'."""
    if signal_type in SIGNAL_TYPE_MAP:
        return SIGNAL_TYPE_MAP[signal_type], False
    return "deferred", True


def _map_prefer_to_action(prefer: str) -> tuple[str, bool]:
    """
    Fix #5: best-effort keyword hint only.
    Returns (action, low_confidence).
    low_confidence=True means the rule should be flagged pending_review.
    """
    p = prefer.lower()

    # Strong deny phrases first (before checking individual keywords)
    if any(phrase in p for phrase in DENY_STRONG):
        return "auto_deny", False

    words = set(re.findall(r'\w+', p))

    if words & APPROVE_KEYWORDS:
        return "auto_approve", False

    if words & DENY_KEYWORDS:
        return "auto_deny", False

    # No clear keyword — default require_approval and flag for review
    return "require_approval", True


def run(project: Path = None, dry_run: bool = False):
    check_dependencies()

    if not DB_PATH.exists():
        print("Universal memory DB not found. Run install/INSTALL.md first.")
        return

    projects = [project] if project else find_projects(Path.home())

    if not projects:
        print("No projects with per-project ICM data found.")
        return

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{prefix}Found {len(projects)} project(s) to migrate.\n")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    total = {"signals_read": 0, "signals_insert": 0, "signals_dup": 0,
             "rules_read": 0, "rules_insert": 0, "rules_dup": 0,
             "decisions": 0, "unmapped": 0}

    try:
        for p in projects:
            # Fix #6: commit per-project, rename only after commit succeeds
            try:
                sig_stats = migrate_signals(conn, p, dry_run)
                rule_stats = migrate_rules(conn, p, dry_run,
                                           migrated_signal_ids=sig_stats.get("migrated_ids", set()))
                decisions = migrate_decision_log(conn, p, dry_run)

                if not dry_run:
                    conn.commit()

                if any([sig_stats["read"], rule_stats["read"], decisions]):
                    print(f"  {p.name}")
                    print(f"    signals:   {sig_stats['read']} read, "
                          f"{sig_stats['insert']} would insert, "
                          f"{sig_stats['duplicate']} would be dropped (duplicate task_id)"
                          if dry_run else
                          f"    signals:   {sig_stats['insert']} migrated, "
                          f"{sig_stats['duplicate']} skipped")
                    if sig_stats["unmapped"]:
                        for ut in sig_stats["unmapped_types"]:
                            print(f"    unmapped signal_type: {ut} "
                                  f"({sig_stats['unmapped_types'].count(ut)})")
                    print(f"    rules:     {rule_stats['read']} read, "
                          f"{rule_stats['insert']} would insert"
                          if dry_run else
                          f"    rules:     {rule_stats['insert']} migrated, "
                          f"{rule_stats['duplicate']} skipped")
                    print(f"    decisions: {decisions}")

                total["signals_read"] += sig_stats["read"]
                total["signals_insert"] += sig_stats["insert"]
                total["signals_dup"] += sig_stats["duplicate"]
                total["rules_read"] += rule_stats["read"]
                total["rules_insert"] += rule_stats["insert"]
                total["rules_dup"] += rule_stats["duplicate"]
                total["decisions"] += decisions
                total["unmapped"] += sig_stats["unmapped"]

            except Exception as e:
                conn.rollback()
                print(f"  ERROR migrating {p.name}: {e} — skipping, no data written")

        print(f"\n{prefix}Migration complete:")
        if dry_run:
            print(f"  signals:   {total['signals_read']} read, "
                  f"{total['signals_insert']} would insert, "
                  f"{total['signals_dup']} would be dropped (duplicate task_id)")
            print(f"  rules:     {total['rules_read']} read, "
                  f"{total['rules_insert']} would insert")
        else:
            print(f"  signals:   {total['signals_insert']} migrated "
                  f"({total['signals_dup']} skipped)")
            print(f"  rules:     {total['rules_insert']} migrated "
                  f"({total['rules_dup']} skipped)")
        print(f"  decisions: {total['decisions']} migrated")
        if total["unmapped"]:
            print(f"  WARNING:   {total['unmapped']} signals had unknown signal_type "
                  f"→ defaulted to 'deferred'")

        if not dry_run:
            print(f"\n  Source files renamed to *.migrated (not deleted).")
            print(f"  Decision logs preserved under {LEGACY_DIR}/")

    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate per-project ICM data to universal memory.")
    parser.add_argument("--project", type=Path, help="Migrate a single project path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    run(project=args.project, dry_run=args.dry_run)

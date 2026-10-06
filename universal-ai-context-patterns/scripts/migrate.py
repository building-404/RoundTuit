#!/usr/bin/env python3
"""
migrate.py — Migrate per-project ICM data to universal memory.

Usage:
    python migrate.py                        # Migrate all projects found under HOME
    python migrate.py --project /path/to/p  # Migrate a single project
    python migrate.py --dry-run             # Preview without writing

Reads from:  <project>/.universal-mwp/icm/preference-signals.json
             <project>/.universal-mwp/icm/preference-rules.yaml
Writes to:   ~/.ai-context/memory/icm/preferences.db

After successful migration, renames source files to *.migrated so they
are not re-processed. Does not delete them.
"""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import yaml

DB_PATH = Path.home() / ".ai-context" / "memory" / "icm" / "preferences.db"
MWP_FOLDER = ".universal-mwp"
SIGNALS_FILE = "icm/preference-signals.json"
RULES_FILE = "icm/preference-rules.yaml"


def check_dependencies():
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("ERROR: PyYAML is required.")
        print("Install it with: pip install pyyaml")
        raise SystemExit(1)


def find_projects(root: Path) -> list[Path]:
    """Find all .universal-mwp folders under root."""
    return [p.parent for p in root.rglob(f"{MWP_FOLDER}/icm/preference-signals.json")]


def migrate_signals(
    conn: sqlite3.Connection,
    project_path: Path,
    dry_run: bool
) -> int:
    signals_path = project_path / MWP_FOLDER / SIGNALS_FILE
    if not signals_path.exists():
        return 0

    with open(signals_path) as f:
        data = json.load(f)

    # Handle both formats: bare list [] or {"signals": [...]}
    if isinstance(data, list):
        signals = data
    else:
        signals = data.get("signals", [])
    if not signals:
        return 0

    project_name = project_path.name
    count = 0

    for sig in signals:
        context_json = json.dumps({
            "observation": sig.get("observation", ""),
            "signal_type": sig.get("signal_type", ""),
            "dimensions": sig.get("dimensions", {}),
            "migrated_id": sig.get("id", "")
        })

        task_type = sig.get("dimensions", {}).get("task_type", "unknown")
        risk_level = sig.get("dimensions", {}).get("risk_assigned", "unknown")
        action = _map_signal_type_to_action(sig.get("signal_type", ""))
        created_at = sig.get("date", datetime.now(timezone.utc).date().isoformat())

        if not dry_run:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO signals
                    (project_path, project_name, task_id, task_type, risk_level,
                     action, confidence, context_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(project_path), project_name,
                    sig.get("task", sig.get("id", f"migrated-{count}")),
                    task_type, risk_level, action,
                    1.0, context_json, created_at
                ))
                count += 1
            except sqlite3.IntegrityError:
                pass  # Already migrated
        else:
            count += 1

    if not dry_run and count > 0:
        signals_path.rename(signals_path.with_suffix(".json.migrated"))

    return count


def migrate_rules(
    conn: sqlite3.Connection,
    project_path: Path,
    dry_run: bool
) -> int:
    rules_path = project_path / MWP_FOLDER / RULES_FILE
    if not rules_path.exists():
        return 0

    with open(rules_path) as f:
        rules = yaml.safe_load(f) or []

    if not rules:
        return 0

    count = 0
    project_pattern = str(project_path)

    for rule in rules:
        rule_id = rule.get("id", f"migrated-rule-{count}")
        condition = json.dumps({
            "situation": rule.get("when", {}).get("situation", ""),
            **{k: v for k, v in rule.get("when", {}).items() if k != "situation"}
        })
        action = _map_prefer_to_action(rule.get("prefer", ""))
        confidence = float(rule.get("confidence", 0.8))
        based_on = rule.get("based_on", [])
        signal_count = len(based_on) if based_on else 1

        if not dry_run:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO rules
                    (rule_id, project_pattern, condition_json, action,
                     confidence, signal_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    rule_id, project_pattern, condition,
                    action, confidence, signal_count
                ))
                count += 1
            except sqlite3.IntegrityError:
                pass  # Already migrated
        else:
            count += 1

    if not dry_run and count > 0:
        rules_path.rename(rules_path.with_suffix(".yaml.migrated"))

    return count


def _map_signal_type_to_action(signal_type: str) -> str:
    mapping = {
        "approval_granted": "approved",
        "implicit_accept": "approved",
        "rejection": "denied",
        "correction": "denied",
        "correction_persistent": "denied",
        "guardrail": "denied",
    }
    return mapping.get(signal_type, "approved")


def _map_prefer_to_action(prefer: str) -> str:
    prefer_lower = prefer.lower()
    if any(w in prefer_lower for w in ["auto", "approve", "proceed", "skip"]):
        return "auto_approve"
    if any(w in prefer_lower for w in ["deny", "reject", "block", "never"]):
        return "auto_deny"
    return "require_approval"


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

    total_signals = 0
    total_rules = 0

    try:
        for p in projects:
            signals = migrate_signals(conn, p, dry_run)
            rules = migrate_rules(conn, p, dry_run)

            if signals or rules:
                print(f"  {p.name}")
                print(f"    signals: {signals}")
                print(f"    rules:   {rules}")
                total_signals += signals
                total_rules += rules

        if not dry_run:
            conn.commit()

        print(f"\n{prefix}Migration complete:")
        print(f"  {total_signals} signals migrated")
        print(f"  {total_rules} rules migrated")

        if not dry_run:
            print("\n  Source files renamed to *.migrated (not deleted).")
            print("  Remove them manually once you've verified the migration.")

    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate per-project ICM data to universal memory.")
    parser.add_argument("--project", type=Path, help="Migrate a single project path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    run(project=args.project, dry_run=args.dry_run)

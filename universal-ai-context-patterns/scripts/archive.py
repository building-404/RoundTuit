#!/usr/bin/env python3
"""
archive.py — Flush SQLite hot window to monthly Parquet cold archive.

Usage:
    python archive.py

Reads from:  ~/.ai-context/memory/icm/preferences.db
Writes to:   ~/.ai-context/memory/icm/archive/YYYY-MM.parquet

Runs automatically on first tick of each day (via icm-protocol.md §6).
Safe to run manually at any time — skips if last archive was < 24 hours ago
unless --force is passed.
"""

import argparse
import sqlite3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

MEMORY_DIR = Path.home() / ".ai-context" / "memory" / "icm"
DB_PATH = MEMORY_DIR / "preferences.db"
ARCHIVE_DIR = MEMORY_DIR / "archive"
RETENTION_DAYS = 28


def check_dependencies():
    """Verify pyarrow is available for Parquet support."""
    try:
        import pyarrow  # noqa: F401
        import pyarrow.parquet  # noqa: F401
    except ImportError:
        print("ERROR: pyarrow is required for Parquet support.")
        print("Install it with: pip install pyarrow")
        raise SystemExit(1)


def is_archive_due(conn: sqlite3.Connection) -> bool:
    """Check if archive has run in the last 24 hours."""
    row = conn.execute(
        "SELECT value FROM meta WHERE key = 'last_archive_at'"
    ).fetchone()
    if not row or not row[0]:
        return True
    last = datetime.fromisoformat(row[0]).replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - last > timedelta(hours=24)


def fetch_expired_signals(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT 'signals' as tbl, id, project_path, project_name,
               task_id, task_type, risk_level, action,
               confidence, context_json, created_at
        FROM signals
        WHERE created_at < date('now', ?)
    """, (f"-{RETENTION_DAYS} days",)).fetchall()
    return [dict(zip(
        ["tbl", "id", "project_path", "project_name", "task_id",
         "task_type", "risk_level", "action", "confidence",
         "context_json", "created_at"], row
    )) for row in rows]


def fetch_expired_decisions(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT 'decisions' as tbl, id, project_path, task_id,
               rule_id, decision, reasoning, NULL, NULL, NULL, created_at
        FROM decisions
        WHERE created_at < date('now', ?)
    """, (f"-{RETENTION_DAYS} days",)).fetchall()
    return [dict(zip(
        ["tbl", "id", "project_path", "task_id", "rule_id",
         "decision", "reasoning", "c1", "c2", "c3", "created_at"], row
    )) for row in rows]


def append_to_parquet(records: list[dict], month: str):
    """Append records to the monthly Parquet archive file."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    path = ARCHIVE_DIR / f"{month}.parquet"

    table = pa.Table.from_pylist(records)

    if path.exists():
        existing = pq.read_table(path)
        table = pa.concat_tables([existing, table])

    pq.write_table(table, path, compression="snappy")
    return len(records)


def group_by_month(records: list[dict]) -> dict[str, list[dict]]:
    """Group records by YYYY-MM of their created_at field."""
    groups: dict[str, list[dict]] = {}
    for r in records:
        month = r["created_at"][:7]  # YYYY-MM
        groups.setdefault(month, []).append(r)
    return groups


def delete_expired(conn: sqlite3.Connection):
    conn.execute(
        "DELETE FROM signals WHERE created_at < date('now', ?)",
        (f"-{RETENTION_DAYS} days",)
    )
    conn.execute(
        "DELETE FROM decisions WHERE created_at < date('now', ?)",
        (f"-{RETENTION_DAYS} days",)
    )


def flag_rules_for_review(conn: sqlite3.Connection) -> int:
    """Flag rules whose source signals have all been archived."""
    cursor = conn.execute("""
        UPDATE rules
        SET pending_review = 1
        WHERE is_permanent = 0
          AND is_active = 1
          AND pending_review = 0
          AND rule_id NOT IN (
            SELECT DISTINCT json_extract(context_json, '$.rule_id')
            FROM signals
            WHERE json_extract(context_json, '$.rule_id') IS NOT NULL
          )
    """)
    return cursor.rowcount


def update_archive_timestamp(conn: sqlite3.Connection):
    conn.execute(
        "INSERT OR REPLACE INTO meta (key, value) VALUES ('last_archive_at', ?)",
        (datetime.now(timezone.utc).isoformat(),)
    )


def run(force: bool = False):
    check_dependencies()

    if not DB_PATH.exists():
        print("Universal memory DB not found. Nothing to archive.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        if not force and not is_archive_due(conn):
            print("Archive not due yet (last run < 24 hours ago). Use --force to override.")
            return

        signals = fetch_expired_signals(conn)
        decisions = fetch_expired_decisions(conn)
        all_records = signals + decisions

        if not all_records:
            print(f"No records older than {RETENTION_DAYS} days. Nothing to archive.")
            update_archive_timestamp(conn)
            conn.commit()
            return

        # Group by month and write to Parquet
        total_archived = 0
        for month, records in group_by_month(all_records).items():
            count = append_to_parquet(records, month)
            total_archived += count
            print(f"  Archived {count} records → {month}.parquet")

        # Delete archived rows from SQLite
        delete_expired(conn)

        # Flag rules for review
        flagged = flag_rules_for_review(conn)

        # Update timestamp
        update_archive_timestamp(conn)
        conn.commit()

        print(f"\nArchive complete:")
        print(f"  {len(signals)} signals archived")
        print(f"  {len(decisions)} decisions archived")
        print(f"  {flagged} rule(s) flagged for review")

        if flagged > 0:
            print(f"\n  Run 'python review_rules.py' to review pending rules.")

    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive old signals and decisions to Parquet.")
    parser.add_argument("--force", action="store_true", help="Run even if archive ran recently")
    args = parser.parse_args()
    run(force=args.force)

#!/usr/bin/env python3
"""
review_rules.py — Surface and resolve rules pending review after archive.

Usage:
    python review_rules.py              # Interactive review
    python review_rules.py --list       # List pending rules without prompting

Rules are flagged for review when their source signals have been archived
(> 28 days old). Rules remain active while pending — this script resolves them.
"""

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".ai-context" / "memory" / "icm" / "preferences.db"


def get_pending_rules(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT rule_id, project_pattern, condition_json, action,
               confidence, signal_count, last_applied_at, derived_at
        FROM rules
        WHERE pending_review = 1
          AND is_active = 1
        ORDER BY last_applied_at DESC NULLS LAST
    """).fetchall()
    return [dict(row) for row in rows]


def format_rule(rule: dict, index: int) -> str:
    pattern = rule["project_pattern"] or "universal"
    last = rule["last_applied_at"] or "never"
    return (
        f"\n[{index}] {rule['rule_id']}\n"
        f"    scope:        {pattern}\n"
        f"    condition:    {rule['condition_json']}\n"
        f"    action:       {rule['action']}\n"
        f"    confidence:   {rule['confidence']:.2f}\n"
        f"    signal count: {rule['signal_count']}\n"
        f"    last applied: {last}\n"
        f"    derived:      {rule['derived_at']}"
    )


def resolve_rule(conn: sqlite3.Connection, rule_id: str, choice: str):
    now = datetime.utcnow().isoformat()

    if choice == "yes":
        conn.execute(
            "UPDATE rules SET pending_review = 0 WHERE rule_id = ?",
            (rule_id,)
        )
        conn.execute(
            "INSERT INTO decisions (project_path, task_id, rule_id, decision, reasoning) "
            "VALUES (?, ?, ?, ?, ?)",
            ("system", f"review-{now}", rule_id, "approved",
             "Rule confirmed active at archive review")
        )
        print(f"  ✓ {rule_id} kept active")

    elif choice == "no":
        conn.execute(
            "UPDATE rules SET is_active = 0, pending_review = 0 WHERE rule_id = ?",
            (rule_id,)
        )
        conn.execute(
            "INSERT INTO decisions (project_path, task_id, rule_id, decision, reasoning) "
            "VALUES (?, ?, ?, ?, ?)",
            ("system", f"review-{now}", rule_id, "denied",
             "Rule disabled at archive review")
        )
        print(f"  ✗ {rule_id} disabled")

    elif choice == "permanent":
        conn.execute(
            "UPDATE rules SET is_permanent = 1, pending_review = 0 WHERE rule_id = ?",
            (rule_id,)
        )
        conn.execute(
            "INSERT INTO decisions (project_path, task_id, rule_id, decision, reasoning) "
            "VALUES (?, ?, ?, ?, ?)",
            ("system", f"review-{now}", rule_id, "approved",
             "Rule made permanent at archive review — will never be flagged again")
        )
        print(f"  ★ {rule_id} made permanent")


def run_interactive(conn: sqlite3.Connection, rules: list[dict]):
    print(f"\n{len(rules)} rule(s) pending review after archive:\n")

    for i, rule in enumerate(rules, 1):
        print(format_rule(rule, i))
        while True:
            choice = input(
                "\n    Keep active? [yes / no / permanent / skip]: "
            ).strip().lower()
            if choice in ("yes", "no", "permanent", "skip"):
                break
            print("    Please enter: yes, no, permanent, or skip")

        if choice != "skip":
            resolve_rule(conn, rule["rule_id"], choice)

    conn.commit()
    print("\nReview complete.")


def run(list_only: bool = False):
    if not DB_PATH.exists():
        print("Universal memory DB not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rules = get_pending_rules(conn)

        if not rules:
            print("No rules pending review.")
            return

        if list_only:
            print(f"{len(rules)} rule(s) pending review:")
            for i, rule in enumerate(rules, 1):
                print(format_rule(rule, i))
            return

        run_interactive(conn, rules)

    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review rules pending after archive.")
    parser.add_argument("--list", action="store_true", help="List pending rules without prompting")
    args = parser.parse_args()
    run(list_only=args.list)

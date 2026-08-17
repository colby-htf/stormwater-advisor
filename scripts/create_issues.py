#!/usr/bin/env python3
"""
Create every issue in ISSUES.md as a real GitHub issue.

ISSUES.md is the single source of truth. This script just parses it and shells
out to the `gh` CLI, so editing the markdown is how you change the backlog.

Usage:
    gh auth login                      # once
    python scripts/create_issues.py --dry-run
    python scripts/create_issues.py

Note: `gh` does not create milestones, so this script creates them via the
REST API first. Labels are created on demand.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISSUES_MD = ROOT / "ISSUES.md"

HEADING = re.compile(r"^### (\d+)\.\s+(.*)$")
META = re.compile(r"^`labels:\s*(.*?)`\s*`milestone:\s*(.*?)`\s*`depends:\s*(.*?)`\s*$")


def parse(text: str) -> list[dict]:
    issues: list[dict] = []
    current: dict | None = None
    body: list[str] = []

    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            if current:
                current["body"] = "\n".join(body).strip()
                issues.append(current)
            current = {"number": int(m.group(1)), "title": m.group(2).strip()}
            body = []
            continue
        if current is None:
            continue
        m = META.match(line.strip())
        if m and "labels" not in current:
            current["labels"] = [x.strip() for x in m.group(1).split(",") if x.strip()]
            current["milestone"] = m.group(2).strip()
            current["depends"] = m.group(3).strip()
            continue
        if line.startswith("## ") or line.strip() == "---":
            continue
        body.append(line)

    if current:
        current["body"] = "\n".join(body).strip()
        issues.append(current)
    return issues


def run(cmd: list[str], dry: bool) -> str:
    if dry:
        print("  $", " ".join(cmd[:6]), "...")
        return ""
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def ensure_milestones(issues: list[dict], dry: bool) -> None:
    existing = set()
    if not dry:
        out = subprocess.run(
            ["gh", "api", "repos/{owner}/{repo}/milestones?state=all"],
            check=True, capture_output=True, text=True,
        ).stdout
        existing = {m["title"] for m in json.loads(out)}

    for title in dict.fromkeys(i["milestone"] for i in issues):
        if title in existing:
            continue
        print(f"milestone: {title}")
        run(["gh", "api", "repos/{owner}/{repo}/milestones",
             "-f", f"title={title}"], dry)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not ISSUES_MD.exists():
        print("ISSUES.md not found", file=sys.stderr)
        return 1

    issues = parse(ISSUES_MD.read_text())
    print(f"parsed {len(issues)} issues\n")

    ensure_milestones(issues, args.dry_run)

    for issue in issues:
        title = f"[{issue['number']}] {issue['title']}"
        body = issue["body"]
        if issue.get("depends", "none") != "none":
            body += f"\n\n---\nDepends on: {issue['depends']}"
        cmd = ["gh", "issue", "create", "--title", title, "--body", body,
               "--milestone", issue["milestone"]]
        for label in issue.get("labels", []):
            cmd += ["--label", label]
        print(f"#{issue['number']:>2} {issue['title']}")
        run(cmd, args.dry_run)

    print("\ndone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

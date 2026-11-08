#!/usr/bin/env python3
"""Checks an application folder without using a model. Usage: check_pack.py applications/<folder>"""
import json
import re
import sys
from pathlib import Path

NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def numbers(text: str) -> set[str]:
    return {match.replace(",", "") for match in NUMBER.findall(text)}


def check(folder: Path) -> list[str]:
    problems = []
    for name in ("master-resume.md", "job.md", "fit.md", "status.md"):
        if not (folder / name).exists():
            problems.append(f"{name} is missing")
    if problems:
        return problems

    first = (folder / "status.md").read_text().strip().splitlines()[0].strip()
    if first not in ("READY", "READY_WITH_NOTES", "SKIP"):
        problems.append("status.md must start with READY, READY_WITH_NOTES or SKIP")
    if first == "SKIP":
        return problems

    for name in ("resume.md", "cover-letter.md", "interview.md"):
        if not (folder / name).exists():
            problems.append(f"{name} is missing")
    if problems:
        return problems

    master = numbers((folder / "master-resume.md").read_text())
    for number in sorted(numbers((folder / "resume.md").read_text()) - master):
        problems.append(f"resume.md contains {number}, which is not in the master resume")

    words = len((folder / "cover-letter.md").read_text().split())
    if not 120 <= words <= 300:
        problems.append(f"cover-letter.md is {words} words")

    if first == "READY":
        try:
            verdict = json.loads((folder / "review.json").read_text()).get("verdict")
        except (OSError, ValueError, AttributeError):
            verdict = None
        if verdict != "PASS":
            problems.append("status is READY but review.json is not a PASS")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    found = check(Path(sys.argv[1]))
    for problem in found:
        print("FAIL:", problem)
    print("OK" if not found else f"{len(found)} problem(s)")
    sys.exit(1 if found else 0)

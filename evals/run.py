#!/usr/bin/env python3
"""Tests the two agents that make the judgment calls, on cases with known answers.

evals/truth/cases: <name>.<PASS or REVISE>.md replaces resume.md, or cover-letter.md if the name starts with letter-
evals/fit/cases:   <name>.<APPLY, STRETCH or SKIP>.md replaces master-resume.md
All people and companies in these files are made up.
Usage: python3 evals/run.py [--model sonnet]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"


def ask(agent: str, folder: Path, tools: list[str], model: list[str]) -> str:
    prompt = f"Review the application folder {folder.relative_to(ROOT)}. This is an offline test."
    return subprocess.run(
        ["claude", "-p", prompt, "--agent", agent, *model, "--tools", ",".join(tools),
         "--allowedTools", *tools, "--permission-mode", "dontAsk",
         "--max-budget-usd", "1", "--no-session-persistence"],
        cwd=ROOT, capture_output=True, text=True, timeout=300).stdout


def truth_case(case: Path, model: list[str]) -> str:
    with tempfile.TemporaryDirectory(dir=EVALS, prefix="tmp-") as tmp:
        folder = Path(tmp)
        for item in (EVALS / "truth").glob("*.md"):
            shutil.copy(item, folder / item.name)
        target = "cover-letter.md" if case.name.startswith("letter-") else "resume.md"
        shutil.copy(case, folder / target)
        output = ask("truth-checker", folder, ["Read", "Glob", "Grep"], model)
    found = re.findall(r'"verdict"\s*:\s*"(PASS|REVISE)"', output)
    return found[-1] if found else "NO VERDICT"


def fit_case(case: Path, model: list[str]) -> str:
    with tempfile.TemporaryDirectory(dir=EVALS, prefix="tmp-") as tmp:
        folder = Path(tmp)
        shutil.copy(EVALS / "truth" / "job.md", folder / "job.md")
        shutil.copy(case, folder / "master-resume.md")
        ask("fit-checker", folder, ["Read", "Write", "Glob", "Grep"], model)
        fit = folder / "fit.md"
        first = fit.read_text().strip().splitlines()[0] if fit.exists() else ""
    match = re.match(r"VERDICT: (APPLY|STRETCH|SKIP)", first)
    return match.group(1) if match else "NO VERDICT"


def main() -> int:
    model = sys.argv[1:]
    groups = [(truth_case, sorted((EVALS / "truth" / "cases").glob("*.md"))),
              (fit_case, sorted((EVALS / "fit" / "cases").glob("*.md")))]
    passed = total = 0
    for run_case, cases in groups:
        for case in cases:
            name, expected = case.name.removesuffix(".md").rsplit(".", 1)
            got = run_case(case, model)
            ok = got == expected
            passed += ok
            total += 1
            print(f"{'ok  ' if ok else 'FAIL'}  {name:<18} expected {expected:<8} got {got}", flush=True)
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

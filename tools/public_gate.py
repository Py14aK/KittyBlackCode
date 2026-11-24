#!/usr/bin/env python3
"""
public_gate: refuse a commit that would publish secrets or employer-internal terms.

    python3 tools/public_gate.py --staged          # files staged for commit (use as pre-commit hook)
    python3 tools/public_gate.py PATH [PATH ...]    # files or directories
    python3 tools/public_gate.py --selftest

Two pattern sources:
  1. Built-in generic secret shapes (tokens, keys, password assignments). Safe to publish.
  2. Private terms: one regex per line in the file named by $KITTY_GATE_TERMS
     (default ~/.config/kitty/gate_terms.txt). Employer names, ticket prefixes, user-id
     shapes, colleague names. That file never enters the repo, so this script names nothing.
Exit 0 clean, 1 hits found, 2 usage error. Prints file:line and the rule, never the full match.
Hook: printf '#!/bin/sh\\npython3 tools/public_gate.py --staged\\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
"""
from __future__ import annotations

import argparse, os, re, subprocess, sys
from pathlib import Path

GENERIC = {
    "github token": r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}",
    "anthropic key": r"\bsk-ant-[A-Za-z0-9_-]{20,}",
    "openai-style key": r"\bsk-[A-Za-z0-9]{32,}\b",
    "aws key id": r"\bAKIA[0-9A-Z]{16}\b",
    "slack token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "password assignment": r"(?i)\b(pass(word)?|pwd)\s*[:=]\s*(?!string\b|['\"]?\[|process\.env)['\"]?[^\s'\"$<{]{6,}",
}
SKIP_DIRS = {".git", "node_modules", "reports", "test-results"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".pdf", ".xlsx", ".docx", ".pptx", ".bundle"}


def private_rules() -> dict[str, str]:
    path = Path(os.environ.get("KITTY_GATE_TERMS", Path.home() / ".config/kitty/gate_terms.txt"))
    if not path.exists():
        print(f"note: no private terms file at {path}; only generic secret patterns are checked", file=sys.stderr)
        return {}
    rules = {}
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if line and not line.startswith("#"):
            rules[f"private term #{i}"] = line
    return rules


def staged() -> list[Path]:
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                         capture_output=True, text=True, check=True).stdout
    return [Path(p) for p in out.splitlines() if p]


def walk(paths: list[Path]) -> list[Path]:
    files = []
    for p in paths:
        if p.is_dir():
            files += [f for f in p.rglob("*") if f.is_file() and not SKIP_DIRS & set(f.parts)]
        elif p.is_file():
            files.append(p)
    return [f for f in files if f.suffix.lower() not in SKIP_EXT]


def scan(files: list[Path], rules: dict[str, str]) -> int:
    compiled = {k: re.compile(v) for k, v in rules.items()}
    hits = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for name, rx in compiled.items():
                if rx.search(line):
                    hits += 1
                    print(f"HIT {f}:{n}: {name}")
        # file names leak too
        for name, rx in compiled.items():
            if name.startswith("private") and rx.search(str(f)):
                hits += 1
                print(f"HIT {f}: path matches {name}")
    print(f"public_gate: {len(files)} files, {hits} hits")
    return hits


def selftest() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("ok line\npassword = hunter22x\ntoken ghp_" + "a" * 36 + "\nAcme internal\n")
        assert scan([p], {**GENERIC, "private term #1": r"\bAcme\b"}) == 3
        p.write_text("password = $T24_INPUT_PASS\nfill(c.pass)\npass: string;\npass: '[name=\"password\"]'\n")
        assert scan([p], GENERIC) == 0, "env references must not trip the gate"
    print("public_gate selftest: ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    files = staged() if a.staged else walk(a.paths)
    if not files:
        print("public_gate: nothing to scan")
        return 0 if a.staged else 2
    return 1 if scan(walk(files), {**GENERIC, **private_rules()}) else 0


if __name__ == "__main__":
    sys.exit(main())

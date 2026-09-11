"""Compare every file against MANIFEST.sha256 as handed over on 2026-09-09.

A CHANGED line is not an error. It says: this file differs from the handover.
Run the check and re-read EDITING.md before trusting it.
"""
import hashlib
import pathlib
import sys

changed = missing = ok = 0
for line in pathlib.Path("MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    if not line or line.startswith("#"):
        continue
    digest, _, rel = line.partition("  ")
    p = pathlib.Path(rel)
    if not p.exists():
        print(f"MISSING  {rel}")
        missing += 1
    elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        print(f"CHANGED  {rel}")
        changed += 1
    else:
        ok += 1
print(f"\n{ok} unchanged, {changed} changed, {missing} missing")
sys.exit(0)

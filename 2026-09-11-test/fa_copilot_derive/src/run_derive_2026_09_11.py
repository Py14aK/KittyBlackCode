"""Run the triangulation over the VoP atom set and print the backlog."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atoms_2026_09_11 import load_atoms  # noqa: E402
from derive_cases_2026_09_11 import derive_cases, report, triangulate  # noqa: E402


def main(path: str | None = None) -> int:
    default = Path(__file__).resolve().parents[1] / "data" / "atoms_vop_2026-09-11.tsv"
    data = Path(path) if path else default
    atoms = load_atoms(data)
    findings = triangulate(atoms)
    cases = derive_cases(findings)

    print(f"{len(atoms)} atoms from {data.name}\n")
    print(report(findings))
    print("DERIVED CASES")
    print("=" * 62)
    for c in cases:
        mark = "run" if c.runnable else "blocked"
        print(f"{c.case_id}  [{c.verdict.value:<13}] {mark:<8} {c.subject}")
        print(f"         when: {c.when}")
        print(f"         from: {', '.join(c.sources)}")
    print(f"\n{sum(1 for c in cases if c.runnable)} runnable, "
          f"{sum(1 for c in cases if not c.runnable)} blocked, "
          f"{len(findings) - len(cases)} subjects yielded no case")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))

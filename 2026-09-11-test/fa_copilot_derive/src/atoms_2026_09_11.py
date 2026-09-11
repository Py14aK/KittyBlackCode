"""Atoms: the smallest addressable unit of a document, with its source anchor.

An atom is one behavioural claim, from one source, traceable back to the line
it came from.  Documents are prose; atoms are addressable.  Everything
downstream - triangulation, test derivation, coverage - needs the address.

Three sources, and they do not carry equal weight:

    BRD        fact       contracted, testable, delivered to us
    FSD_S8     claim      what the solution section says we will do
    T24        empirical  what the system was observed to do

A claim is not a fact.  An observation is not a requirement.  Collapsing the
three is the mistake this module exists to prevent.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Source(StrEnum):
    BRD = "BRD"        # fact: contracted requirement
    FSD_S8 = "FSD_S8"  # claim: section 8, Solution
    T24 = "T24"        # empirical: observed behaviour

    @property
    def weight(self) -> int:
        """BRD outranks a claim; an observation outranks neither, it reports."""
        return {"BRD": 3, "FSD_S8": 2, "T24": 1}[self.value]


class Verdict(StrEnum):
    """What the triangulation found for one subject."""

    DEFECT = "DEFECT"              # required and claimed, system does otherwise
    SPEC_GAP = "SPEC_GAP"          # required, nothing in the solution
    CLAIM_DRIFT = "CLAIM_DRIFT"    # required and claimed, but the two disagree
    CLAIM_WRONG = "CLAIM_WRONG"    # system meets the BRD, the FSD says otherwise
    UNVERIFIED = "UNVERIFIED"      # required and claimed, never observed
    UNDOCUMENTED = "UNDOCUMENTED"  # observed, required by nobody
    GOLD_PLATING = "GOLD_PLATING"  # claimed, required by nobody
    CONFIRMED = "CONFIRMED"        # all three agree

    @property
    def priority(self) -> int:
        """Lower runs first.  Contradictions before absences before agreements."""
        return {
            "DEFECT": 1,
            "SPEC_GAP": 2,
            "CLAIM_DRIFT": 3,
            "CLAIM_WRONG": 4,
            "UNVERIFIED": 5,
            "UNDOCUMENTED": 6,
            "GOLD_PLATING": 7,
            "CONFIRMED": 8,
        }[self.value]


@dataclass(frozen=True)
class Atom:
    """One behavioural claim from one source.

    subject  groups atoms across sources.  Two atoms sharing a subject are
             statements about the same thing and can be compared.
    assertion the normalised behaviour, so BRD and T24 wording differ but the
             assertion matches when they agree.
    anchor   where it came from, so a reader can go and check.
    """

    atom_id: str
    source: Source
    subject: str
    assertion: str
    anchor: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.subject:
            raise ValueError(
                f"{self.atom_id}: subject is the join key, it cannot be empty"
            )
        if not self.anchor:
            raise ValueError(
                f"{self.atom_id}: an atom without an anchor cannot be checked"
            )


def load_atoms(path: str | Path) -> list[Atom]:
    """Read a tab-separated atom file.

    Tidy long format, one atom per row, at the adapter boundary.  TSV rather
    than CSV because the assertions contain commas and Bulgarian punctuation.
    """
    rows: list[Atom] = []
    with Path(path).open(encoding="utf-8", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh, delimiter="\t"), start=2):
            if not r.get("atom_id") or r["atom_id"].startswith("#"):
                continue
            try:
                rows.append(
                    Atom(
                        atom_id=r["atom_id"].strip(),
                        source=Source(r["source"].strip()),
                        subject=r["subject"].strip(),
                        assertion=r["assertion"].strip(),
                        anchor=r["anchor"].strip(),
                        note=(r.get("note") or "").strip(),
                    )
                )
            except (KeyError, ValueError) as exc:
                raise ValueError(f"{path}:{i}: {exc}") from exc
    ids = [a.atom_id for a in rows]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"{path}: duplicate atom ids {sorted(dupes)}")
    return rows

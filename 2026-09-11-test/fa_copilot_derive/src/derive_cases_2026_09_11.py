"""Derive test cases from the disagreement between three sources.

Agreement produces regression tests, which are cheap and boring.  Disagreement
produces findings, which are the reason anyone does functional analysis.

The pilot decides.  This module only shows where the three sources fail to
line up, and in which order that matters.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from atoms_2026_09_11 import Atom, Source, Verdict


@dataclass
class Finding:
    """One subject, triangulated."""

    subject: str
    verdict: Verdict
    brd: Atom | None
    claim: Atom | None
    empirical: Atom | None
    rationale: str
    atoms: list[str] = field(default_factory=list)

    @property
    def priority(self) -> int:
        return self.verdict.priority

    @property
    def blocking(self) -> bool:
        """A finding that stops a release rather than joining a backlog."""
        return self.verdict in (
            Verdict.DEFECT,
            Verdict.SPEC_GAP,
            Verdict.CLAIM_DRIFT,
            Verdict.CLAIM_WRONG,
        )


@dataclass
class TestCase:
    """A derived scenario.  Carries its provenance, always."""

    case_id: str
    subject: str
    verdict: Verdict
    given: str
    when: str
    then: str
    sources: list[str]
    runnable: bool
    blocked_reason: str = ""


def _agree(a: Atom | None, b: Atom | None) -> bool:
    """Normalised comparison of two assertions.

    Deliberately literal.  A fuzzy match here would hide exactly the small
    wording differences that turn out to be real disagreements.
    """
    if a is None or b is None:
        return False
    return a.assertion.strip().casefold() == b.assertion.strip().casefold()


def triangulate(atoms: list[Atom]) -> list[Finding]:
    """Group atoms by subject and classify each group."""
    by_subject: dict[str, dict[Source, Atom]] = defaultdict(dict)
    for a in atoms:
        if a.source in by_subject[a.subject]:
            raise ValueError(
                f"subject {a.subject!r} has two {a.source.value} atoms; "
                "split the subject or merge the atoms"
            )
        by_subject[a.subject][a.source] = a

    findings: list[Finding] = []
    for subject, m in by_subject.items():
        brd, claim, emp = m.get(Source.BRD), m.get(Source.FSD_S8), m.get(Source.T24)

        if brd and claim and emp:
            if _agree(brd, emp) and _agree(brd, claim):
                v, why = (
                    Verdict.CONFIRMED,
                    "All three agree. Lock it with a regression test.",
                )
            elif _agree(brd, emp) and not _agree(brd, claim):
                v, why = (
                    Verdict.CLAIM_WRONG,
                    "System satisfies the BRD; the solution section says otherwise. "
                    "Document defect, not a code defect.",
                )
            else:
                v, why = (
                    Verdict.DEFECT,
                    "Required and claimed, but observed behaviour differs. Raise it.",
                )
        elif brd and claim and not emp:
            if _agree(brd, claim):
                v, why = (
                    Verdict.UNVERIFIED,
                    "Required and claimed, never observed. This is the UAT backlog.",
                )
            else:
                v, why = (
                    Verdict.CLAIM_DRIFT,
                    "Requirement and solution say different things. Found without "
                    "running anything; resolve on paper before it reaches test.",
                )
        elif brd and not claim:
            v, why = (
                Verdict.SPEC_GAP,
                "Contracted requirement with nothing in the solution. Blocking; "
                "no test can be written yet.",
            )
        elif claim and not brd:
            v, why = (
                Verdict.GOLD_PLATING,
                "The solution claims behaviour nobody required. Confirm the source "
                "or drop it.",
            )
        else:
            v, why = (
                Verdict.UNDOCUMENTED,
                "Observed behaviour nobody wrote down. Decide: keep and document, "
                "or remove.",
            )

        findings.append(
            Finding(
                subject=subject,
                verdict=v,
                brd=brd,
                claim=claim,
                empirical=emp,
                rationale=why,
                atoms=sorted(a.atom_id for a in m.values()),
            )
        )

    return sorted(findings, key=lambda f: (f.priority, f.subject))


def derive_cases(findings: list[Finding], prefix: str = "TC") -> list[TestCase]:
    """Turn findings into scenarios.

    A SPEC_GAP yields no test on purpose.  Writing a test for a requirement
    with no solution invents the expectation, and an invented expectation is
    the quietest way to ship the wrong thing.
    """
    cases: list[TestCase] = []
    n = 0
    for f in findings:
        if f.verdict is Verdict.SPEC_GAP:
            continue
        n += 1
        anchor = f.brd or f.claim or f.empirical
        assert anchor is not None
        expected = (f.brd or f.claim or f.empirical).assertion
        runnable = f.empirical is not None or f.verdict is Verdict.UNVERIFIED
        cases.append(
            TestCase(
                case_id=f"{prefix}{n:03d}",
                subject=f.subject,
                verdict=f.verdict,
                given=f"T24, VoP scope, subject: {f.subject}",
                when=anchor.assertion,
                then=f"Expected per {'BRD' if f.brd else 'solution claim'}: {expected}",
                sources=[a.atom_id for a in (f.brd, f.claim, f.empirical) if a],
                runnable=runnable,
                blocked_reason="" if runnable else f.rationale,
            )
        )
    return cases


def report(findings: list[Finding]) -> str:
    """Plain text summary. Highest value first."""
    out: list[str] = []
    counts: dict[str, int] = defaultdict(int)
    for f in findings:
        counts[f.verdict.value] += 1

    out.append("TRIANGULATION")
    out.append("=" * 62)
    for v in sorted(Verdict, key=lambda x: x.priority):
        if counts[v.value]:
            flag = "  <- blocking" if v in (
                Verdict.DEFECT,
                Verdict.SPEC_GAP,
                Verdict.CLAIM_DRIFT,
                Verdict.CLAIM_WRONG,
            ) else ""
            out.append(f"{counts[v.value]:3d}  {v.value}{flag}")
    out.append("")
    blocking = [f for f in findings if f.blocking]
    out.append(
        f"{len(blocking)} blocking, {len(findings) - len(blocking)} for the backlog"
    )
    out.append("")
    for f in findings:
        if not f.blocking:
            continue
        out.append(f"[{f.verdict.value}] {f.subject}")
        out.append(f"    {f.rationale}")
        for lbl, a in (("BRD", f.brd), ("claim", f.claim), ("T24", f.empirical)):
            shown = f"{a.anchor}: {a.assertion}" if a else "- none -"
            out.append(f"    {lbl:<6} {shown}")
        out.append("")
    return "\n".join(out)

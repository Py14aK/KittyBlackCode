"""Tests for the deriver itself.

The deriver decides what gets tested.  If it is wrong, everything downstream
inherits the error silently, so it needs its own tests more than most code.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from atoms_2026_09_11 import Atom, Source, Verdict, load_atoms  # noqa: E402
from derive_cases_2026_09_11 import derive_cases, triangulate  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "atoms_vop_2026-09-11.tsv"


def atom(aid, src, subj, assertion, anchor="x"):
    return Atom(aid, Source(src), subj, assertion, anchor)


def verdict_of(atoms):
    return triangulate(atoms)[0].verdict


# --- the classification matrix, one test per cell -------------------------

def test_all_three_agree_is_confirmed():
    assert verdict_of([
        atom("B", "BRD", "s", "the field is mandatory"),
        atom("C", "FSD_S8", "s", "the field is mandatory"),
        atom("E", "T24", "s", "the field is mandatory"),
    ]) is Verdict.CONFIRMED


def test_requirement_with_no_solution_is_a_spec_gap():
    assert verdict_of([atom("B", "BRD", "s", "print a slip")]) is Verdict.SPEC_GAP


def test_solution_with_no_requirement_is_gold_plating():
    v = verdict_of([atom("C", "FSD_S8", "s", "also send an email")])
    assert v is Verdict.GOLD_PLATING


def test_behaviour_nobody_wrote_down_is_undocumented():
    assert verdict_of([atom("E", "T24", "s", "it also logs")]) is Verdict.UNDOCUMENTED


def test_required_and_claimed_but_unobserved_is_unverified():
    assert verdict_of([
        atom("B", "BRD", "s", "same wording"),
        atom("C", "FSD_S8", "s", "same wording"),
    ]) is Verdict.UNVERIFIED


def test_requirement_and_claim_disagreeing_on_paper_is_claim_drift():
    """The cell added after the first run missed it. Found without running T24."""
    assert verdict_of([
        atom("B", "BRD", "s", "a close match returns a suggested name"),
        atom("C", "FSD_S8", "s", "a close match returns a name and stores it"),
    ]) is Verdict.CLAIM_DRIFT


def test_system_matching_the_brd_against_a_wrong_claim_is_claim_wrong():
    assert verdict_of([
        atom("B", "BRD", "s", "blocks the second FT"),
        atom("C", "FSD_S8", "s", "warns on the second FT"),
        atom("E", "T24", "s", "blocks the second FT"),
    ]) is Verdict.CLAIM_WRONG


def test_system_contradicting_both_is_a_defect():
    assert verdict_of([
        atom("B", "BRD", "s", "blocks the second FT"),
        atom("C", "FSD_S8", "s", "blocks the second FT"),
        atom("E", "T24", "s", "allows the second FT"),
    ]) is Verdict.DEFECT


# --- ordering and guarantees ---------------------------------------------

def test_contradictions_sort_above_absences_above_agreements():
    order = [v.priority for v in (
        Verdict.DEFECT, Verdict.SPEC_GAP, Verdict.CLAIM_DRIFT,
        Verdict.CLAIM_WRONG, Verdict.UNVERIFIED, Verdict.UNDOCUMENTED,
        Verdict.GOLD_PLATING, Verdict.CONFIRMED)]
    assert order == sorted(order)


def test_a_spec_gap_never_yields_a_test_case():
    """Writing a test for an unsolutioned requirement invents the expectation."""
    findings = triangulate([atom("B", "BRD", "s", "print a slip")])
    assert derive_cases(findings) == []


def test_every_case_carries_its_provenance():
    cases = derive_cases(triangulate(load_atoms(DATA)))
    assert cases
    assert all(c.sources for c in cases)


# --- input contracts ------------------------------------------------------

def test_an_atom_without_an_anchor_is_rejected():
    with pytest.raises(ValueError, match="anchor"):
        Atom("X", Source.BRD, "s", "something", "")


def test_two_atoms_from_one_source_on_one_subject_are_rejected():
    with pytest.raises(ValueError, match="two BRD atoms"):
        triangulate([
            atom("B1", "BRD", "s", "one thing"),
            atom("B2", "BRD", "s", "another thing"),
        ])


def test_the_shipped_atom_file_loads_and_has_all_three_sources_declared():
    atoms = load_atoms(DATA)
    assert len(atoms) == 31
    present = {a.source for a in atoms}
    assert Source.BRD in present and Source.FSD_S8 in present
    # T24 is deliberately absent: nothing has been observed yet.
    assert Source.T24 not in present


def test_the_shipped_set_reports_the_internal_branch_as_unsolutioned():
    gaps = {f.subject for f in triangulate(load_atoms(DATA))
            if f.verdict is Verdict.SPEC_GAP}
    assert all(s.startswith("internal.") for s in gaps)
    assert len(gaps) == 5

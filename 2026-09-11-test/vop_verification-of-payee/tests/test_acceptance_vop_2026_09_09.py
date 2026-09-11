"""AC01-AC16 as executable tests against the reference model.

Test names carry the acceptance-scenario ID.  That is the whole traceability
mechanism: grep an ID, get the requirement and the test that can refute it.

Scenarios blocked on an undecided question are skipped, not guessed, and the
skip reason names the decision that unblocks them.
"""
from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vop_enquiry_model_2026_09_09 import (  # noqa: E402
    ConfirmationRequiredError,
    DuplicateFTError,
    Enquiry,
    NoRecordError,
    OpenDecisionError,
    Selection,
    reload,
)

T0 = datetime(2026, 9, 9, 9, 0, tzinfo=UTC)


def sel(n: int = 1) -> Selection:
    return Selection(
        iban=f"BG{n:02d}UBBS80021012345678",
        name_lat=f"PAYEE {n}",
        name_cyr=f"ПОЛУЧАТЕЛ {n}",
    )


def seeded(n: int, *, with_ft: int = 0) -> Enquiry:
    e = Enquiry()
    for i in range(1, n + 1):
        r = e.generate_request(sel(i), response_code="MTCH", now=T0)
        if i <= with_ft:
            e.create_ft(r.request_id)
    return e


# --- AC01-AC04: what the enquiry shows -------------------------------------

def test_AC01_empty_scope_shows_only_the_last_row():
    rows = Enquiry().render()
    assert len(rows) == 1
    assert rows[0].is_last


def test_AC02_three_records_with_ft_stay_visible_plus_last_row():
    rows = seeded(3, with_ft=3).render()
    assert len(rows) == 4
    assert all(r.request.has_ft for r in rows[:3])   # R02
    assert rows[-1].is_last                          # R03


def test_AC03_new_request_from_last_row_then_back():
    e = seeded(3, with_ft=3)
    e.generate_request(sel(9), now=T0)
    rows = reload(e)
    assert len(rows) == 5
    assert sum(1 for r in rows[:-1] if r.request.has_ft) == 3
    assert rows[-1].is_last


def test_AC04_pending_request_does_not_remove_the_last_row():
    e = seeded(4, with_ft=3)                 # record 4 has no FT
    e.generate_request(sel(9), now=T0)       # R04
    rows = e.render()
    assert rows[-1].is_last
    assert sum(1 for r in rows if r.is_last) == 1


# --- AC05: the identity rule, the one that changed mid-transcript ----------

def test_AC05_regenerating_from_an_existing_row_creates_a_new_id():
    e = seeded(4, with_ft=3)
    q4 = e.records[3]
    q5 = e.generate_request(source_id=q4.request_id, now=T0)
    assert q5.request_id != q4.request_id            # R07
    assert e.get(q4.request_id).ft_reference is None  # not overwritten
    assert q5.selection == q4.selection               # V02, narrowest reading
    assert len(e.records) == 5


# --- AC06-AC09: the FT route ----------------------------------------------

def test_AC06_ft_binds_to_the_selected_request_and_creates_nothing_else():
    e = seeded(4, with_ft=3)
    q4 = e.records[3]
    before = len(e.records)
    ft = e.create_ft(q4.request_id)                   # R08
    assert e.get(q4.request_id).ft_reference == ft
    assert len(e.records) == before                   # no new request
    assert len(reload(e)) == before + 1


def test_AC07_second_ft_on_the_same_request_is_blocked():
    e = seeded(1, with_ft=1)
    with pytest.raises(DuplicateFTError):             # R09
        e.create_ft(e.records[0].request_id)


def test_AC08_stale_view_still_reads_current_state():
    e = seeded(1)
    stale_id = e.records[0].request_id                # captured before the FT
    e.create_ft(stale_id)
    with pytest.raises(DuplicateFTError):
        e.create_ft(stale_id)


def test_AC09_two_attempts_yield_at_most_one_ft():
    e = seeded(1)
    rid = e.records[0].request_id
    ok, refused = 0, 0
    for _ in range(2):
        try:
            e.create_ft(rid)
            ok += 1
        except DuplicateFTError:
            refused += 1
    assert (ok, refused) == (1, 1)


def test_AC03b_ft_has_no_basis_on_the_last_row():
    with pytest.raises(NoRecordError):                # R03
        Enquiry().create_ft("VOP-0001")


# --- AC10, AC15, AC16: response codes and admissibility --------------------

def test_AC10_a_negative_check_never_blocks_a_new_one():
    e = Enquiry()
    e.generate_request(sel(1), response_code="NMTC", now=T0)
    fresh = e.generate_request(sel(1), now=T0)        # allowed, always
    assert fresh.request_id != e.records[0].request_id


@pytest.mark.parametrize("code", ["NMTC", "NOAP"])
def test_AC10b_admissibility_of_a_negative_check_is_undecided(code):
    e = Enquiry()
    r = e.generate_request(sel(1), response_code=code, now=T0)
    with pytest.raises(OpenDecisionError) as exc:
        e.create_ft(r.request_id)
    assert exc.value.decision_id == "V07"


def test_AC15_close_match_needs_a_recorded_confirmation():
    e = Enquiry()
    r = e.generate_request(
        sel(1), response_code="CMTC", suggested_name="IVAN P PETROV", now=T0
    )
    with pytest.raises(ConfirmationRequiredError):
        e.create_ft(r.request_id)
    ft = e.create_ft(r.request_id, client_confirmed=True)
    assert e.get(r.request_id).ft_reference == ft
    assert e.get(r.request_id).suggested_name == "IVAN P PETROV"  # V12


def test_AC11b_name_over_140_chars_is_an_open_decision():
    with pytest.raises(OpenDecisionError) as exc:
        Selection(iban="BG18UBBS8002", name_lat="X" * 141, name_cyr="Х")
    assert exc.value.decision_id == "V11"


def test_AC08b_regenerating_from_a_completed_row_is_undecided():
    e = seeded(1, with_ft=1)
    with pytest.raises(OpenDecisionError) as exc:
        e.generate_request(source_id=e.records[0].request_id, now=T0)
    assert exc.value.decision_id == "V08"


# --- blocked on decisions: recorded, not guessed --------------------------

@pytest.mark.skip(reason="blocked on V05 - session scope of the concat key")
def test_AC11_visibility_after_a_new_session():
    raise AssertionError("unreachable until V05 is decided")


@pytest.mark.skip(reason="blocked on V04 - send/commit sequence and timeout")
def test_AC12_timeout_after_dispatch():
    raise AssertionError("unreachable until V04 is decided")


@pytest.mark.skip(reason="blocked on V04 - partial-failure recovery")
def test_AC13_record_written_but_concat_link_failed():
    raise AssertionError("unreachable until V04 is decided")


@pytest.mark.skip(reason="blocked on V06 - moment the FT reference is filled")
def test_AC14_ft_started_but_not_authorised():
    raise AssertionError("unreachable until V06 is decided")


@pytest.mark.skip(reason="blocked on V10 - client-sector rule for the local field")
def test_AC16_sector_rule_forces_the_local_field():
    raise AssertionError("unreachable until V10 is decided")

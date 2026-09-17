"""Reference model of the VoP enquiry: two routes, one identity rule.

Executable specification for the T24 Verification-of-Payee enquiry.
Pure Python. Touches no banking system, no network, no T24 client.

Its only job: make the rules R02-R09 falsifiable. Every rule below is
referenced by ID from tests/test_acceptance_vop_2026_09_09.py.

Filename uses underscores, not the 2026-09-09 hyphen convention, because
hyphens are invalid in Python module names.
"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from itertools import count
from typing import Literal

ResponseCode = Literal["MTCH", "CMTC", "NMTC", "NOAP"]

#: Response codes that permit an FT without further decision.  V07 is open:
#: NMTC and NOAP are NOT listed here on purpose.  Adding them is a business
#: decision, not a code change made in passing.
ADMISSIBLE: frozenset[str] = frozenset({"MTCH"})

#: CMTC returns a suggested name and requires an explicit client confirmation
#: recorded as a separate event (V12).
NEEDS_CONFIRMATION: frozenset[str] = frozenset({"CMTC"})


class VopError(Exception):
    """Base for every refusal this model can express."""


class DuplicateFTError(VopError):
    """R09 - the selected request already carries an FT reference."""


class NoRecordError(VopError):
    """R03 - the last row is not yet a record; FT has no basis on it."""


class OpenDecisionError(VopError):
    """The rule needed here has not been decided yet.  Carries the decision ID.

    Raising rather than guessing is deliberate.  A model that silently picks a
    branch on an undecided question produces a specification nobody agreed to.
    """

    def __init__(self, decision_id: str, detail: str) -> None:
        self.decision_id = decision_id
        super().__init__(f"{decision_id}: {detail}")


class ConfirmationRequiredError(VopError):
    """CMTC without a recorded client confirmation."""


@dataclass(frozen=True)
class Selection:
    """The three attributes carried by the last row of the enquiry.

    They are exactly the three input fields of the business document:
    IBAN, payee name in Latin, payee name in Cyrillic.
    """

    iban: str
    name_lat: str
    name_cyr: str

    def __post_init__(self) -> None:
        # VARCHAR 140 on both name fields, per the business document.
        for label, value in (("name_lat", self.name_lat), ("name_cyr", self.name_cyr)):
            if len(value) > 140:
                raise OpenDecisionError(
                    "V11", f"{label} exceeds 140 chars; truncate or reject is undecided"
                )
        if not self.iban:
            raise ValueError("iban is required; it keys the check")


@dataclass
class Request:
    """One VoP check.  Permanent identity; an FT reference at most once."""

    request_id: str
    selection: Selection
    response_code: ResponseCode
    request_time: datetime
    suggested_name: str | None = None
    ft_reference: str | None = None
    #: Borica Check ID, if it is a separate value from request_id.
    #: V01 is open; None means "not decided".
    external_check_id: str | None = None

    @property
    def has_ft(self) -> bool:
        return self.ft_reference is not None


@dataclass
class Row:
    """A rendered line of the enquiry."""

    number: int
    request: Request | None  # None marks the last row

    @property
    def is_last(self) -> bool:
        return self.request is None


@dataclass
class Enquiry:
    """The enquiry itself.  Holds records; always offers one more row."""

    records: list[Request] = field(default_factory=list)
    _req_seq: Iterator[int] = field(default_factory=lambda: count(1), repr=False)
    _ft_seq: Iterator[int] = field(default_factory=lambda: count(1), repr=False)

    # -- reading ---------------------------------------------------------
    def render(self) -> list[Row]:
        """R02 + R03.

        Rows with an FT are not hidden.  Exactly one last row is appended,
        always, regardless of whether unfinished requests exist (R04).
        """
        rows = [Row(i + 1, r) for i, r in enumerate(self.records)]
        rows.append(Row(len(rows) + 1, None))
        return rows

    def get(self, request_id: str) -> Request:
        for r in self.records:
            if r.request_id == request_id:
                return r
        raise NoRecordError(f"no record {request_id!r}")

    # -- route one: generate a request -----------------------------------
    def generate_request(
        self,
        selection: Selection | None = None,
        *,
        source_id: str | None = None,
        response_code: ResponseCode = "MTCH",
        suggested_name: str | None = None,
        now: datetime | None = None,
    ) -> Request:
        """R06 + R07.

        From the last row, or from any existing row.  Both produce a NEW
        record with a NEW id.  The source row is never overwritten.

        Which attributes are carried over from a source row is V02 and is
        deliberately implemented as "all three, verbatim" - the narrowest
        reading of the transcript.  Widen it only by decision.
        """
        if source_id is not None:
            source = self.get(source_id)
            if source.has_ft:
                raise OpenDecisionError(
                    "V08", "re-checking from a row that already carries an FT"
                )
            selection = source.selection  # V02
        if selection is None:
            raise ValueError("selection required when no source row is given")
        if response_code == "CMTC" and suggested_name is None:
            raise ValueError("CMTC must carry the suggested name")

        rec = Request(
            request_id=f"VOP-{next(self._req_seq):04d}",
            selection=selection,
            response_code=response_code,
            request_time=now or datetime.now(UTC),
            suggested_name=suggested_name,
        )
        self.records.append(rec)
        return rec

    # -- route two: create an FT -----------------------------------------
    def create_ft(
        self, request_id: str, *, client_confirmed: bool = False
    ) -> str:
        """R08 + R09.

        Reads the selected request by its own id and checks for an existing
        FT reference before doing anything else.  The check and the write sit
        in one call on purpose: splitting them is what lets two open versions
        both succeed (V09).
        """
        rec = self.get(request_id)
        if rec.has_ft:
            raise DuplicateFTError(
                f"{request_id} already carries {rec.ft_reference}"
            )
        if rec.response_code not in ADMISSIBLE:
            if rec.response_code in NEEDS_CONFIRMATION:
                if not client_confirmed:
                    raise ConfirmationRequiredError(
                        f"{rec.response_code} needs a recorded client confirmation"
                    )
            else:
                raise OpenDecisionError(
                    "V07", f"admissibility of {rec.response_code} is undecided"
                )
        rec.ft_reference = f"FT2609{next(self._ft_seq):04d}"
        return rec.ft_reference


def reload(enquiry: Enquiry) -> list[Row]:
    """R05 - Back re-runs the enquiry.  Nothing is created by reloading."""
    return enquiry.render()

# VoP — verification of payee, T24 enquiry

Verification of payee on outgoing SEPA credit / SEPA instant and internal
transfers, under Regulation (EU) 2024/886. The T24 enquiry calls a Borica
microservice; internal versions compare Ben. Customer 1 against BG.NAME in
CUSTOMER.

Two routes out of one enquiry. One creates a new identity, the other consumes
an existing one. That distinction is the whole specification; everything else
is a consequence of it.

Working concept, 2026-09-09. Not an approved FSD. Describes no verified
implementation. No test was run against a banking system.

## What is here

| Path | What it is |
| --- | --- |
| `UBB_VoP_Handover_2026-09-09.html` | Handover deck for PM and BA, Bulgarian, with a live enquiry simulator. Open it in a browser; nothing is stored. |
| `src/vop_enquiry_model_2026_09_09.py` | Reference model of rules R02–R09. Pure Python, no network, no T24 client. |
| `tests/test_acceptance_vop_2026_09_09.py` | AC01–AC16 as tests. Test name carries the scenario id. |
| `docs/DECISIONS.md` | V01–V13, all open. |

## Run it

```bash
python -m pip install pytest ruff
ruff check .
python -m pytest -q
```

Expected: `16 passed, 5 skipped`. The five skips are not failures. Each is a
scenario blocked on an undecided question, and the skip reason names the
decision that unblocks it. When a `Vxx` is answered, one skip turns into a
test with a known expectation. That is the progress metric for this folder —
skips remaining, not lines written.

## Why a model at all

The transcript produced prose. Prose cannot be refuted. The model exists so
that every rule has an id, every id has a test, and a wrong reading fails
loudly instead of surviving into a specification nobody agreed to.

Where a rule was never decided, the model raises `OpenDecisionError` carrying
the decision id rather than picking a branch. Guessing quietly is the failure
mode this folder is built to prevent.

## Naming

Deliverables carry the date: `UBB_VoP_Handover_2026-09-09.html`. Python
modules use underscores instead — hyphens are invalid in module names.

## Provenance

Derived from two transcript excerpts, the business document and screenshots of
working screens. Statements about implementation are interpretation, not fact.
Recommendations on concurrency, session durability and technical retry are the
assistant's additions and were not decided in the conversation.

Technical detail is written as in the source: version names, field names,
response codes and sector values. Names of staff, ticket keys and internal
hosts are not carried over.

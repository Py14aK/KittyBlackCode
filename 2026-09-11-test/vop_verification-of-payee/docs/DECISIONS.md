# VoP: decision form

Status: open. Nothing here is decided. An assistant-filled decision form is
more dangerous than an empty one, so these stay blank until the team answers.

Convention: one row, one decision. When a row is answered, move it into its
own ADR file under `docs/decisions/` with the date and the owner, and replace
the row here with a link. The `Blocks` column is what stops moving.

| ID | Decision needed | Blocks | Answer | Owner / date |
| --- | --- | --- | --- | --- |
| V01 | Identifiers: local record key, Borica Check ID, concat value. Are they one field or three? Do not assume synonyms. | everything | | |
| V02 | New id when regenerating from an existing row: generator, moment of assignment, which attributes carry over. A timestamp is not a uniqueness spec. | AC05 | | |
| V03 | Meaning of "second request": a second FT, a repeat external call on the same check id, or two separate controls. | AC07 | | |
| V04 | Dispatch, write, concat and response: exact order; behaviour on timeout and partial failure. | AC12, AC13 | | |
| V05 | Session id in the concat key: visibility after re-login, scope across tabs and users. | AC11 | | |
| V06 | When the FT reference is written: creation, commit or authorisation. Behaviour for started, refused, cancelled, reversed. | AC14 | | |
| V07 | Validity window of a check, and which of MTCH / CMTC / NMTC / NOAP admit an FT. Regulatorily the heaviest question here and it was never raised in the transcript. | AC10b | | |
| V08 | Actions available on a row that already carries an FT. May a new check start from it? | AC08b | | |
| V09 | Guarding against a double FT under concurrent attempts; whether the scope crosses sessions. | AC09 | | |
| V10 | The Yes/No local field: mandatory where client sector is not 5100 / 5200 / 5900 / 9400. Does it apply identically to UBB.INT.ACC.TO.ACC, UBB.INT.BUDGET and UBB.INT.BUDGET.250? | AC16 | | |
| V11 | Latin vs Cyrillic: which name goes to Borica, behaviour past 140 characters, transliterate or refuse. | AC11b | | |
| V12 | Evidence of the check: what is written into the payment, what is printed on commit, where the suggested name from a close match is stored. | AC15 | | |
| V13 | One model or two: the external route asks the Borica microservice, the internal route compares BG.NAME in CUSTOMER. If both feed one enquiry and one local field, say so as a requirement. | — | | |

## Traceability

Each `Vxx` appears in three places and must stay consistent:

1. `docs/DECISIONS.md` — this table
2. `src/vop_enquiry_model_2026_09_09.py` — raised as `OpenDecisionError("Vxx", ...)`
3. `tests/test_acceptance_vop_2026_09_09.py` — asserted, or skipped with the id in the reason

```bash
grep -rn "V07" src/ tests/ docs/
```

# Handover — VoP functional analysis

Read this page. Nothing else is required to hand the work on.

## What this is

A worked example of functional analysis, end to end, on one real change:
verification of payee in T24 under Regulation (EU) 2024/886.

It shows the whole chain in one folder:

    transcript  ->  concept  ->  numbered rules  ->  open decisions  ->  acceptance tests

The point of the example is not the VoP rules. It is the chain. The same four
steps work for any FSD. What makes it a specification rather than a document is
that every claim has an id, and every id has something that can refute it.

## Five minutes

1. Open `UBB_VoP_Handover_2026-09-09.html` in a browser. It is one file, no
   install, nothing stored. Arrow keys move. On the fourth page, click a row
   and press a button — the rules run live.
2. Open `docs/DECISIONS.md`. Thirteen open questions. All blank on purpose.
3. Run the check below. It proves the rules behave as written.

## The check

Windows:

    check.cmd

macOS or Linux:

    ./check.sh

Expected, every time:

    All checks passed!
    16 passed, 5 skipped

The five skips are not failures. Each is an acceptance scenario blocked on a
decision nobody has made yet, and the skip message names which one. Progress on
this folder is measured in skips remaining, not lines added.

## What sits where

| Path | What it is | Who touches it |
| --- | --- | --- |
| `UBB_VoP_Handover_2026-09-09.html` | The deck. Bulgarian. Live enquiry simulator. | Present it. Rarely edit. |
| `docs/DECISIONS.md` | V01–V13, all open | BA and PM, in a meeting |
| `docs/decisions/` | One answered decision, one file | BA, after the meeting |
| `src/vop_enquiry_model_2026_09_09.py` | The rules R02–R09 as running code | Developer |
| `tests/test_acceptance_vop_2026_09_09.py` | AC01–AC16, test name carries the id | Developer, tester |
| `EDITING.md` | How to change this without breaking it | Everyone, before editing |
| `.github/copilot-instructions.md` | Rules Copilot follows automatically | Nobody edits by hand |
| `prompts/` | Paste-ready tasks for Copilot | Anyone driving the agent |

## Status

Working concept, 2026-09-09. Not an approved FSD. Describes no verified
implementation. No test has been run against a banking system. Statements about
implementation are interpretation. The concurrency, session-durability and
retry recommendations were added during analysis and were not decided in the
original conversation.

Names of staff, ticket keys and internal hosts are not carried over. Technical
detail is written as in the source: Borica, the FUNDS.TRANSFER version names,
Ben. Customer 1, BG.NAME, the sector values.

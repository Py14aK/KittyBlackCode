# FA handover — 2026-09-11

Three folders. One worked example of functional analysis, handed over three
different ways: to an agent, to a person, and to a deriver.

Open `fa_handover_human-to-human/00_START_HERE.md` first. Five minutes.

| Folder | What it holds | Who opens it |
| --- | --- | --- |
| `vop_verification-of-payee/` | The work itself: deck, rules as code, AC01–AC16, 13 open decisions | everyone |
| `fa_handover_human-to-human/` | Passing it to a person: Zoom runbook, Teams post, glossary, Excel tracker | receiver, PM, BA |
| `fa_copilot_derive/` | Atomised BRD, FSD §8 and T24, triangulated into a test backlog | BA, developer |

## Prove it works, in one minute

    cd vop_verification-of-payee && check.cmd          (Windows)
    cd vop_verification-of-payee && ./check.sh         (macOS, Linux)

Expected `All checks passed!` and `16 passed, 5 skipped`.

    cd fa_copilot_derive/src && python run_derive_2026_09_11.py
    cd fa_copilot_derive && python -m pytest -q        # 15 passed

## Where things live once unpacked

**Unzip the readable layer into the Teams channel's Files tab.** That tab is a
SharePoint library — same store, one upload. M365 Copilot cannot see inside a
zip, so a folder left zipped there is invisible to it.

**Put the runnable layer in git.** SharePoint executes nothing and the `.py`
files may be blocked by tenant policy anyway.

This zip is transport, not storage. See
`fa_handover_human-to-human/02_SHAREPOINT_TEAMS.md`.

## Status

Working concept. Not an approved FSD. No test has been run against a banking
system, which is why the atom set contains zero T24 observations and every
subject is unverified.

Names of staff, ticket keys and internal hosts are not carried over. Technical
detail is written as in the source.

## The one thing to take away

Every claim gets an id. Every id gets something that can refute it. A
requirement without an id cannot be traced; an id without a test cannot be
refuted; a claim that cannot be refuted is a wish, not a requirement.

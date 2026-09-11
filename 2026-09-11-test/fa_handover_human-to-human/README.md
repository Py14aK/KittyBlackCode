# Human-to-human handover

A worked example of passing functional-analysis work between people, using the
VoP folder next door as the payload.

The agent-driven handover lives in `vop_verification-of-payee/` — `HANDOVER.md`,
`.github/copilot-instructions.md`, `prompts/`. This folder is the other half:
what a person says to another person, in a room, over a call.

Written in Bulgarian because the session is in Bulgarian.

| File | For whom |
| --- | --- |
| `00_START_HERE.md` | The person receiving the work |
| `01_ZOOM.md` | Whoever runs the live session, 40 minutes |
| `02_SHAREPOINT_TEAMS.md` | Whoever stores it — what SharePoint breaks |
| `03_TASK_CARD.md` | The stripped task-only card passed onward |
| `04_GLOSSARY.md` | Anyone seeing this kind of work for the first time |
| `05_CONFIRM.md` | The receiver, two days later, filled in alone |
| `06_TEAMS_POST.md` | The one channel message, ready to paste |
| `VoP_tracker_2026-09-11.xlsx` | Decisions and atoms, co-edited in the Teams tab |

## The idea

Two layers, on purpose. The receiver gets context, the glossary and the live
session. The next person down gets `03` and nothing else — task, artifact,
definition of done, four blocking questions. If they need more, `00` is there;
it is not pushed at them.

A handover is complete when someone else does the thing unaided, not when they
nod. `05` is the instrument that tests it, and it is filled in by the receiver,
not the sender.

## Assumed

Live session on Zoom. Readable layer unzipped in the Teams channel's Files tab,
which is the same thing as a SharePoint library. Runnable layer in git.

Two tiers on purpose: M365 Copilot cannot see inside a zip and SharePoint runs
no code, so the docs live unzipped where people and Copilot can reach them, and
the code lives in git where it can actually execute. The zip is transport only.

Decisions are co-edited in the Excel tab rather than posted in chat. A decision
answered in a chat message looks like progress and is gone after two weeks of
scrolling.

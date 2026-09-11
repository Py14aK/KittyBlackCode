# Prompts — M365 Copilot, over SharePoint and Teams

Different machine, different limits. M365 Copilot reads what is in SharePoint,
Teams and Outlook. It **cannot run code**, cannot see inside a zip, and cannot
execute the deriver. So nothing here asks it to compute a verdict.

It is good at retrieval across the tenant, at drafting, and at finding the
thing somebody said in March. Use it for that and nothing more.

Prerequisite: the folder is **unzipped** in the channel's Files tab. Zipped,
Copilot is blind to all of it.

---

## Find the source for an unsourced rule

> In the FA - Verification of Payee folder and in this channel's history,
> find anything that states whether rows already carrying an FT should remain
> visible in the enquiry, or whether exactly one empty final row should always
> be present. Quote the source and give me the document and date. If nothing
> states it, say so plainly rather than inferring it from context.

Why: four solution claims currently have no BRD source. Either the source
exists somewhere in the tenant, or those rules need contracting.

---

## Recover a decision that was taken in a meeting and never written down

> Search this channel and my Teams meetings from the last three months for any
> discussion of how long a payee verification stays valid before a transfer,
> or which check results permit a payment to proceed. Give me who said it,
> when, and the exact wording. Do not summarise several people into one
> position.

Why: V07 is the heaviest open question and it was never raised in the
transcripts we have.

---

## Prepare the decision meeting

> From the Decisions sheet in VoP_tracker_2026-09-11.xlsx, list the rows where
> Status is OPEN and the Blocks column is not empty. For each, name the team
> most likely to own it based on the subject matter, and draft one question to
> put to that team. One sentence per question. Do not propose answers.

Why: the machine can prepare the question. It must not prepare the answer.

---

## Check the upload survived

> List every file in the FA - Verification of Payee folder with its size and
> last modified date, as a table.

Compare against MANIFEST.sha256 in the repo. A missing file means SharePoint
dropped it on upload.

---

## What not to ask it

Do not ask it to fill in a decision, to judge whether the system meets the BRD,
or to produce a verdict from the atoms. It has not run anything and cannot.
Its confident tone on those questions is the most expensive thing in this
folder.

Verdicts come from `src/run_derive_2026_09_11.py`, on a machine, from atoms
with anchors.

---
name: ubb-fsd-rewrite
description: Rewrite UBB Temenos T24 FSD and BRD Word/Excel packs into one folder per FSD ID with atomic requirements and vertical task cards. Trigger on FSD rewrite, BRD to cards, VoP local-ref mapping, UBBPMINTL, pack 15/16, GPT-5.6 Sol Copilot agent, or vertical card pivot. Do not use for generic Jira daily mail or physics packs.
metadata:
  type: workflow
  version: "2026-09-01"
  model: gpt-5.6-sol
---

# UBB FSD Rewrite

Turn a Word FSD and a Word/Excel BRD into seven plain-text artifacts in one folder per FSD ID. Do not write a replacement 30-page FSD. Do not invent T24 field names.

## Load these files when needed

- Owner lock and collisions — [references/owners.md](references/owners.md)
- Card grammar — [references/card-format.md](references/card-format.md)
- Copilot Sol paste pack — [references/copilot-sol.md](references/copilot-sol.md)
- Empty seven-file set — [assets/folder-template/](assets/folder-template/)

## Hard rules

- Identifier lock from KittyBlackCode packs 01, 02, 11. BENEF.ID stays BENEF.ID.
- Fail if output contains FIELD_1_NAME, BEN.NAME.CYR, VOP.RESP.STAT, VOP.TIMEOUT.FLG, VOP.RETRY.REQ, L.RTN.RSN.CD unless that exact token is in the user-supplied catalog.
- One FSD ID per run. Do not open a second product folder to be helpful.
- No catalog slice in the turn means every FIELD is UNMATCHED.
- TSC-17855 is Direct Debits and also claimed by Cash Management. Write COLLISION. Do not pick a winner.
- Do not claim a file write, Jira update, or git push unless a tool result in this turn shows it.
- Ignore Gemini architectural blueprints.

## Process

1. Read FSD_ID from the user. If missing, ask once.
2. Write 01_SOURCE from filenames actually present. Do not summarise the whole Word file yet.
3. Fill 02_EPIC from [references/owners.md](references/owners.md) unless the user pasted a newer table.
4. Split shall/must/should that belong to this FSD ID into 03_BRD_ATOMS.
5. Split behaviours into 04_FSD_ATOMS with actor and exact version string.
6. Emit 05_CARDS using [references/card-format.md](references/card-format.md).
7. List gaps in 06_GAPS. Lists only in 07_SPRINT.

Scaffold a folder with:

```bash
bash scripts/scaffold_fsd.sh FSD_ID slug outdir
```

## Output when files cannot be written

Print seven blocks starting with === FILE: 00_INDEX.txt ===

No sentence before WORKFLOW inside 05_CARDS.

## Copilot

If the user says Copilot or Sol, load [references/copilot-sol.md](references/copilot-sol.md) and tell them to pick GPT-5.6 Sol, reasoning max, not Free/Luna/Terra.

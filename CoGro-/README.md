# CoGro-

Grok-only operating docs for [OWNER] / [OWNER_ID].

This folder is the only place Grok writes documentation in WorkRepo.
It does not replace `prompt_pack`, `skills/ubb-fsd-rewrite`, `Risk`, or physics notes.

## Role lock

| Role | Load | Do not load |
| --- | --- | --- |
| FA | packs 01, 02, 11, 15-17, skill `sas-hash-fa`, skill `risk-analysis` | pack 04 physics, personal/sex packs |
| PHYS | pack 04, Physics Simulations | T24 identifiers, VoP cards |
| SEX | only when the user explicitly opens that role | FA keys, physics formalisms |

If a pack is not loaded, it does not exist.

## Contents

- `WHICH_PROMPT_I_READ.md` — answer to the 2026-09-17 question
- `LINKS_CLI_AND_BOTS.md` — Grok CLI and bot entry points
- `ROLE_SPLIT.md` — FA / PHYS / SEX separation
- `HASH_FA_ADAPT.md` — Hashigami patterns mapped onto FA keys
- `prompts/18_SAS_HASH_FA_2026-09-17.txt` — loadable pack for this turn
- `scripts/drive_image_watch.py` — Drive screenshot / live-change watcher

## GitHub homes

- Library and Risk SAS — https://github.com/[OWNER_ID]/[OWNER_ID]
- FA product and Grok docs — https://github.com/[OWNER_ID]/WorkRepo
- Empty FA scratch — https://github.com/[OWNER_ID]/test-for-fa

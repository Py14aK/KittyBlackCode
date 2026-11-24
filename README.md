# KittyBlackCode v2

A functional analyst's toolkit for Temenos T24 delivery, set up to work with Claude.

## What is here

| Path | What it is | Status |
|---|---|---|
| `plugins/kitty-fa/` | Claude plugin with 15 skills | ready |
| `plugins/kitty-fa/skills/pm-*` | 8 product-management skills (Anthropic, Apache-2.0), each with an FA/T24 overlay | ready |
| `plugins/kitty-fa/skills/t24-pw-*` | 6 Playwright skills: calibrate, xray-to-spec, ft-flow, field-rules, msg-check, triage | ready |
| `plugins/kitty-fa/skills/copilot-relay` | one-way instruction packets for free Copilot on the closed network | ready |
| `playwright-t24/` | runnable Playwright harness plus an offline T24 mock | 17/17 green on the mock, not yet run on a real T24 |
| `tools/public_gate.py` | pre-commit scan for secrets and private terms | ready |
| `prompt_pack/`, `guides/`, `fsd*/`, `skills/`, `2026-09-11-test/` | v1 material | unchanged in v2 |

## Install the skills

Claude Code:
```
/plugin marketplace add Py14aK/KittyBlackCode
/plugin install kitty-fa@kittyblackcode
```
claude.ai: zip one skill folder (for example `plugins/kitty-fa/skills/t24-pw-ft-flow`) and upload it under Settings, Capabilities, Skills.

## Start here

1. `cd playwright-t24 && npm install && T24_TARGET=mock npx playwright test --project=chromium`
2. Read `playwright-t24/README.md`, section "Bring up on SYT".
3. Calibrate the selectors with the `t24-pw-calibrate` skill.
4. Move manual Xray tests in with `t24-pw-xray-to-spec`.

## Skill map

| Need | Skill |
|---|---|
| Spec, sprint, roadmap, status update, metrics | pm-write-spec, pm-sprint-planning, pm-roadmap-update, pm-stakeholder-update, pm-metrics-review |
| Make sense of UAT feedback | pm-synthesize-research |
| Fit the harness to a real T24 release | t24-pw-calibrate |
| Turn manual tests into code | t24-pw-xray-to-spec |
| Payment input, authorise, enquiry, services, H table | t24-pw-ft-flow |
| Field limits, mandatory, VAL routines, overrides | t24-pw-field-rules |
| Base64, XML, XSD, routing | t24-pw-msg-check |
| Red run: harness, environment, data or defect | t24-pw-triage |
| Hand work to Copilot inside the closed network | copilot-relay |

Rules for working in this repo with Claude: `CLAUDE.md`.

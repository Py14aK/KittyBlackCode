---
name: t24-pw-triage
description: Triage a failed Playwright T24 run: read the error, error-context.md, trace and screenshots, classify the failure as harness/selector, environment, test data or product defect, and draft the defect or fix with evidence. Also prepares the Xray execution import. Use after any red run.
---
# Failure triage

## Inputs
`reports/html`, `test-results/*/error-context.md`, `trace.zip` (open with `npx playwright show-trace`), `reports/xray_execution_<date>.json`.

## Classify each failure into one class
| Class | Signature | Action |
|---|---|---|
| Selector | element not found, the page snapshot shows the element under another attribute | run t24-pw-calibrate |
| Focus/timing | key pressed and nothing happened, or it passes in click mode and fails in key mode | focus the frame, wait for the new screen |
| Environment | login refused, service down, COB running, record locked | rerun later. Not a defect |
| Data | account closed, limit used up, the date is not the business date | fix the data CSV |
| Product | screen correct, message or value differs from the FSD | draft a defect |

## Defect draft (for Product only)
Title: `<version> <field or step>: <observed> instead of <expected>`. Then steps (from the test.step names), expected (with the FSD reference), observed (the exact message), and evidence (the screenshot file names). Then environment: release, SYT, business date. No names, no credentials.

## Xray
The reporter writes `xray_execution_<date>.json` with PASS/FAIL and screenshots. Server/DC uses `evidences`, Cloud uses `evidence` (set `XRAY_FLAVOUR`). Import it through the Xray import-execution REST endpoint, or hand it to whoever imports. Say it is ASSUMED-format until the first import succeeds.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

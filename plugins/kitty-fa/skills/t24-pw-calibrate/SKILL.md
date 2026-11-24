---
name: t24-pw-calibrate
description: Calibrate the Playwright T24 harness to a real T24 Browser release (R21 or R26): turn codegen output, DOM snippets or screenshots into selector values in profiles.ts. Use when a test fails with 'element not found', when moving from mock to SYT, or when a new release changes screens.
---
# T24 Playwright calibration

Goal: make `profiles.ts` true for one release, one value at a time, with evidence.

## Inputs
- Release (R21 or R26) and what the user captured: codegen output, an outerHTML snippet, a screenshot, or a failing test's `error-context.md`.

## Steps
1. List which profile keys the captured material covers. Keys: login.*, frames.*, commandLine, commandGo, signOff, field(), toolbar.*, keys.*, messages.*, completeRe, recordStatus, enquiry.*, services.*.
2. For each covered key, propose the new value. Prefer stable attributes: `name`, `id`, `title`, then role/text. Never use nth-child chains or generated ids that change per session.
3. Frames: decide whether the element is in an iframe, a frameset `frame`, or a popup window. A popup needs `page.waitForEvent('popup')` in session.ts. Say so explicitly. Do not force it into frameLocator.
4. Edit only the release's profile object. Replace the ASSUMED comment with `// verified <release> <date> via <codegen|snippet>`.
5. Give the one-test command that proves the change: `npx playwright test -g TKT-00003 --project=edge`.
6. Keep a table in the reply: key, old, new, evidence, status (verified / still ASSUMED).

## Kata
Locator ladder: id or name, then title, then role plus name, then visible text. Write down why each rung was rejected before you use a lower one.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

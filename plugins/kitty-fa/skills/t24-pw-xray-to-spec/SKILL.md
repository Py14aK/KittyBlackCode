---
name: t24-pw-xray-to-spec
description: Turn Jira Xray manual tests (Test Case Importer CSV, TCID;Test Summary;...;Action;Data;Result) into Playwright specs for the T24 harness, and close the unmapped steps. Use when the user has Xray tests, a test CSV, or asks to automate existing manual test cases.
---
# Xray CSV to Playwright spec

## Steps
1. Check the header is exactly `TCID;Test Summary;Test Priority;Component;Action;Data;Result`, semicolon, UTF-8. If it is not, stop and show the diff. The generator refuses bad headers on purpose.
2. Run: `python tools/xray2spec.py data/cases/<file>.csv --fieldmap data/fieldmap.csv` (from `playwright-t24/`).
3. Read the coverage table. Every FIXME line is a step the generator did not understand.
4. Close each FIXME by the cheapest fix, in this order:
   a. Add a phrase to `data/fieldmap.csv` (phrase;FIELD), e.g. `payer;DEBIT.ACCT.NO`.
   b. Reword the Xray step to the house grammar: "Enter the <field phrase>", "Press Validate", "Type the <x> command and press Go", "The banner is <text>", "<field phrase> shows <value>".
   c. Only then, hand-edit the generated spec, and move it out of `tests/generated/` so regeneration does not overwrite it.
5. Regenerate. Run against the mock if the flow exists there, otherwise `--project=edge` on SYT.
6. A generated test with `test.fixme` is skipped, never green. Report it as not automated.

## House grammar for new manual tests
One action per row. Data holds exactly the typed value. Result is one observable sentence. Writing tests this way makes them both importable and generatable.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

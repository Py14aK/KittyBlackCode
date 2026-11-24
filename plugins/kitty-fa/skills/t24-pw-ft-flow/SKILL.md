---
name: t24-pw-ft-flow
description: Write or extend an end-to-end Playwright test for a T24 funds transfer: input as inputter, validate, overrides, commit, capture FT id, authorise as second user, check TXN.ENTRY, TS services, H table and outgoing XML. Use for outgoing or incoming payment flows, new FT versions, or SEPA/SWIFT/CBPR routing checks.
---
# FT end-to-end flow

Model: `playwright-t24/tests/ft-outgoing-e2e.spec.ts`. Copy its shape. Do not start from scratch.

## Flow skeleton
1. `t24.login(inputter)` then `ft.input({...})`. Order: DEBIT.ACCT.NO, then CREDIT.CURRENCY, then the rest. Assert no errors and capture the id.
2. Read the record back with `ft.open('S', id)` and assert the enriched fields (debit currency, vostro credit account).
3. Four-eyes negative: the inputter tries to authorise and gets the same-user error.
4. `t24.logout()`, `t24.login(authoriser)`, `ft.authorise(id)`, then `ft.status(id) === 'AUTH'`.
5. `enq.run('TXN.ENTRY', {...})`: both legs present, the amount matches.
6. `ts.ensure(service, 'START')`, then the H table enquiry shows the record, then decode the payload with `b64decode`, `parseXml` and assert EndToEndId, amount, currency and creditor name. For a full schema check, use `tools/xsd_check.py`.
7. `t24.evidence()` after each step that a human would screenshot.

## Rules
- Version name comes from `T24_FT_VERSION` or the test data, never hard-coded in two places.
- Use a test.step per business step so the HTML report and the Xray evidence read like the manual test.
- A negative path (service stopped, wrong currency, override refused) gets its own test, tagged with its own key.
- Use the T24 business date from `T24_TODAY`, not the wall clock.
- Incoming flows: start from the H table or the inbound queue and work backwards. Say which inbound injection method is used, because it is environment specific.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

# playwright-t24

Playwright harness for Temenos T24 Browser functional tests (R21 and R26), built for a closed test environment where the only AI is free Copilot and the FA runs the tests.

Status 2026-10-28: 17 of 17 tests green against the offline mock, in both click mode and F-key mode. Nothing has run against a real T24 yet. Every real-screen selector is marked ASSUMED in `src/t24/profiles.ts` until you calibrate it.

## Layout

```
src/t24/profiles.ts     selectors per release. The ONLY file to edit when a screen differs
src/t24/session.ts      T24 class: login, command line, fields, validate/commit, overrides, evidence
src/pages/              FtPaymentPage (input/authorise/see), EnquiryPage, ServicesPage (TS)
src/util/codec.ts       UTF-8 base64, XML parse with position errors, dotted path get
src/util/csv.ts         semicolon CSV reader (Xray convention)
src/util/xray-reporter.ts  run -> reports/xray_execution_<date>.json with screenshots as evidence
tests/                  e2e FT flow, field-rule matrix (CSV driven), enquiry, codec unit tests
tests/generated/        specs written by tools/xray2spec.py
data/cases/             test data as CSV. Add rows, not code
tools/xray2spec.py      Xray importer CSV -> spec skeletons. Unknown steps force test.fixme
tools/xsd_check.py      validate XML or base64 payloads against the scheme XSD (lxml)
mock/                   offline T24 look-alike: frames, command line, FT, enquiry, TS, H table, XML
```

## Run on the mock (any machine)

```
npm install
T24_TARGET=mock npx playwright test --project=chromium
T24_TARGET=mock T24_PREFER_KEYS=1 npx playwright test --project=chromium
npx playwright show-report reports/html
python tools/xray2spec.py --selftest
python tools/xsd_check.py --selftest
```

Windows PowerShell: `$env:T24_TARGET="mock"; npx playwright test --project=chromium`

## Bring up on SYT (closed network)

1. Edge is already there, so use `--project=edge` (channel msedge). No browser download is needed.
2. Packages: on a connected machine run `npm ci`, zip `node_modules`, carry it in through the approved channel. Or ask IT to mirror `@playwright/test` and `fast-xml-parser` in the internal registry.
3. `cp .env.example .env` and fill in the URL and the test users. `.env` is git-ignored. Never put credentials in code, CSV or prompts.
4. Calibrate the selectors: `npx playwright codegen --channel=msedge --ignore-https-errors <SYT url>`. Click through login, the command line, one FT field, Validate, Commit and an enquiry. Copy each locator codegen shows into the R21 (or R26) profile and delete its ASSUMED note.
5. Run one test first: `npx playwright test -g TKT-00003 --project=edge`. Widen only when it is green.

## Things learned on the mock that will matter on the real screen

- **F-keys go to the focused frame.** After a command, focus sits in the banner frame (the command line). An F-key pressed "on the page" is silently lost. `T24.act()` moves focus into the work frame first. Found by the F-key run failing only on the authorise screen.
- **Wait for the new screen before pressing a key.** A click waits for its own button to appear. A key press does not, so it can land on the previous document. `FtPaymentPage.authorise()` waits for the record status first.
- **Order of input matters.** Enter DEBIT.ACCT.NO, then CREDIT.CURRENCY, then the rest. Each `set()` tabs out of the field, so enrichment routines fire the way they do for a human.
- **Overrides are never auto-accepted** unless the test says so. Errors are never accepted.
- **No retries.** A flaky T24 test is a finding, not something to hide.

## Mock behaviour (invented, not Temenos)

The rules below are mock rules. They are there to exercise the harness, and the real rules come from the FSD. BENEF.NAME has a maximum of 35 characters. An amount over 10000 raises an override. Debit and credit amount are mutually exclusive. The vostro account autoloads by currency. The inputter cannot authorise their own record. The H table shows SENT with a base64 pacs.008 only when `BNK.H.TRANSFER` is started. The keymap is F5 validate, F2 commit, F9 authorise.

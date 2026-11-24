---
name: t24-pw-field-rules
description: Derive a data-driven validation matrix for a T24 version (mandatory fields, max length, mutually exclusive fields, formats, overrides vs errors) from FSD/BRD atoms, as a CSV the Playwright harness runs. Use when testing VAL routines, new local fields, field limits, or stress/boundary cases.
---
# Field-rule matrix

Output: rows appended to `playwright-t24/data/cases/<version>_field_rules.csv`, run by `tests/ft-field-rules.spec.ts` (or a copy for another version).

## Steps
1. List the rules from the FSD atoms, one per line, with the source grade SPEC / OBSERVED / ASSUMED.
2. For each rule, generate cases by technique:
   - Max length L: L-1, L, L+1. Also multibyte characters at L (Cyrillic), because byte limits and character limits differ.
   - Mandatory: empty, whitespace only.
   - Mutually exclusive A/B: A only, B only, both, neither.
   - Numeric: 0, negative, too many decimals, the limit exactly, the limit plus the smallest unit.
   - Override threshold: at the limit gives no override; above it gives an override, and the test refuses it (it is not an error).
3. Expect column: complete | error | override. Contains column: the shortest stable substring of the T24 message. Never the full text, because messages differ by language and release.
4. One TCID per row. Pairwise-reduce when there are more than about 30 rows. Keep every boundary row and cut only the interior combinations.
5. State what the matrix does NOT cover (cross-field routines, enrichment timing, authorise-time checks).

## Kata
Equivalence classes plus boundaries. For each rule, write the classes first, then pick one representative inside each class and every edge between classes.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

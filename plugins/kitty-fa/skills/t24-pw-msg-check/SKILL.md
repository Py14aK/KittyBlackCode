---
name: t24-pw-msg-check
description: Check payment messages produced by T24: decode base64, parse XML, validate against ISO 20022 XSD (pacs.008, pacs.009, camt), compare fields to the FT record, and verify routing/rerouting to the right service or queue. Use when a test must prove the outgoing or incoming message is correct.
---
# Message checks

## Tools
- In tests: `b64encode`, `b64decode`, `parseXml`, `get` from `playwright-t24/src/util/codec.ts`.
- Out of band: `python tools/xsd_check.py <scheme.xsd> msg.xml` or `--b64 "<payload>"`. The XSD comes from the scheme pack on SYT, never from the internet.

## Steps
1. Get the payload. In an enquiry cell or attribute, read it with `enq.cellData(row, col, attr)`. If it is a download, use `page.waitForEvent('download')`.
2. Decode the base64 as UTF-8. Check that Cyrillic survives (round trip in `codec.unit.spec.ts`).
3. Parse. A malformed message fails with line:col.
4. Field mapping table, FT field to XML path. EndToEndId, IntrBkSttlmAmt plus @Ccy, Dbtr/Cdtr Nm, accounts, charge bearer. Assert each one, and attach the XML to the report.
5. XSD validate the same payload. A test that only parses is not a schema check. Say which one was done.
6. Routing: assert which service or H table received it and that the others did not. For rerouting, flip the routing parameter, rerun, and assert the move.

## Notes
- Amounts parse as numbers in fast-xml-parser (250.00 becomes 250). Compare numerically, or set parseTagValue false when the exact decimal string matters.

## Ground rules (all t24-pw-* skills)

- The harness lives in `playwright-t24/`. Reuse `T24`, the page objects and the CSV utilities. Do not write a second login, a second command-line helper or a second CSV reader.
- Selectors live only in `playwright-t24/src/t24/profiles.ts`. A test file never contains a raw CSS selector for a T24 element.
- T24 field, version, enquiry and service names are copied verbatim (DEBIT.ACCT.NO, FT,VERSION.NAME, ENQ TXN.ENTRY). Never rename or translate them. A name you have not seen in the user's material is written as UNMATCHED and asked about.
- Credentials come from `.env` only. Never write a user id or password into code, CSV, prompts, commit messages or chat output, even when the user pastes one. If one is pasted, say it should be rotated.
- No employer names, real customer data, ticket keys or colleague names in anything committed. Use BNK, role codes (FA1, QA1) and TKT-00000-style keys.
- State what was executed. "Green on mock" and "green on SYT" are different claims. Never report a run you did not see.

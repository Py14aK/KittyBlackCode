# KittyBlackCode v2: working rules for Claude

This repo holds a functional analyst's T24 toolkit: skills in `plugins/kitty-fa`, the runnable Playwright harness in `playwright-t24`, and v1 material (prompt packs, FSD rewrites, guides).

## Hard rules
- Public-safe content only. No employer or bank names (use BNK), no colleague names (use FA1, PM1, QA1), no real ticket keys (TKT-00000), no customer data, no credentials. Run the gate below before every commit.
- T24 identifiers are verbatim: field, version, enquiry and service names keep their exact spelling and punctuation.
- Selectors for T24 screens live only in `playwright-t24/src/t24/profiles.ts`.
- Reuse before writing: `T24` session, page objects, `codec.ts`, `csv.ts`, `xray2spec.py`, `xsd_check.py`.
- Filenames for new dated artifacts end in `_YYYY-MM-DD`.
- Say what was executed and where (mock or SYT). Never report an unseen run.

## Check before commit
```
cd playwright-t24 && npx tsc --noEmit -p . && T24_TARGET=mock npx playwright test --project=chromium
python tools/xray2spec.py --selftest && python tools/xsd_check.py --selftest
cd .. && python3 tools/public_gate.py --staged
```

## Where things go
- New skill: `plugins/kitty-fa/skills/<name>/SKILL.md`. Use the t24-pw- prefix for automation and pm- for planning.
- New test data: `playwright-t24/data/cases/*.csv`, never inline arrays in specs.
- New T24 flow: page object in `src/pages`, test in `tests`, a mock route in `mock/work.html` only if needed for the self-test.

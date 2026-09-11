# Prompt — review before handing on

---

Audit this folder for broken traceability. Report only findings, change nothing.

1. **Orphan decisions.** Any `Vxx` in `docs/DECISIONS.md` that appears in
   neither `src/` nor `tests/`.
2. **Orphan raises.** Any `OpenDecisionError` id with no row in
   `docs/DECISIONS.md`.
3. **Orphan scenarios.** Any `ACxx` in the deck's scenario table with no test,
   or any test id missing from the deck.
4. **Fake progress.** Any test that was un-skipped while its decision is still
   blank in `docs/DECISIONS.md`.
5. **Answered in code.** Any branch that resolves an open `Vxx` without an ADR.
   Check `ADMISSIBLE` specifically.
6. **Encoding damage.** Any Cyrillic rendered as mojibake.

For each finding: the id, the file, the line, and the single smallest change
that would repair the link.

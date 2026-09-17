# Prompt — a decision has been answered

Use this only after a real answer exists, with an owner and a date.

---

Decision **V__** has been answered by the team:

> <paste the answer, the owner and the date>

Apply it, in this order, and stop if any step cannot be done cleanly:

1. Write `docs/decisions/ADR-000N-<slug>.md` with Context, Decision and
   Consequences. Date it. Record any earlier reading it supersedes.
2. Replace the row in `docs/DECISIONS.md` with a link to that ADR.
3. Update `src/` so the branch is implemented instead of raising
   `OpenDecisionError` for this id.
4. Convert the matching skipped test into a real test with the now-known
   expectation. Keep the `ACxx` id exactly as it is.
5. Update the deck: the scenario table row, and the decision list in the
   script near the bottom of the HTML.

Then run `ruff check .` and `python -m pytest -q` and paste both outputs. The
skip count must drop by exactly the number of scenarios this decision unblocked
and by no more.

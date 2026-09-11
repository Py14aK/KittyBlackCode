# Repository instructions

This folder is a functional-analysis specification, not application code. The
value is the traceability between four artifacts, not the lines of Python.
Copilot reads this file automatically in VS Code and on github.com.

## What you are working on

    docs/DECISIONS.md       V01-V13, business questions, all deliberately open
    src/...model....py      rules R02-R09 as executable code
    tests/...acceptance...  AC01-AC16, test name carries the scenario id
    *.html                  the deck people read

## Hard rules

1. **Never fill in an answer in `docs/DECISIONS.md`.** Those are business
   decisions taken by people in a meeting. Draft options if asked, in the chat,
   not in the file.
2. **Never delete or un-skip a test to make the suite pass.** Five tests are
   skipped because the decision that would define their expectation has not
   been made. The skip reason names the decision. Removing a skip fakes
   progress.
3. **Never add `NMTC` or `NOAP` to `ADMISSIBLE`.** That answers V07 in code.
   V07 is a regulatory question about which check results permit a payment.
4. **Never rename a test.** The `ACxx` prefix is the traceability handle.
   Adding words after the id is fine; touching the id is not.
5. **Never rename the Python modules to hyphenated dates.** Hyphens are invalid
   in module names. Deliverables use `2026-09-09`, modules use underscores.
6. **Preserve UTF-8.** Bulgarian text and Cyrillic fixtures throughout.

## When adding something

A new rule needs all three: the row in `docs/DECISIONS.md` if it is an open
question, the behaviour in the model, and a test whose name carries the id.
Two out of three is worse than none, because it looks complete.

For an undecided branch, raise `OpenDecisionError("Vxx", "...")` rather than
picking a default. Guessing quietly is the failure this folder exists to
prevent.

## Before you report done

Run and paste the output:

    ruff check .
    python -m pytest -q

Expected: `All checks passed!` and `16 passed, 5 skipped`. If the skip count
dropped and no decision was answered in `docs/DECISIONS.md`, you broke rule 2.

## Style

Comments and docstrings explain *why*, since the *what* is readable. Prose in
the deck is Bulgarian: short declarative sentences, concrete nouns, no
ornament. Match it.

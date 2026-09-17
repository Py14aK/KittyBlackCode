# How to edit this without destroying it

The folder holds together because of three links. Break a link and the folder
still runs, still looks fine, and is no longer a specification. That is the
failure mode to guard against — not a crash, a quiet loss of meaning.

## The three links

**1. Every `Vxx` exists in three places.**

    docs/DECISIONS.md                     the row that states the question
    src/...model....py                    raise OpenDecisionError("Vxx", ...)
    tests/...acceptance....py             asserted, or skipped with Vxx named

Check any one of them:

    findstr /s /n "V07" src\*.py tests\*.py docs\*.md      (Windows)
    grep -rn "V07" src/ tests/ docs/                        (macOS, Linux)

Three or more hits, consistent. Fewer means a link is cut.

**2. Every test name carries its scenario id.** `test_AC05_...`. The id is the
handle the whole chain hangs from. Rename freely after the id; never remove or
renumber the id itself.

**3. Every rule id `Rxx` in the model appears in the deck.** The deck is the
version people read; the model is the version that can be wrong.

## Safe to change

- Wording, anywhere. Bulgarian prose, docstrings, comments, table text.
- Adding an acceptance test. Give it the next free `ACxx` and add the row to
  the deck's scenario table.
- Adding a decision. Next free `Vxx`, and the same in all three places.
- Styling in the deck. It is one file with no build step.

## Not safe

- **Deleting a skip to make the suite look greener.** A skip is a recorded open
  question. A suite of sixteen greens and no skips would mean somebody guessed
  five business decisions. Convert a skip into a real test only after the
  matching `Vxx` has an answer written in `docs/DECISIONS.md` with an owner and
  a date.
- **Widening `ADMISSIBLE`** in the model. Today it is `{"MTCH"}`. Adding
  `NMTC` or `NOAP` is answering V07 in code, silently, and V07 is the heaviest
  regulatory question in the folder. It needs an ADR first.
- **Filling in `docs/DECISIONS.md` with an AI.** Prose describing a decision is
  not a decision. An assistant-filled form is worse than a blank one because it
  looks settled.
- **Renaming the Python files to match the `2026-09-09` convention.** Hyphens
  are invalid in Python module names. Deliverables carry hyphenated dates;
  modules carry underscores. This asymmetry is deliberate.
- **Reformatting the deck** with a prettifier or pasting it through Word. It is
  hand-written single-file HTML with inline SVG and no build.

## Encoding

Everything is UTF-8. The deck and the docs are Bulgarian; the model uses
Cyrillic in test fixtures. Editing through Windows Notepad in ANSI, or opening
a file in Excel and saving it back, will corrupt Cyrillic and you may not
notice for weeks. Use VS Code. If a Cyrillic character shows as `?` or `Ð`,
close without saving.

## Before you commit

    check.cmd            (Windows)
    ./check.sh           (macOS, Linux)

Green, or do not commit. If `ruff` complains about your edit, it is usually
right; read the message before disabling the rule.

## If you think a rule is wrong

Good. That is what the model is for. Change the model, run the check, and let a
test fail. A failing test is the cheapest possible argument. Then either the
test was wrong and you fix it with a note, or the rule was wrong and you have
just found a defect before it reached development.

Do not fix the failure by deleting the test.

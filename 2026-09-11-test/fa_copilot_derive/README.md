# FA Copilot — derivation layer

Documents are prose. Prose cannot be joined, diffed or counted. Atomise them
and all three become queryable, and test cases fall out of where they disagree.

The pilot decides. The suit carries the load and shows where the sources fail
to line up.

## The three sources are not equal

| Source | Status | What it can prove |
| --- | --- | --- |
| `BRD` | **fact** — contracted, testable, delivered to us | what *must* be true |
| `FSD_S8` | **claim** — section 8, Solution | what we *say* we will do |
| `T24` | **empirical** — observed behaviour | what *is* |

A claim is not a fact. An observation is not a requirement. Collapsing the
three is the mistake the whole module exists to prevent.

## The matrix

| BRD | Claim | T24 | Verdict | Meaning |
| :-: | :-: | :-: | --- | --- |
| ✓ | ✓ | ✗ | `DEFECT` | Required and claimed; system does otherwise |
| ✓ | — | — | `SPEC_GAP` | Contracted, nothing in the solution. **No test emitted.** |
| ✓ | ≠ | — | `CLAIM_DRIFT` | Requirement and solution disagree, on paper |
| ✓ | ≠ | ✓ | `CLAIM_WRONG` | System meets the BRD; the FSD describes something else |
| ✓ | ✓ | — | `UNVERIFIED` | Required and claimed, never observed — the UAT backlog |
| — | — | ✓ | `UNDOCUMENTED` | Behaviour nobody wrote down |
| — | ✓ | — | `GOLD_PLATING` | Claimed, required by nobody |
| ✓ | ✓ | ✓ | `CONFIRMED` | Lock it with a regression test |

Sorted contradictions first, absences second, agreements last.

**A `SPEC_GAP` deliberately produces no test case.** Writing a test for a
requirement with no solution means inventing the expectation, and an invented
expectation is the quietest way to ship the wrong thing.

## Run it

    cd src && python run_derive_2026_09_11.py
    python -m pytest -q        # 15 passed

## What the shipped set says today

31 atoms: 16 from the BRD, 15 solution claims, **zero** T24 observations,
because nothing has been run against a banking system.

    5  SPEC_GAP     blocking
    1  CLAIM_DRIFT  blocking
    10 UNVERIFIED
    4  GOLD_PLATING

All five spec gaps sit in the internal-payments branch: the commit printout,
the FT audit field, the Yes/No local field, the sector validation and the
pop-up on No. The concept work solved the two-route enquiry and never
solutioned the internal path. That is a real finding and it was invisible in
prose.

The four gold-plating entries are the two-route rules themselves — row
retention, the last row, the duplicate-FT guard, new identity on regeneration.
They are correct engineering and **no BRD line requires them**. Either find the
source or get them contracted.

The single claim drift is the close-match suggested name: the BRD says it is
returned, the solution says it is returned *and stored*. Storage is an extra
obligation nobody agreed to.

## Adding atoms

One row per atom, tab separated, in `data/`. `subject` is the join key —
atoms sharing a subject are statements about the same thing. `anchor` is where
it came from; an atom without one is rejected, because it cannot be checked.

Two atoms from the same source on the same subject are rejected too: either
the subject is too broad or the atoms should be merged.

## When T24 observations arrive

Add `T24` rows from UAT. Every `UNVERIFIED` collapses into `CONFIRMED`,
`DEFECT` or `CLAIM_WRONG`. That transition is the measure of test progress —
not how many cases were written, but how many subjects stopped being unobserved.

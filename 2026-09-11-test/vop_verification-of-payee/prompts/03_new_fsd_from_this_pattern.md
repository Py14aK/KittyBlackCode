# Prompt — reuse the pattern on a different FSD

This is the transferable part. The VoP content is the example, not the point.

---

Use this folder as the template for a new functional analysis.

Source material: <paste the transcript, the BRD extract, or attach the doc>

Produce the same four artifacts, in this order:

1. **Numbered rules.** Read the source and extract every behavioural claim as
   `R01, R02, ...`. One claim per rule. Mark each: established by the source,
   working interpretation, or your own addition. Do not blur the three.
2. **Open decisions.** Every question the source does not answer becomes
   `V01, V02, ...` in `docs/DECISIONS.md`. Leave every answer blank. Note which
   decisions block which others.
3. **A reference model** in `src/`, pure Python, no network and no core-banking
   client. Implement the rules. Where a rule is undecided, raise
   `OpenDecisionError("Vxx", ...)` instead of choosing a branch.
4. **Acceptance tests** in `tests/`, named `test_ACxx_...`. Scenarios blocked
   on a decision are skipped with that decision named in the reason.

Then run the check and paste the output.

Report at the end: how many rules, how many decisions, how many tests, how many
skips, and which decision blocks the most.

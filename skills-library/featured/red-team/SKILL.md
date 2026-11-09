---
name: red-team
description: Attack a draft before it ships, whether a recommendation, analysis, model, trading or portfolio idea, backtest, plan, spec or document. Produce the strongest case against it, counterexamples, failure regimes, hidden assumptions, numbers that disagree across files, and one alternative from another field, each with the cheapest way to settle it. Use it before any high-stakes deliverable or decision and whenever the user asks to stress-test, poke holes, challenge, review critically or asks what they are missing, even without the words red team. Not for line-by-line review of a code diff.
---

# Red team

Agreement is cheap and errors are expensive. A short adversarial pass before a recommendation or document leaves the user is where most avoidable mistakes get caught.

## Steps

1. Restate the claim or recommendation in one sentence, so the attack targets what was actually said.
2. Strongest case against. Argue the opposite the way a competent critic would, with the best evidence available.
3. Counterexamples and failure regimes. Where does it break: crashes and correlation spikes, small samples, fat tails, regime change, illiquidity, costs and slippage, look-ahead and survivorship bias, data errors.
4. Hidden assumptions. List what has to be true for the conclusion to hold, and mark the ones nobody checked.
5. Consistency. When several files or sections exist, check that the same parameter has the same value everywhere and that numbers in the text match the tables.
6. Cross-domain alternative. One approach from another field that would attack the same problem differently. Prefix it with "mine:" when it is your own idea.

## Report

A ranked list, most damaging first. For each item: the attack, why it matters, and the cheapest test that would settle it. Close with a one-line verdict: holds, holds with fixes, or does not hold. Leave the draft itself alone unless the user asks for a rewrite.

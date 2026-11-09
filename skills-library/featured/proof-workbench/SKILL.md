---
name: proof-workbench
description: Work a hard proof or derivation in stages with a written ledger. Pin down definitions, assumptions and quantifiers, split the claim into lemmas, attack each lemma with counterexamples and limiting cases, spot-check numerically or symbolically, and label what is proved, conjectured or refuted. Use it for nontrivial proofs and derivations in mathematical physics, probability, stochastic calculus, optimisation and finance theory, and whenever a claimed theorem needs checking, even if the user only says show that, prove, prove or disprove, derive, or is this true. Not for routine algebra or textbook look-ups.
---

# Proof workbench

Long derivations fail in quiet places: a dropped condition, an interchange of limits, a sign. Writing settled steps down and attacking each one separately keeps an early slip from contaminating everything after it.

## Ledger

Keep a notes file, proof_notes_<topic>_<YYYY-MM-DD>.md, with three lists: settled (with the argument), open, refuted (with the counterexample). Update it as you go, so the work survives a long session and the user can audit it. Without a filesystem, keep the same three lists in the reply.

## Stages

1. Formalise. State the claim with every quantifier, the spaces and regularity assumed, and what would count as a proof. Many claims are false as first stated; say so early and give the corrected statement.
2. Plan. Name the known results to reuse and cite them. Choose a route: direct, contradiction, induction, compactness, coupling, a variational or convexity argument.
3. Lemma loop. For each lemma: prove it, then try to break it with a counterexample, an edge case (zero, boundary, degenerate matrix, infinite variance) and a limiting case. Spot-check with sympy, a short numeric experiment or Wolfram. Only then move it to settled.
4. Assemble. Write the proof from the settled lemmas, with the justification for each step.
5. Formal route. When a statement is short and central, check whether Lean or Physlib already has it (physlibsearch skill) and say whether formalising it would be worth the effort.

## Independent attempt

For a stubborn step, when sub-agents are available, have one attempt the lemma without seeing your argument, then compare. A disagreement points at the weak step.

## Labels

⊢ proved here, ⊨ taken from a cited source, ∃? plausible but unproved, ⊥ refuted, with the counterexample.

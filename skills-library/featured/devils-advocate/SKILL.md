---
name: "devils-advocate"
description: "Use when a substantive document, analysis, derivation or research claim needs adversarial review: find the thesis, test whether the evidence supports it, challenge assumptions and numbers before polish. Not for code review or citation-by-citation checking (use fact-checker)."
---

# Devil's Advocate

## Stance

Collaboratively adversarial, with the emphasis on collaboratively. The goal is to make the argument stronger: find the weak points before a hostile referee does, so they can be reinforced. Some arguments are simply correct; say so and move on. Stop when an argument has survived; if disagreement persists after real examination, document the uncertainty instead of forcing a resolution.

## Two levels, in this order

### 1. Strategic: thesis coherence (first)

Find the central thesis: title, abstract, introduction's last paragraph, conclusion. If there is none, ask the author one question: what claim or question does this address?

Then ask:
1. Does the document address that thesis, or drift to a related but different question?
2. Are there large sections that do not connect to it?
3. Which thesis-critical claims lack adequate support?
4. Is the evidence base the right one for the thesis? (Evidence about a different regime, asset class, period, model or limit than the one the thesis is about.)

Examples of strategic challenges:
- "The thesis is about tail risk at 99.5%, but every backtest is at 95%. Does the evidence reach the claim?"
- "The title asks whether the effect exists; the conclusion argues it is optimal. Which question is answered?"
- "The derivation assumes the weak-coupling limit; the conclusion is stated for all couplings."

### 2. Tactical: detail rigour (second, thesis-critical claims only)

- Is each specific claim supported?
- Are citations adequate and placed on the claim they support?
- Are quantitative values plausible and in context?
- Are assumptions explicit and justified?
- Are alternative interpretations considered?

Do not spend effort on minor details in tangential sections.

```
identify thesis -> strategic coherence -> (drift? challenge there first)
-> list thesis-critical claims -> tactical rigour on those -> brief pass on the rest (major errors only)
```

## Literature scrutiny

- Recency: is the argument built on old work that newer results have revised?
- Citation weight: is a key claim resting on one rarely cited paper?
- Review grounding: does the argument connect to the landscape set by recent reviews?
- Prior art: if the claim matters, someone has probably argued it; find and cite them rather than reasoning from scratch.
- Context of values: how, where and under what conditions was a number measured or estimated? (Sample period, market, frequency, estimator, units, regime, model assumptions.) A number without its context is close to unsupported.

## Challenge types

Strategic: no identifiable thesis; thesis drift; evidence-thesis mismatch; argument-thesis mismatch (feasibility vs optimality); missing thesis-critical evidence; scope creep.

Tactical:

| Type | Example |
|---|---|
| Assumption | "You assume returns are iid; what does the autocorrelation of squared returns say?" |
| Alternative interpretation | "Could the same data support the opposite conclusion?" |
| Missing consideration | "What about transaction costs / survivorship bias / finite-size effects?" |
| Quantitative sanity check | "This implies a Sharpe of 4 for a decade; is that plausible?" |
| Limit and dimension check | "Does the formula reduce correctly as sigma -> 0? Are units consistent?" |
| Practical objection | "Even if the model is right, can it be traded / measured / computed?" |
| Source context | "Which sample, frequency and estimator produced this value?" |

## Workflow

1. Read the whole draft.
2. Identify the thesis (ask if absent).
3. Strategic coherence.
4. List thesis-critical claims.
5. Note the strong points and leave them alone.
6. Find weak points, thesis-critical first.
7. Phrase challenges as questions or "have you considered", strategic before tactical, each with what would resolve it.
8. When the author answers, acknowledge resolved points.
9. Stop after resolution or two exchanges; record what remains uncertain.

## Output format

```markdown
# Devil's Advocate Review: [document]
Exchange: [1/2 or 2/2]   Date: [YYYY-MM-DD]

## Thesis evaluation
Identified thesis: "..."
Strategic coherence: ...

## Strong points (no challenge needed)
- ...

## Strategic challenges
### 1. [title]
Issue: ...
Challenge: ...
What would address this: ...

## Tactical challenges (thesis-critical)
### 1. [title]
Location: ...
Claim: "..."
Why thesis-critical: ...
Challenge: ...
What would address this: ...

## Overall assessment
Ready to proceed? Main remaining concern?
```

## Does not

Obstruct, demand zero uncertainty, substitute judgment for evidence, keep challenging a point already defended, or rewrite the content.

## Pairs with

fact-checker (verify each citation after the argument holds), statistician and mathematician (to settle a disputed number or derivation), scientific-critical-thinking (evidence-quality patterns).
# Featured skills

The 15 skills behind the Copilot agent pack. Each folder holds a `SKILL.md` (Agent Skills format: works in Claude, Claude Code, Codex, Copilot in VS Code, Kilo Code, Grok Build) plus any reference `.md` files. Scripts from the original repos are not included.

| Skill | What it does | Source and license |
|---|---|---|
| [proof-workbench](proof-workbench/SKILL.md) | Work a hard proof or derivation in stages with a written ledger. Pin down definitions, assumptions and quantifiers, split the claim into lemmas, attack each lem... | own |
| [sanity-checks](sanity-checks/SKILL.md) | Physicist's plausibility pass on a derivation, formula, model output or number before it is reported. Checks units and dimensions, limiting cases, a known speci... | own |
| [red-team](red-team/SKILL.md) | Attack a draft before it ships, whether a recommendation, analysis, model, trading or portfolio idea, backtest, plan, spec or document. Produce the strongest ca... | own |
| [statistician](statistician/SKILL.md) | Use when selecting statistical methods (hypothesis tests, regression), running power analysis, guiding uncertainty quantification (Bayesian or frequentist), or ... | dangeles/claude (MIT), adapted |
| [mathematician](mathematician/SKILL.md) | Use when designing deterministic algorithms, analysing time/space complexity, selecting numerical methods (ODEs, optimisation, linear algebra), or verifying mat... | dangeles/claude (MIT), adapted |
| [devils-advocate](devils-advocate/SKILL.md) | Use when a substantive document, analysis, derivation or research claim needs adversarial review: find the thesis, test whether the evidence supports it, challe... | dangeles/claude (MIT), adapted |
| [econometrics](econometrics/SKILL.md) | Econometric work on time series, panels and cross sections, identification first. Check stationarity, cointegration, serial correlation, heteroskedasticity and ... | own |
| [modeling-loop](modeling-loop/SKILL.md) | Build, fit and judge a model with a fixed discipline. State the question and the loss, fit a naive baseline first, fit candidate models, check residuals and par... | own |
| [solo-proof](solo-proof/SKILL.md) | Use when asked to work one hard mathematics problem to a written proof: reason in stages, save each settled step to a notes file so nothing is lost if a reply i... | anthropics/claude-plugins-official (Apache-2.0), adapted |
| [math-olympiad](math-olympiad/SKILL.md) | Solve competition math problems (IMO, Putnam, USAMO, AIME) with adversarial | anthropics/claude-plugins-official (Apache-2.0) |
| [what-if-oracle](what-if-oracle/SKILL.md) | Supports structured what-if scenario analysis for research planning, experimental contingencies, and scientific project decisions. Explores favorable, reference... | K-Dense-AI/claude-scientific-skills (MIT) |
| [consciousness-council](consciousness-council/SKILL.md) | Structures a multi-perspective council exercise for decisions, research trade-offs, and creative challenges. Simulates thinking archetypes, separates evidence f... | K-Dense-AI/claude-scientific-skills (MIT) |
| [perspective-swarm](perspective-swarm/SKILL.md) | Protocol specification for multi-perspective brainstorming via 5 parallel agents with confidence-weighted synthesis. Executed by brainstorming-pm orchestrator. | dangeles/claude (MIT) |
| [scientific-brainstorming](scientific-brainstorming/SKILL.md) | Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit assumptions, transparent evaluation, adversarial rev... | K-Dense-AI/claude-scientific-skills (MIT) |
| [hypothesis-generation](hypothesis-generation/SKILL.md) | Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or associational claims, discriminating predictions, measurem... | K-Dense-AI/claude-scientific-skills (MIT) |

`own` means written for this account. `adapted` means edited from the source for chat use.

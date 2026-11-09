---
name: "modeling-loop"
description: "Build, fit and judge a model with a fixed discipline. State the question and the loss, fit a naive baseline first, fit candidate models, check residuals and parameter stability, validate out of sample (walk-forward for time series), compare against the baseline with uncertainty, and write a short model card. Use it for any forecasting, regression, classification, risk (VaR, expected shortfall), pricing, factor or physical-parameter model, statistical, machine-learning or mechanistic, and whenever the user asks to model, fit, predict, forecast, calibrate or estimate something from data. Not for choosing a single hypothesis test (statistician), econometric identification and robust inference (econometrics) or designing a simulation study (numerical-experiment)."
---

# Modeling loop

A model is worth its margin over a naive baseline on data it has not seen. Most impressive in-sample fits fail that test, so the loop puts the test first.

## Steps

1. Question and loss. State what is predicted or estimated, at what horizon, and the loss that matters for the decision: squared error, quantile loss for VaR, log-loss, profit after costs.
2. Baseline. Fit the naive model first: random walk or historical mean for returns, last value for levels, historical simulation for VaR, the textbook closed form for a physical system. Every later model is judged against it.
3. Split. Hold out data the model never sees while it is being built. For time series use walk-forward or expanding windows, keep time order, and leave a gap between train and test so overlapping labels do not leak.
4. Candidates. Start simple (linear, ARMA, a few parameters with physical meaning) and add complexity only when it beats the simpler model out of sample.
5. Diagnostics. Residuals for autocorrelation, heteroskedasticity, fat tails and structure against fitted values. Parameters for standard errors, stability across subperiods, and sensible signs and magnitudes.
6. Compare. Out-of-sample loss against the baseline with uncertainty: Diebold-Mariano for forecasts, a bootstrap of the loss difference otherwise, Kupiec and Christoffersen coverage tests for VaR.
7. Sensitivity. Perturb the inputs and hyperparameters that were chosen by hand and report how far the conclusion moves.

## Model card

Write model_card_<name>_<YYYY-MM-DD>.md next to the code, starting from references/model_card.md: question and loss, data and period, split, baseline score, model score with interval, diagnostics, sensitivity, known limits, and what would change the conclusion.

## Report

Lead with the out-of-sample comparison to the baseline. A model that does not beat the baseline is a finding worth stating plainly.

## Bundled files

This copy carries its files inline. Where the skill folder is installed (Codex, Claude Code), use the files there. Otherwise write each block below to the path in its heading, relative to the working directory, before running it.

### references/model_card.md

```markdown
# Model card: <name> (<YYYY-MM-DD>)

Question and horizon:
Loss used for the decision:
Data: source, period, frequency, filters, provenance line
Split: train, validation and test windows, gap between them
Baseline: <naive model>, score
Model: <specification>, score with interval
Comparison: test used and result
Diagnostics: residual autocorrelation, heteroskedasticity, tails, parameter stability (numbers, pass or fail)
Sensitivity: what was perturbed and how far the conclusion moved
Known limits:
What would change the conclusion:
Code and config: path, commit, seed
```
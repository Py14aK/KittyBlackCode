---
name: sanity-checks
description: Physicist's plausibility pass on a derivation, formula, model output or number before it is reported. Checks units and dimensions, limiting cases, a known special case, symmetry and sign, an order-of-magnitude estimate, and recomputes the key number with a second tool. Use it whenever an answer contains a closed-form result, a derived formula, a risk or pricing number (VaR, CVaR, volatility, option prices, Greeks, portfolio variance), a physical quantity with units or a fitted parameter, and whenever the user asks whether a number looks right, sounds right or is plausible, even if they never say check. Not for explaining a concept (learn), sourcing claims in a report (retestable-analysis) or failing code (debug-root-cause).
---

# Sanity checks

A wrong number that looks precise does more damage than an honest "not checked". A few minutes of checks catch most errors in a derivation or a result, so run them before the result reaches the user.

## The checks

Run the ones that apply, cheapest first. A failed check means the result is not settled yet.

1. Units and dimensions. Every term in a sum carries the same units; arguments of exp, log and trig functions are dimensionless. In finance the usual traps are annual versus daily, percent versus decimal, basis points, and per-share versus per-position.
2. Limiting cases. Push a parameter to 0, 1 or infinity and compare with what must happen. Black-Scholes call: as sigma goes to 0 it tends to max(S - K e^(-rT), 0); as T goes to 0 it tends to max(S - K, 0).
3. A known special case. Reduce to a case with a textbook answer: one asset, zero correlation, Gaussian returns, a harmonic potential, a flat yield curve.
4. Symmetry and sign. Put-call parity, CVaR at least VaR at the same level, a covariance matrix that is symmetric positive semidefinite, probabilities in [0, 1] that sum to 1, conserved quantities that stay conserved.
5. Order of magnitude. A one-line estimate that should land within a small factor. For roughly Gaussian daily returns, 1-day 99% VaR is about 2.33 times daily volatility, and daily volatility is about annual volatility divided by the square root of 252. Square-root-of-time scaling multiplies by the square root of the horizon, not by the horizon.
6. Second tool. Recompute the key number another way: closed form against simulation, Python against Wolfram, a sympy simplification of the derived expression, a different library.

For quantities with units or measurement uncertainty, compute with pint and uncertainties in Python, so a dimension error raises instead of passing silently.

## Report

One short line per check that was run: what was tested and the outcome, for example "T to 0 limit: matches intrinsic value". When a check fails, say exactly what failed and give the nearest true statement, then fix the result or flag it. List checks that could not be run as unrun rather than leaving them out. Keep it brief: the user should see what was tested at a glance.

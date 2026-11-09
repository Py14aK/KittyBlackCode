---
name: "econometrics"
description: "Econometric work on time series, panels and cross sections, identification first. Check stationarity, cointegration, serial correlation, heteroskedasticity and structural breaks, then choose the estimator (OLS with HAC errors, ARMA and GARCH, VAR with impulse responses, panel fixed or random effects, IV and 2SLS, event studies, factor regressions) and report robust inference with multiple-testing control. Use it whenever the user runs a regression on economic or financial data, asks about an econometric test, Granger causality or identification, volatility models, cointegration or pairs, factor exposures, event studies or panel data, even if they never say econometrics. Not for test choice outside econometrics (statistician) or forecasting horse races (modeling-loop)."
---

# Econometrics

Economic and financial data break the assumptions behind textbook standard errors: trends, unit roots, serial correlation, volatility clustering, breaks, endogeneity. A coefficient with the wrong standard error is a confident wrong answer, so diagnose first and estimate second.

## Diagnose

Run scripts/ts_diagnostics.py on each series. It puts ADF (null of a unit root) beside KPSS (null of stationarity) with a joint verdict, plus Ljung-Box on levels, Ljung-Box on squares and ARCH-LM (on AR residuals when the levels are autocorrelated, so mean dynamics are not read as volatility clustering), Jarque-Bera and a Newey-West lag suggestion. The two stationarity tests have opposite nulls, so agreement is the evidence; a conflict points to breaks, long memory or a 5% false rejection.

- Unit root in levels: model returns or differences, or test for cointegration before regressing levels on levels, which is otherwise spurious.
- Volatility clustering: a GARCH-type model, or at least HAC standard errors.
- Breaks: Chow at a known date, Bai-Perron for unknown dates; split the sample when the regime changed.

## Estimate

- Time-series regression: OLS with Newey-West (HAC) standard errors.
- Volatility: GARCH(1,1) with Student-t errors as the default; check that persistence stays below 1.
- Dynamics: VAR in stationary variables, lag order by information criteria, impulse responses with bootstrap bands. Granger causality is predictive, not causal.
- Cointegration: Engle-Granger for two series, Johansen for more. For pairs, report the half-life of the spread.
- Panels: fixed effects by default, Hausman test before random effects, standard errors clustered by entity and time.
- Endogeneity: IV and 2SLS with a first-stage F of at least about 10, higher being safer, and an argument for exclusion. Say what the instrument assumes.
- Factor regressions and event studies: name the factor set or the estimation and event windows; use cumulative abnormal returns with proper standard errors.

## Inference hygiene

Report effect sizes with intervals. When many specifications or factors were tried, say how many and raise the bar (a t-statistic near 3 for a new factor) or control the false discovery rate. Use bootstrap or nonparametric inference when residuals are far from normal.

## Tools

Python statsmodels, arch and linearmodels; Julia or Wolfram for a second implementation of the key estimate.

## Report

Specification, the diagnostics that shaped it, estimates with robust intervals, what the identification assumes, and the checks not run.

## Bundled files

This copy carries its files inline. Where the skill folder is installed (Codex, Claude Code), use the files there. Otherwise write each block below to the path in its heading, relative to the working directory, before running it.

### scripts/ts_diagnostics.py

```python
#!/usr/bin/env python3
"""ts_diagnostics.py  (econometrics skill)

Stationarity and dependence diagnostics for one or more series in a file.
ADF (null of a unit root) and KPSS (null of stationarity) side by side with a
joint verdict, Ljung-Box on levels, Ljung-Box on squares and ARCH-LM (on AR
residuals when the levels are autocorrelated), Jarque-Bera, and the
Newey-West lag rule floor(4 (T/100)^(2/9)).

Usage
  python ts_diagnostics.py FILE --cols a,b [--transform none|diff|logret]
                           [--trend c|ct] [--lags 10] [--alpha 0.05] [--json OUT.json]

Needs statsmodels and scipy. KPSS p-values are interpolated from a table and
capped at 0.01 and 0.10, so they are reported as bounds at the edges.
"""
from __future__ import annotations

import argparse
import inspect
import json
import math
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

try:
    from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
    from statsmodels.tsa.ar_model import AutoReg, ar_select_order
    from statsmodels.tsa.stattools import adfuller, kpss
except ImportError:  # keep the error readable
    raise SystemExit("statsmodels is required: pip install statsmodels")


def call(fn, *args, **kw):
    """statsmodels 0.15 began moving tests to result objects; ask for the classic tuple
    where the switch exists so positional unpacking stays valid across versions."""
    if "result_object" in inspect.signature(fn).parameters:
        kw["result_object"] = False
    return fn(*args, **kw)


def prewhiten(x: np.ndarray, maxlag: int = 10) -> tuple[np.ndarray, int]:
    """Residuals of an AR(k) fit, k by AIC. Squares of an autocorrelated series are
    autocorrelated too, so ARCH tests on raw levels confuse mean and variance dynamics."""
    sel = ar_select_order(x, maxlag=maxlag, ic="aic", trend="c")
    k = max(sel.ar_lags) if sel.ar_lags else 0
    if k == 0:
        return x - x.mean(), 0
    return np.asarray(AutoReg(x, lags=k, trend="c").fit().resid), k


def transform(x: pd.Series, how: str) -> pd.Series:
    if how == "diff":
        return x.diff().dropna()
    if how == "logret":
        if (x <= 0).any():
            raise SystemExit("logret needs strictly positive values")
        return np.log(x).diff().dropna()
    return x.dropna()


def verdict(adf_p: float, kpss_p: float, alpha: float) -> str:
    adf_rejects, kpss_rejects = adf_p < alpha, kpss_p < alpha
    if adf_rejects and not kpss_rejects:
        return "stationary"
    if not adf_rejects and kpss_rejects:
        return "unit root"
    if adf_rejects and kpss_rejects:
        return "conflicting: check for breaks or long memory"
    return "inconclusive: low power, get more data"


def diagnose(x: pd.Series, lags: int, alpha: float, trend: str = "c") -> dict:
    x = x.astype(float).to_numpy()
    n = len(x)
    if n < 30:
        raise SystemExit(f"series too short for these tests: {n} points")
    adf_stat, adf_p, *_ = call(adfuller, x, regression=trend, autolag="AIC")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # InterpolationWarning when p is at the table edge
        kpss_stat, kpss_p, *_ = call(kpss, x, regression=trend, nlags="auto")
    c = x - x.mean()
    lb = acorr_ljungbox(c, lags=[lags], return_df=True)
    lb_p = float(lb["lb_pvalue"].iloc[0])
    resid, k = prewhiten(x) if lb_p < alpha else (c, 0)
    lb2 = acorr_ljungbox(resid ** 2, lags=[lags], return_df=True)
    arch_lm, arch_p, *_ = call(het_arch, resid, nlags=lags)
    jb_stat, jb_p = stats.jarque_bera(x)
    return {
        "n": n,
        "adf_stat": round(float(adf_stat), 3), "adf_p": round(float(adf_p), 4),
        "kpss_stat": round(float(kpss_stat), 3), "kpss_p": round(float(kpss_p), 4),
        "verdict": verdict(adf_p, kpss_p, alpha),
        "ljungbox_p": round(lb_p, 4),
        "prewhiten_lags": k,
        "ljungbox_sq_p": round(float(lb2["lb_pvalue"].iloc[0]), 4),
        "arch_lm_p": round(float(arch_p), 4),
        "jarque_bera_p": round(float(jb_p), 4),
        "newey_west_lags": int(math.floor(4 * (n / 100) ** (2 / 9))),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file")
    ap.add_argument("--cols", required=True, help="comma-separated column names")
    ap.add_argument("--transform", choices=["none", "diff", "logret"], default="none")
    ap.add_argument("--trend", choices=["c", "ct"], default="c",
                    help="c: constant (level-stationary null for KPSS); ct: constant and trend")
    ap.add_argument("--lags", type=int, default=10)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--json")
    a = ap.parse_args()

    df = pd.read_parquet(a.file) if a.file.endswith(".parquet") else pd.read_csv(a.file)
    cols = [c.strip() for c in a.cols.split(",")]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"missing columns {missing}; file has {list(df.columns)}")
    out = {c: diagnose(transform(pd.to_numeric(df[c], errors="coerce"), a.transform), a.lags, a.alpha, a.trend)
           for c in cols}
    print(f"transform={a.transform}  trend={a.trend}  lags={a.lags}  alpha={a.alpha}")
    print(f"{'series':<12}{'n':>6}{'ADF p':>8}{'KPSS p':>8}  {'verdict':<44}{'LB p':>7}{'pw':>4}{'LB^2 p':>8}"
          f"{'ARCH p':>8}{'JB p':>8}{'NW lags':>8}")
    for c, r in out.items():
        print(f"{c:<12}{r['n']:>6}{r['adf_p']:>8.3f}{r['kpss_p']:>8.3f}  {r['verdict']:<44}"
              f"{r['ljungbox_p']:>7.3f}{r['prewhiten_lags']:>4}{r['ljungbox_sq_p']:>8.3f}{r['arch_lm_p']:>8.3f}"
              f"{r['jarque_bera_p']:>8.3f}{r['newey_west_lags']:>8}")
    print("pw: AR order removed before LB^2 and ARCH when levels are autocorrelated (0 = raw).")
    print("KPSS p is interpolated and capped to [0.01, 0.10]; read 0.010 as <=0.01 and 0.100 as >=0.10.")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
        print("json written to", a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
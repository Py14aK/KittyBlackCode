# Hashigami adapted for FA

Source dump: SAS hash merge macro, HashSort, group sums, MD5 chunks, array-hash, unfinished Fib scheme, plus `Risk/path_finding_with_hash`.

Library home: `Py14aK/Py14aK/SaS Black Belt Hashigami` and `Py14aK/Py14aK/SaS`.

## What was broken in the paste

- `%mend merge();` should be `%mend merge;`
- `if _n_=0 then set` does not load attributes; use `if 0 then set`
- Hash constructor commas and `ordered` arguments were truncated
- Fib / Horner listing mixed an unfinished `data _NULL_` Fibonacci fragment into the array-hash program
- Cyrillic placeholder dataset names are examples, not UBB table names

## FA ports

Account lookup — key `account_id` or `BENEF.ID`, data `pd_hat`, `urg`, `score`.
Vintage S-matrix — key `month score_band`, data counts of good/bad, rate = bad/n.
URG migration — key `urg_bck`, multidata forward URG rows.
VoP match — key IBAN plus normalised name hash; miss is unmatched, not a default.
Broken event order — path rebuild with pid/id as in `path_finding_with_hash`.

## Python stand-in when SAS is unavailable

```python
from collections import defaultdict

def group_sum(rows, key, val):
    s, n = defaultdict(float), defaultdict(int)
    for r in rows:
        k = r[key]
        if r[val] is None:
            continue
        s[k] += r[val]
        n[k] += 1
    return {k: {"sum": s[k], "n": n[k], "mean": s[k] / n[k] if n[k] else None} for k in s}
```

Use pandas `groupby` for S-matrix cells. Use an ordered dict when you need last-month wins.
Do not call this a PD calibration.

## RAM rule from the dump, kept

Split the unsorted book on a uniform partial key or on `rank(char(md5(...),1))`.
Keep chunk count in 4–10 unless the partial key is indexed.
Clear hashes at the end of each ID by-group.

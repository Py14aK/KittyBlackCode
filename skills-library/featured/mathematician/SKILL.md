---
name: "mathematician"
description: "Use when designing deterministic algorithms, analysing time/space complexity, selecting numerical methods (ODEs, optimisation, linear algebra), or verifying mathematical correctness. Not for statistical method selection (use statistician)."
---

# Mathematician

Algorithm design, complexity analysis, numerical method selection and mathematical verification. Produces a specification (and, in chat, runnable reference code when useful) whose correctness is argued, not asserted.

## When to use

- Algorithm design requiring complexity analysis (Big-O)
- Numerical methods selection (integration, ODEs, optimisation, linear algebra, root finding)
- Mathematical correctness verification of an algorithm or derivation
- Optimisation problem formulation and solver selection
- Data structure selection from access patterns and constraints

Trigger words: algorithm, complexity, O(n), Big-O, optimisation, minimise, maximise, numerical, approximation, precision, conditioning, sort, search, graph, tree, matrix, eigenvalue, decomposition.

## When not to use

- Statistical inference, hypothesis tests, MCMC, confidence intervals: use statistician
- Simple operations needing no analysis (CRUD, I/O)
- Constraint satisfaction / scheduling / puzzle uniqueness: prefer the ortools skill for the solver, use this skill for the formulation

## Workflow

1. Pin down constraints: input size bounds, time and space budgets, precision needs, available libraries.
2. Classify the problem (sorting, search, graph, optimisation, linear system, ODE, eigenproblem ...).
3. Review the standard algorithms for that class against the constraints; select or design.
4. Complexity analysis: best / average / worst time, auxiliary and total space, method used (recurrence + Master theorem, loop analysis, amortised analysis).
5. Numerical stability assessment wherever floating point is involved.
6. Deliver: pseudocode or runnable code, invariants, test cases, edge cases, alternatives with trade-offs, confidence level with reason.
7. Where a claim can be checked, check it: symbolic (SymPy / Wolfram) or numerical (small-n brute force vs the fast algorithm).

## Output format

```yaml
math_handoff:
  algorithm: {name, description}
  complexity_analysis:
    time: {best_case, average_case, worst_case}
    space: {auxiliary, total}
    analysis_notes: how it was derived
  numerical_stability:
    stable: bool
    conditions: when it holds
    precision_requirements: float32 / float64 / extended
    failure_modes: [condition, symptom, mitigation]
  implementation_guidance:
    recommended_approach, pseudocode, libraries, pitfalls
  verification_criteria:
    invariants: []
    test_cases: []
    edge_cases: []
  alternative_approaches: [name, trade_off, when_to_use]
  confidence: high | medium | low
  confidence_notes: why
```

## Complexity analysis protocol

Report time (best, average, worst) and space (auxiliary, total), plus the method: recurrence relation if recursive, loop analysis if iterative, amortised analysis if applicable.

Example, merge sort: T(n) = 2T(n/2) + O(n). Master theorem with a=2, b=2, f(n)=n gives log_b a = 1, f(n) = Theta(n^1), case 2, so T(n) = Theta(n log n) in all cases; O(n) auxiliary space for the merge buffer.

## Numerical stability assessment

1. Identify issues: catastrophic cancellation, overflow / underflow, accumulated rounding, condition number of the problem.
2. Mitigate: algorithmic changes (Kahan summation, log-sum-exp, pivoting, QR instead of normal equations), precision choice, reformulation.

```yaml
numerical_stability:
  stable: true
  conditions: well-conditioned matrices (cond < 1e6)
  precision_requirements: float64 required
  failure_modes:
    - condition: singular or near-singular matrix
      symptom: division by zero or extreme values
      mitigation: check condition number first
    - condition: very small pivots
      symptom: amplified rounding error
      mitigation: partial pivoting
```

## Reference tables

### Sorting

| Algorithm | Avg | Worst | Space | Stable | Notes |
|---|---|---|---|---|---|
| Merge sort | n log n | n log n | n | yes | preferred for stability |
| Quick sort | n log n | n^2 | log n | no | fast in practice |
| Heap sort | n log n | n log n | 1 | no | in-place guarantee |
| Timsort | n log n | n log n | n | yes | Python default |

### Searching

| Algorithm | Avg | Requires | Notes |
|---|---|---|---|
| Binary search | log n | sorted array | iterative preferred |
| Hash table | 1 | good hash | n worst case |
| Balanced BST | log n | balancing | n if unbalanced |
| B-tree | log n | - | disk friendly |

### Graphs

| Algorithm | Time | Space | Use |
|---|---|---|---|
| BFS | V+E | V | unweighted shortest path |
| DFS | V+E | V | connectivity, cycles |
| Dijkstra | (V+E) log V | V | non-negative weights |
| Bellman-Ford | VE | V | negative weights |
| Floyd-Warshall | V^3 | V^2 | all pairs |

### Numerical methods

| Method | Use | Stability | Library |
|---|---|---|---|
| LU (pivoted) | linear systems | stable with pivoting | scipy.linalg.lu_factor |
| QR | least squares | stable | numpy.linalg.qr |
| SVD | low rank, pseudo-inverse | very stable | numpy.linalg.svd |
| Cholesky | SPD systems, covariance | stable for SPD | scipy.linalg.cholesky |
| Newton-Raphson | roots | quadratic near root | scipy.optimize |
| Gradient / quasi-Newton | smooth optimisation | depends on conditioning | scipy.optimize.minimize |
| RK45 / Radau | non-stiff / stiff ODEs | adaptive | scipy.integrate.solve_ivp |

## Coordination with statistician

Mathematician owns complexity, numerical stability, computational efficiency, data structures. Statistician owns statistical validity, intervals, tests, Monte Carlo convergence. Example, Monte Carlo integration: mathematician gives the sampling algorithm and convergence rate; statistician gives variance reduction and the confidence interval.

## Worked example: k-nearest neighbours

Request: n up to 1e6 points in d up to 100 dimensions, m up to 1e4 queries, k up to 100; build O(n log n), query O(log n + k), space O(n).

Handoff: KD-tree for d < 20, ball tree above. Build O(n log n), query O(log n + k) average, O(n) worst for adversarial data; KD-tree degrades toward O(n) for d > 20 (curse of dimensionality). Use sklearn.neighbors.KDTree / BallTree; for d > 20 consider approximate methods (Annoy, Faiss). Pitfalls: do not rebuild per query batch; normalise features with different scales. Tests: a query point in the data returns itself first; query time scales as log n on uniform data. Edge case: equidistant duplicates return in arbitrary order. Confidence high.
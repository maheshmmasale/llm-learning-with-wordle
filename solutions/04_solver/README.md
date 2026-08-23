# 04 — Constraint solver

`ConstraintSolver` retains only candidate answers that would reproduce every
observed feedback pattern. This exact replay approach naturally handles repeated
letters: for example, a gray copy of a letter can impose an upper count even
when another copy is green or yellow.

```python
from solver import ConstraintSolver

solver = ConstraintSolver(["cigar", "rebut", "sissy", "humph"])
remaining = solver.add_feedback("array", "BYBGB")
print(remaining)
print(solver.constraints.minimum_counts)
print(solver.best_guess())
```

Feedback uses `G` (green), `Y` (yellow), and `B` (gray). `add_feedback` accepts
probe guesses outside the candidate list. `best_guess()` maximizes feedback
entropy over remaining answers; pass a larger allowed-guess list to consider
non-answer probes. It raises a clear error if observations leave no candidates.

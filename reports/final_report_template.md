# Final Report Checklist

Fill this in; delete the guidance lines. One page per section max. Every
number must point at a committed run directory (`experiments/results/`).

## Metadata

- Author, date, repo commit, base model + exact revision, divides of
  train/validation/test/challenge targets.

## Claim and evidence (one row per claim)

| Claim | Evidence (run dir + metric) | Threat to validity |
|---|---|---|
| | | |

## Required sections

1. **Problem** — one paragraph: task, constraints (local-only, budgets).
2. **Method** — system diagram in words: model, solver, search, data.
3. **Baselines** — random, heuristic, base model, prompted model, strong
   reference, all under one protocol with seeds. Table: win rate (as
   count + %), avg guesses, calls, tokens, wall time.
4. **Experiments** — what you changed, one factor at a time; negative
   results required (at least one).
5. **Ablations** — remove each technique in turn; attribute every gain to
   training vs prompting vs filtering vs search.
6. **Failure analysis** — categorized failures with counts and examples
   (repeated letters, uncommon words, OOD states).
7. **Leakage audit** — how you verified the target never reaches the model
   (observations, prompts, dataset rows, solver inputs).
8. **Compute** — training and inference cost estimates; what halves/doubles
   with 2x budget.

## Evidence checklist (from `grading_rubric.md`)

- [ ] Frozen held-out target list; documented split policy.
- [ ] Exact commands for one baseline and the best system.
- [ ] Machine-readable per-game outcomes committed.
- [ ] Compute/cost estimates recorded.
- [ ] Three independent runs per central comparison (or written justification).
- [ ] At least one negative result + one qualitative failure analysis.
- [ ] Model-only vs model+solver vs model+search distinguished.

## Honesty section

Strongest supported conclusion; most uncertain conclusion; what you would
try with 10x compute and why the evidence earns that experiment.

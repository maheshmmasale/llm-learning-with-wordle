# Problem 08 — Final Challenge: A Local End-to-End Guessing System

## Module context

Integrate everything under fixed budgets with a comparison against targets
you write down before running. A credible negative result with rigorous
ablations beats a high score from leakage or undocumented tuning.

- Theory: `theory/01_ablations.md`, `theory/06_evaluation_and_statistics.md`
- Reference solution: `src/solutions/08_final/`

## Objective

Ship a complete guessing system that runs **entirely on consumer hardware**
and lands within **5pp of a strong reference's win rate** at **≥4× less
inference compute** — with the ledger to prove it.

## Constraints

- <16 GB RAM, ≤8 cores, models <1B params, CPU fallback for everything.
- Final path: <5 s/game on CPU (median + p95 reported).
- Targets and primary compute unit declared before the frozen test run.

## Requirements

1. One executable pipeline: data → train/select → inference → eval →
   compute ledger → report. Local only; no paid APIs or hosted inference.
2. Strong reference: exact/high-compute local procedure, validated on
   validation data, same information constraints.
3. Frozen test: identical games, seeds, rules for student and reference;
   sample size justified; never touch the system after seeing outcomes.
4. ≥5 ablations (adaptation on/off, search on/off, adaptive vs fixed
   compute, data balancing, one architecture choice) + robustness tests on
   ≥2 distribution shifts.
5. Compute ledger reconciling every material run (configs, seeds, tokens,
   calls, CPU-hours, peak RAM, checksums); per-decision traces for the
   final path.

## Done when

- Win-rate gap ≤5pp with honest uncertainty; compute ratio ≥4× on raw
  counts, neural and symbolic reported separately.
- Smoke test reproduces a small CPU-only run from saved artifacts.
- Final report links every figure to machine-readable source data.

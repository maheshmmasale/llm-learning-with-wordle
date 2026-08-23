# Module 8 — Final Integrated Experiment and Research Challenge

## Research challenge

Starting from a public 0.2B–0.5B language model, build a Wordle system that comes within approximately five percentage points of a strong reference on a held-out benchmark while using substantially less inference compute and staying within the declared training budget. The threshold may be revised only from evidence gathered when the benchmark and reference were frozen—not after seeing final results.

This is not a leaderboard-only exercise. A credible negative result with rigorous ablations is more valuable than a high score produced by leakage, undocumented tuning, or an incomparable budget.

## Learning objectives

By the end of this module, you should be able to:

- Integrate environment, model, training, solver, and evaluation components.
- Form a testable hypothesis and predeclare a final comparison.
- Optimize under fixed training and inference compute budgets.
- Design ablations that identify the causes of improvement.
- Evaluate generalization, failure modes, and statistical uncertainty.
- Produce a reproducible research artifact suitable for a portfolio or interview.
- Explain deployment tradeoffs beyond the toy task.

## Experimental contract

Before the final run, write a short preregistration containing:

- chosen base model and exact revision;
- fixed train, validation, test, and challenge splits;
- strong reference and its information/call budget;
- primary metric and acceptable confidence interval method;
- training budget, for example `$300` or a fixed number of GPU-hours;
- inference budgets in tokens, calls, latency, and solver expansions;
- final system configuration selected using validation only;
- planned ablations and stopping criteria.

Freeze the test set until this document is committed. Preserve all configuration files, environment details, package versions, seeds, checkpoints, and raw trajectories.

Useful resources:

- [NeurIPS reproducibility checklist](https://neurips.cc/public/guides/PaperChecklist)
- [ML reproducibility checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf)
- [W&B experiment tracking](https://docs.wandb.ai/) or [MLflow](https://mlflow.org/docs/latest/)
- [Matplotlib](https://matplotlib.org/stable/) and [Seaborn](https://seaborn.pydata.org/)
- [ACM artifact review and badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)

## Required system comparisons

At minimum, compare:

1. random and heuristic baselines;
2. untouched small base model;
3. best prompted small model;
4. deterministic solver alone;
5. SFT model;
6. SFT plus filtering/search;
7. best inference-scaled system;
8. strong reference.

Use the same target order and rules. Report solve rate with uncertainty, mean/median guesses, guess distribution, invalid rate, repeated-letter performance, difficulty strata, model calls, tokens, wall time, memory, and estimated cost.

## Core ablations

Remove or replace one component at a time while keeping the rest fixed:

- SFT weights → base weights;
- generated training data → smaller or simpler data;
- exact constraint filter → no filter;
- entropy/search reranker → model-only selection;
- multiple samples → one sample;
- structured prompt → minimal prompt;
- full compute budget → half budget.

Add at least one interaction test, such as whether search helps the base and SFT models equally. Include a failure taxonomy with representative trajectories: invalid output, forgotten constraint, locally reasonable but globally poor guess, repeated-letter error, overexploration, and premature answer commitment.

## Questions to answer

- Did the system meet the within-five-point target, and is the conclusion statistically supported?
- What fraction of improvement comes from training, deterministic tools, and extra inference compute?
- Does the model learn transferable decision rules or imitate teacher trajectories?
- What happens when training or inference compute is halved?
- Which component is the performance bottleneck?
- What would you change with ten times the compute?
- How would batching, caching, reliability, monitoring, and cost change at one million games per day?
- Which conclusions plausibly transfer beyond Wordle, and which are environment-specific?

## Deliverables

- A one-command or scripted final benchmark using frozen configs.
- A complete results directory with raw trajectories, summaries, plots, and resource logs.
- A final ablation matrix and compute-performance frontier.
- A research report with abstract, related work, methods, results, generalization, failure analysis, limitations, conclusions, and future work.
- A concise model/system card, reproducibility instructions, and budget ledger.
- A 10–15 minute presentation or recorded walkthrough plus a live demonstration.
- An executive summary explaining the strongest result and the most important negative result.

**Exit criterion:** an independent reviewer can reproduce the headline claim, audit the compute budget, and understand why the best system works—not merely observe that it scores well.
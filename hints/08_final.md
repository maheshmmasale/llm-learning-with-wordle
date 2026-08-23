# Hints: Final Challenge

> **Try without hints first.** Draft your experiment table and success criteria before assembling the final system. The goal is a defensible conclusion, not one lucky score.

## Level 1 — Think in ablations

For each component in the best system, ask: what claim does this component support, and what happens when it is removed?

A useful core table may compare:

- base model,
- prompted model,
- deterministic solver alone,
- model + solver,
- SFT model,
- SFT + solver/search,
- best inference-scaled system.

Keep targets, seeds, parsing rules, and budgets aligned so differences can be attributed to the component under study.

## Level 2 — Allocate the fixed budget deliberately

Before final runs, reserve compute for:

- smoke tests and debugging,
- baseline replication,
- a small hyperparameter sweep,
- at least one failed/negative hypothesis,
- final held-out evaluation,
- reruns or uncertainty checks.

Do not spend the full budget on one long training run. Maintain a compute ledger containing training GPU-hours/cost and inference cost. Decide in advance which metric controls model selection.

## Level 3 — Combine only validated components

Build the final system from pieces that each earned their place in controlled experiments. Confirm interface compatibility: training format matches inference format, feedback encodings match, solver vocabulary matches evaluation rules, and reranker scores are calibrated for remaining turns.

Run the best configuration once on the untouched test benchmark after choices are frozen. Include uncertainty, reference-model conditions, and capability-per-compute—not just the headline win rate.

## Level 4 — Turn failure modes into the report

Tag unsuccessful games and inspect representative traces. Possible categories:

- invalid or unparsable output,
- violated green/yellow constraints,
- duplicate-letter misunderstanding,
- vocabulary mismatch,
- over-exploration late in the game,
- premature exploitation,
- repeated guess,
- candidate generator omitted the winning action,
- verifier selected the wrong candidate,
- distribution shift or memorization,
- latency/search-budget failure.

A final decision checklist:

```text
[ ] Frozen target set and split manifest
[ ] Same evaluation protocol for all comparable systems
[ ] Baselines rerun with recorded seeds/configs
[ ] Component ablations completed
[ ] Training + inference compute ledger complete
[ ] Confidence intervals or paired significance analysis included
[ ] Leakage checks passed
[ ] Failure categories quantified with example traces
[ ] Reproduction command tested from a clean environment
[ ] Claims limited to what the evidence supports
```

If the target score is missed, do not hide it. A rigorous explanation of where the gap remains—and which experiment would most efficiently test the next hypothesis—can be a stronger research artifact than an opaque high score.

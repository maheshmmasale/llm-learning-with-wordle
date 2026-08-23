# Hints: Inference-Time Scaling

> **Try without hints first.** More inference compute is useful only if you measure it and show where it helps.

## Level 1 — Generate more than one candidate

Instead of accepting the first completion, sample or decode several candidate guesses. Deduplicate them and retain raw outputs for analysis.

Vary one dimension at a time: number of samples, temperature, top-p, beam width, or prompt. More generations can improve coverage while also increasing invalid and redundant proposals.

## Level 2 — Add an explicit verifier or reranker

Candidate generation and candidate selection can be separate. A verifier might check:

- dictionary membership,
- consistency with known constraints,
- expected information gain,
- answer probability,
- shallow rollout success,
- a learned value score.

Report whether the winning candidate came from the model’s first choice or was rescued by the verifier. Compare model-only reranking with deterministic ranking to identify the source of gains.

## Level 3 — Account for compute end to end

For every game, log at least:

- number of model calls,
- prompt and generated tokens,
- candidate count,
- solver/search nodes,
- wall-clock latency,
- peak memory where available,
- estimated or measured cost.

A retry, verifier call, and rollout are not free. Use identical hardware and batching conditions for timing comparisons, with warm-up runs. If exact FLOPs are unavailable, state your proxy rather than presenting token count as literal FLOPs.

## Level 4 — Build a Pareto frontier

Sweep a small set of budgets—for example 1, 2, 4, 8, and 16 candidate generations—and plot performance against compute or latency. A system is Pareto-dominated if another system is at least as accurate and no more expensive, with one strict improvement.

```python
records = []
for budget in [1, 2, 4, 8, 16]:
    metrics = evaluate(policy.with_candidate_budget(budget), games)
    records.append({
        "budget": budget,
        "win_rate": metrics.win_rate,
        "tokens_per_game": metrics.tokens_per_game,
        "latency_ms": metrics.latency_ms,
    })
```

Add confidence intervals or paired bootstrap comparisons on the same target games. Highlight the “knee” of the curve: where additional compute yields sharply diminishing returns. The best research result may be a slightly lower score with far better capability per unit compute.

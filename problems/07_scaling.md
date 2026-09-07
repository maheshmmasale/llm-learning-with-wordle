# Problem 07 — Inference-Time Scaling and Compute–Quality Tradeoffs

## Module context

Weights are only one source of capability: proposals, verifiers, and search
buy performance with test-time compute. Plot the compute–performance frontier
and attribute gains to diversity, filtering, verification, and search
separately.

- Theory: `theory/04_search_and_solver.md`, `theory/02_local_llms.md`
- Reference solution: `src/solutions/07_scaling/`

## Objective

Compare direct decoding, repeated sampling, reranking, and explicit search
from one checkpoint on identical games, and deliver a **Pareto curve of
inference compute vs win rate** where every point is auditable.

## Requirements

1. One policy interface: (state, hard budget, seed, config) → legal action
   + compute trace. Budgets enforced, not estimated afterward.
2. Methods: direct decoding; sampling at several counts with dedup;
   reranking with ≥2 signals (likelihood, entropy, value, simulation);
   explicit search (beam / best-first / MCTS / rollouts); one neural+symbolic
   hybrid that sees only legitimate state.
3. ≥5 budgets spanning ≥10× in a predeclared primary unit (FLOPs, forward
   passes, or calibrated cost); keep raw counts (tokens, calls, nodes,
   latency) alongside.
4. Same checkpoint, tokenizer, action set, stopping rules, and game
   instances everywhere; predeclare ties, timeouts, invalid handling.
5. Stochastic methods get multiple paired seeds; win rates carry intervals.

## Done when

- Pareto plot regenerable from released per-game records + plotting code;
  dominated points identified, not hidden.
- A budget auditor confirms no trace exceeds its cap, cache included.
- Verdict per method: where it beats direct decoding, where it saturates,
  and why — or credible negative evidence.

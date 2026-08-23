# Module 7 — Inference-Time Scaling

## Why this module matters

Model weights are only one source of capability. At inference time, a small model can generate multiple proposals, critique them, use a verifier, or search over possible futures. This module investigates a central modern question: how much performance can additional test-time computation recover without increasing model size or retraining?

## Learning objectives

By the end of this module, you should be able to:

- Define inference compute in measurable units.
- Generate diverse candidate actions with controlled sampling.
- Implement self-consistency and deterministic or learned reranking.
- Build a verifier for legality, constraint satisfaction, or strategic quality.
- Sweep temperature, candidate count, calls, beam width, and search depth.
- Plot compute-performance frontiers and identify dominated systems.
- Separate gains from diversity, filtering, verification, and additional search.

## Techniques

**Multiple candidate generation** samples `k` guesses from one or more model calls. Diversity matters: duplicate proposals do not provide useful extra compute. Track unique valid candidates as well as total generations.

**Self-consistency** aggregates repeated reasoning paths or votes over final guesses. For Wordle, exact word voting may fragment, so consider voting over candidate rankings, constraint interpretations, or scorer-selected proposals.

**Reranking** applies a deterministic entropy score, a learned reward model, or an LLM judge to the same candidate pool. A **verifier** can reject invalid words and known constraint violations, then assess strategic quality. Keep hard correctness checks deterministic whenever possible.

**Search** explores future feedback partitions with beam search, expectimax, or Monte Carlo-style rollout. Define what is simulated and ensure no hidden target enters the policy. Cache repeated partition computations.

Recommended reading:

- [Self-Consistency](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [Let’s Verify Step by Step](https://arxiv.org/abs/2305.20050)
- [Scaling LLM Test-Time Compute](https://arxiv.org/search/?query=test-time+compute+language+models&searchtype=all)
- [Hugging Face generation strategies](https://huggingface.co/docs/transformers/generation_strategies)

## Compute accounting

Report at least model calls, prompt tokens, generated tokens, wall-clock latency, and peak memory. Where possible, estimate FLOPs as a function of model parameters and tokens. Distinguish serial latency from parallelizable work. Record solver node expansions and scorer calls separately from neural compute.

Choose a reference budget, such as one greedy call, then evaluate multiples of that budget. A result is Pareto-dominated if another system has equal or better solve rate at lower compute. Plot win rate, invalid rate, and average guesses against tokens, latency, calls, and estimated cost.

## Suggested experiments

1. Candidate counts `k = 1, 2, 4, 8, 16, 32`.
2. Temperatures such as 0, 0.2, 0.7, 1.0, with and without top-p sampling.
3. Majority/self-consistency selection versus entropy reranking on identical generations.
4. Deterministic verifier versus LLM verifier versus both.
5. One long reasoning call versus several short independent calls with equal token budgets.
6. Beam widths and depths under matched wall-clock or node-expansion budgets.
7. Base model versus SFT model across the same inference budgets.
8. Adaptive compute: spend more calls only when the candidate set is large or verifier confidence is low.

Use fixed seeds where possible, but report variance over stochastic runs. Do not choose the best seed. Include confidence intervals because small differences can be noise.

## Questions to answer

- Where are the steepest and flattest parts of the compute-performance curve?
- Does temperature improve strategic diversity or only invalid-output rate?
- Which component selects the winning candidate: model, verifier, or solver?
- Is adaptive compute more efficient than a fixed budget per turn?
- Do SFT and inference scaling complement or substitute for one another?
- How much parallel hardware would be required to realize theoretical latency gains?
- At what point would a larger model become cheaper or faster than scaling the small one?

## Deliverables

- Configurable candidate generation, aggregation, reranking, and verification modules.
- A sweep manifest covering temperature, samples, calls, search depth, and beam width.
- Raw resource logs and reproducible stochastic seeds.
- Compute-versus-performance plots with Pareto frontiers.
- An ablation table isolating diversity, hard filtering, reranking, verification, and search.
- A recommended inference policy for low-, medium-, and high-compute regimes.
- A short analysis explaining diminishing returns and the fairness of compute accounting.

**Exit criterion:** you can recommend a system for a stated inference budget and defend why no tested alternative achieves better Wordle performance for less measured compute.
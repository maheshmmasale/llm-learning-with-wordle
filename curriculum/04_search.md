# Module 4 — External Constraint Solving and Search

## Why this module matters

A language model may know useful word statistics while failing at exact bookkeeping. Wordle lets you separate these capabilities cleanly. The environment and solver should enforce deterministic facts; the model can then generate or rank candidates. This decomposition creates stronger systems and clearer scientific conclusions about what the model contributes.

## Learning objectives

By the end of this module, you should be able to:

- Build an exact candidate filter from guess/feedback history.
- Separate LLM proposal, deterministic validation, scoring, and action selection.
- Implement entropy and expected-remaining-candidates heuristics.
- Compare answer-only guesses with exploratory guesses.
- Add constrained reranking, beam search, or shallow lookahead.
- Attribute performance gains to solver, search, and LLM components.

## Architecture

Use explicit interfaces:

```text
public state → LLM candidate generator → candidate validator
             → deterministic scorer/search → selected guess
```

The solver must derive its candidate set only from public feedback. A proposed word may be (a) invalid, (b) valid but inconsistent with known constraints, (c) a possible answer, or (d) a legal exploratory guess that cannot be the answer. Keep these categories separate.

For each possible guess `g`, partition remaining answers by feedback pattern. Compute quantities such as expected posterior size, worst-case bucket size, solve probability, or Shannon entropy. Entropy is useful but not automatically optimal under a six-turn objective; test alternative criteria.

Recommended resources:

- [Shannon, “A Mathematical Theory of Communication”](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)
- [3Blue1Brown: Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [NetworkX search algorithms](https://networkx.org/documentation/stable/reference/algorithms/)
- [Python profiling](https://docs.python.org/3/library/profile.html)

## System variants

Benchmark at least these variants:

1. **LLM alone:** direct next-guess generation.
2. **Filter only:** reject inconsistent proposals and request or choose a valid replacement.
3. **Solver alone:** deterministic entropy or frequency policy.
4. **LLM proposals + solver ranking:** sample `k` legal words, score them deterministically, select the best.
5. **Solver proposals + LLM ranking:** provide top candidates or strategic probes to the model.
6. **Search:** evaluate multi-step consequences through beam search or depth-limited expectimax over feedback partitions.

For beam search, define the node, branch, score, depth, and pruning policy. Cache `(candidate_set, guess)` partitions; otherwise repeated scoring can dominate runtime. Log whether a guess originated from the LLM, fallback, or solver.

## Suggested experiments

- Sweep candidate proposal counts `k = 1, 4, 8, 16, 32`.
- Compare entropy, expected posterior size, worst-case bucket, and answer probability.
- Allow only remaining answers versus all legal exploratory words.
- Measure one-step scoring against depth-2 search with several beam widths.
- Remove deterministic filtering while preserving the same number of model calls.
- Compare LLM reranking and deterministic reranking on identical candidate sets.
- Evaluate late-game states separately, where exact constraint tracking matters most.
- Profile runtime and memory as candidate-set size changes.

## Questions to answer

- How much of the base model’s deficit comes from violating deterministic constraints?
- Does the LLM add value beyond a strong solver, and in which states?
- When is a non-answer exploratory guess preferable to a likely answer?
- Does entropy correlate with eventual solve rate under the six-turn limit?
- How quickly do deeper search returns diminish relative to compute?
- Are comparisons fair when one variant silently makes more model calls?

## Deliverables

- A tested deterministic candidate filter and partition scorer.
- A modular policy pipeline with interchangeable generator, validator, scorer, and selector.
- At least four system variants evaluated on the frozen benchmark.
- Search configuration files for depth, beam width, proposal count, and scoring objective.
- A performance profile including cache hit rate, latency, and evaluated branches.
- An ablation table separating gains from constraint filtering, proposal diversity, ranking, and lookahead.
- A written conclusion explaining what remains a learned-model capability after deterministic reasoning is externalized.

**Exit criterion:** the best hybrid result is reproducible, and every gain can be assigned to a named component rather than an opaque “agent” pipeline.
# Problem 07 — Inference-Time Scaling and Compute–Quality Tradeoffs

## Objective

Implement and compare multiple inference-time scaling methods for a state-to-next-guess policy, then quantify the tradeoff between additional computation and game performance. Your final result must include a **Pareto curve of inference compute versus win rate** and enough accounting detail to explain every point on that curve. At minimum, study direct decoding, repeated sampling, candidate reranking, and an explicit search method. The comparison must reveal whether more compute is being used productively rather than merely producing more text.

This assignment focuses on algorithms and measurement. Training a larger model is not the primary intervention. All methods should operate from the same fixed model checkpoint or from clearly separated, predeclared checkpoints, and every method must be evaluated on the same held-out game instances. Compute budgets must be enforced rather than estimated after the fact.

## Background

A learned policy can improve at inference time by considering several candidate actions, scoring them, simulating future outcomes, or combining model confidence with a symbolic objective. Repeated sampling can increase action diversity; self-consistency can identify stable choices; reranking can use model log-probability, a learned value model, or an entropy heuristic; beam or tree search can reason across multiple future turns. These approaches are not directly comparable unless computation is counted consistently.

Floating-point operation estimates alone may be unavailable or misleading when systems combine neural inference with CPU-side candidate enumeration. Conversely, wall-clock latency depends strongly on hardware and batching. You must therefore report multiple compute proxies: model forward passes, input and output tokens, sampled candidates, game-state expansions, reference-solver evaluations, and measured latency. Define a primary normalized compute unit for Pareto analysis, but retain the raw components so another researcher can reinterpret the comparison.

## Exact Requirements

1. Implement a common policy interface that accepts a state, a hard compute budget, a seed, and a method configuration, and returns a legal action plus a structured computation trace.
2. Include at least these methods:
   - deterministic direct decoding as a minimal-compute baseline;
   - stochastic sampling at multiple sample counts, with deduplication of candidate guesses;
   - candidate reranking using at least two scoring signals or combinations, such as model likelihood, expert entropy score, a learned value estimate, or simulated expected outcome;
   - an explicit search procedure such as beam search over action sequences, best-first search, Monte Carlo tree search, or rollout search.
3. Add at least one hybrid method that combines neural proposal with symbolic evaluation or search. The symbolic component may inspect only information legitimately available from the current game state.
4. Define no fewer than five total inference budgets spanning at least an order of magnitude in the primary compute unit. Every algorithm must halt at or below the assigned budget, including failed samples, parsing retries, and search expansions.
5. Ensure that methods share the same legal action set, state representation, stopping rules, model checkpoint, tokenizer, and evaluation game instances. Any exception must be documented and separately analyzed.
6. Count all inference-time work: prompt tokens, generated tokens, model forward passes or calls, candidate proposals, unique candidates, reranker evaluations, game simulations, expanded nodes, entropy computations, and retries. Cache hits must be logged and charged according to a stated policy.
7. Define the primary compute unit before viewing final test results. It may be estimated FLOPs, model-equivalent forward passes, or a calibrated cost model combining token generation and symbolic operations. Provide the calibration procedure and raw measurements.
8. Generate a Pareto plot with compute on the horizontal axis and win rate on the vertical axis. Mark dominated points, show uncertainty intervals, and distinguish methods. Also provide a table containing every plotted point.
9. Evaluate on enough independent held-out games to resolve a five-percentage-point win-rate difference with reasonable uncertainty, or provide a statistical power analysis explaining the chosen sample count.
10. Use multiple seeds for stochastic methods. Pair seeds and game instances where possible so that comparisons benefit from paired statistical tests.
11. Predeclare tie-breaking, invalid-output handling, timeouts, maximum context length, and behavior when a budget cannot support the requested search depth.
12. Save per-decision traces in a machine-readable format sufficient to reconstruct compute totals and inspect why the selected action won the internal comparison.

## Acceptance Criteria

- At least four qualitatively different inference strategies are implemented through one shared interface and evaluated at multiple enforced budgets.
- A budget auditor verifies that no trace exceeds its cap and that cached or failed operations are not omitted.
- The submitted Pareto curve can be regenerated exactly from released per-game records and plotting code.
- Win-rate estimates include confidence intervals, and stochastic comparisons use repeated seeds or paired bootstrap analysis.
- At least one nontrivial scaling method improves over direct decoding at some budget, or the report presents credible negative evidence and diagnoses why scaling failed.
- Dominated configurations are identified using both point estimates and uncertainty-aware discussion rather than being hidden.
- Compute reporting includes raw neural, symbolic, token, latency, and cost-related quantities rather than only a bespoke aggregate score.
- Search has no access to the hidden target or future feedback except through legitimate simulation over the current candidate distribution.

## Expected Experiments

Sweep sampling counts such as 1, 2, 4, 8, 16, and 32 while comparing temperature and top-p settings chosen on validation data. For reranking, compare model likelihood alone, entropy alone, and a calibrated combination. Measure whether increasing samples still helps after duplicate proposals saturate. For search, sweep depth, branching factor, rollout count, or node budget while holding the total compute cap fixed. Compare neural-only search, symbolic-only selection, and neural-proposal-plus-symbolic-reranking. Run an experiment with caching enabled and disabled, and report both logical compute and actual latency effects. Include a policy that allocates compute adaptively based on state difficulty, then compare it to a fixed-budget policy with the same average compute.

## What to Measure/Metrics

The primary quality measure is end-to-end win or solve rate under a fixed game protocol. Also report average guesses to solve, median and tail guess count, expert-action agreement, tie-aware agreement, action regret under the reference score, legal-output rate, and performance by state difficulty and turn. Compute metrics must include input/output tokens, forward passes, model calls, unique proposals, duplicate rate, reranker calls, entropy calculations, search nodes, rollouts, maximum resident memory, median and p95 latency, energy if available, and estimated monetary cost. Quantify marginal gain per doubling of compute and area under the compute–win-rate curve. Report confidence intervals for Pareto points and the frequency with which one method beats another on paired instances.

## Questions to Answer

1. Which method gives the largest early gain when moving above the direct-decoding budget?
2. At what budget does each method show diminishing returns, and what causes saturation?
3. Does sampling improve because of diversity, confidence aggregation, or increased opportunity for symbolic reranking?
4. How sensitive is the Pareto frontier to the chosen compute unit and hardware?
5. When does explicit lookahead outperform one-step entropy reranking?
6. Can adaptive compute allocation dominate fixed allocation at the same average cost?
7. Which states consume disproportionate search effort, and do they receive corresponding quality gains?
8. How would conclusions change if latency, dollar cost, or energy—not model-equivalent operations—were the binding constraint?

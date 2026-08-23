# Evaluation and Statistics

## Define the Primary Outcome

The main Wordle metric is **win rate**: the fraction of held-out games solved within six valid guesses. Report it as both a count and percentage, such as 736/1,000 = 73.6%. Counts make sample size visible and prevent a result from looking more precise than it is.

Secondary metrics explain how the system behaves: mean and median guesses among wins, distribution of finish turns, invalid-word rate, constraint-violation rate, model calls, generated tokens, wall-clock seconds per game, and peak RAM. For losses, record whether the solver exhausted six guesses, repeated a word, broke a known constraint, produced malformed output, or timed out.

Do not rely on one aggregate score. Two systems can both win 75% of games while one fails mostly on repeated letters and the other is slow but consistent.

## Confidence Intervals

A measured win rate is an estimate from a finite sample. A confidence interval communicates uncertainty. For a binomial outcome, Wilson intervals are a good default, especially for small samples or rates near zero or one. A difference of two percentage points is not persuasive if both intervals are wide.

Use at least enough games that the interval is meaningful for the claim. A 20-game demo can catch crashes but cannot support a near-SOTA conclusion. Freeze a larger held-out target list before tuning.

## Paired Comparisons and Bootstrap

Evaluate competing systems on the **same target words**. This paired design removes variation caused by one system receiving harder games. For each target, record system A's outcome and system B's outcome. The paired difference is then estimated across targets.

A paired bootstrap repeatedly samples target indices with replacement, preserving both systems' results for each sampled target. Compute the win-rate difference on every resample, then use percentiles for a confidence interval. The same technique can compare guesses used or seconds per game. Set and report the bootstrap seed and number of resamples.

Paired analysis answers a useful question: on this fixed benchmark, how consistently did the new method improve over the baseline? It is stronger than comparing two separately sampled averages.

## Difficulty Slices

Aggregate results can hide where gains occur. Predefine slices such as repeated-letter targets, uncommon-letter targets, large versus small candidate sets after turn two, early failures, late-game near-collisions, and frequent versus rare words. Report sample size for every slice. Avoid inventing a slice only after seeing a surprising result unless you label the analysis exploratory.

Build a failure taxonomy and assign each loss one primary cause:

- invalid or malformed model output;
- violated green/yellow/letter-count constraint;
- legal but low-information guess;
- unlucky high-information branch;
- candidate filter bug;
- repeated-letter handling error;
- search or timeout failure.

Review a random sample of failures as well as the worst-looking ones. This prevents memorable anecdotes from replacing statistics.

## Compute–Performance Tradeoffs

A local system must be evaluated on resource use, not API cost. Measure wall-clock latency, model calls, generated tokens, CPU-hours, and peak RAM. Separate model-loading time from steady-state game time. Use the same machine, power mode, thread settings, and warm-up procedure when comparing configurations.

Plot win rate against seconds per game and peak memory. A configuration is **Pareto dominated** if another configuration is at least as accurate, no slower, and uses no more memory, with one strict improvement. The remaining configurations form a Pareto frontier: each offers a real tradeoff.

For example, direct decoding may achieve 61% at 0.8 seconds/game, four-sample reranking 72% at 3.0 seconds, and MCTS 73% at 20 seconds. MCTS is not automatically “best” because it wins one additional point; its local latency may be unacceptable.

## A Reproducible Evaluation Protocol

Version the word lists and benchmark targets. Log model revision, quantization, prompt template, decoding settings, random seeds, hardware, software versions, and commit hash. Never tune on the final test set. Use a development set for prompt and hyperparameter choices, then run the final benchmark once the design is frozen.

Good evaluation does more than produce a leaderboard number. It tells you whether the gain is likely real, which games improved, what failures remain, and how much local computation the improvement requires.

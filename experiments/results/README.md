# Experiment results

Each run writes to a new immutable directory named
`<UTC timestamp>-<experiment>-s<seed>-<suffix>/`.

Required files:

- `config.yaml` — fully resolved configuration, including overrides.
- `environment.json` — Python, PyTorch, Transformers, CUDA, GPU, and Git commit.
- `metrics.json` — aggregate metrics and confidence intervals.
- `games.jsonl` — one record per game: target, guesses, feedback, win, latency,
  model calls, generated tokens, and candidate counts.
- `stdout.log` — captured progress and warnings.
- `artifacts/` — plots, checkpoints, or sampled model outputs.

Do not hand-edit run directories. Add a new run for every change, including prompt
changes. Keep target order and random seed fixed when making paired comparisons.
Never commit model checkpoints or large per-token traces; store them externally and
record their content hash and URI. Small metric summaries and plots should be
committed. Add failed runs too, with a `failure.json` describing the exception and
the last completed game.

A comparison table should report win rate, a bootstrap 95% confidence interval,
average guesses among wins, invalid-output rate, calls/game, tokens/game, and
seconds/game. State the hardware and whether model loading time is excluded.

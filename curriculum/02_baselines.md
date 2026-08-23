# Module 2 — Establish Trustworthy Baselines

## Why this module matters

A research project needs a measured starting point. Without baselines, an apparent improvement may simply come from an easier test set, a favorable first guess, answer leakage, or extra inference calls. This module builds a comparison ladder from trivial policies to a strong reference. Your goal is not to obtain an impressive number yet; it is to create a benchmark that makes later numbers meaningful.

## Learning objectives

By the end of this module, you should be able to:

- Define a fixed, held-out Wordle benchmark with uncertainty estimates.
- Implement random and heuristic non-neural policies.
- Evaluate an unmodified 0.2B–0.5B language model through a stable interface.
- Measure prompted and unprompted behavior separately.
- Select and document a strong reference policy.
- Compare quality, latency, tokens, calls, and estimated compute fairly.
- Diagnose invalid outputs and common evaluation leakage.

## Baseline ladder

Build at least five baselines:

1. **Random valid guess:** sample uniformly from allowed guesses, optionally restricted to consistent candidates after feedback.
2. **Simple heuristic:** use letter frequency or positional frequency, with a deterministic tie-breaker.
3. **Base small LLM:** load a public 0.2B–0.5B model and ask for the next word with minimal formatting. Suitable candidates include [SmolLM](https://huggingface.co/HuggingFaceTB), [Qwen2-0.5B](https://huggingface.co/Qwen), or another documented model in range.
4. **Prompted small LLM:** provide rules, history, and an explicit output schema, but no training.
5. **Strong reference:** a high-capability model such as GPT-4-class, Claude-class, or Llama 70B; alternatively, use a strong entropy solver or carefully measured human-expert policy. Record the exact model/version or algorithm.

Useful resources:

- [Hugging Face Transformers generation](https://huggingface.co/docs/transformers/main_classes/text_generation)
- [PyTorch reproducibility](https://pytorch.org/docs/stable/notes/randomness.html)
- [SciPy bootstrap confidence intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [ML experiment tracking with W&B](https://docs.wandb.ai/) or [MLflow](https://mlflow.org/docs/latest/)

## Metrics and protocol

The primary metric is solve rate within six valid turns. Secondary metrics should include mean and median guesses among wins, guess-count distribution, invalid-word rate, failures to obey the output format, per-turn survival/solve curves, and performance by answer difficulty. Record model calls, generated tokens, wall-clock latency, peak memory, and—where feasible—estimated FLOPs or cost.

Create one immutable test answer list before tuning prompts. Use the same target order for all policies. Report a confidence interval, not only a point estimate. If API cost prevents evaluating a reference on the full set, predeclare a stratified subset and evaluate all compared policies on that same subset.

## Suggested experiments

1. Compare unconstrained random guessing with random guessing from the remaining consistent set.
2. Compare global letter-frequency and positional-frequency heuristics.
3. Run the base LLM at greedy decoding and at several temperatures.
4. Measure how often free-form output parsing changes the apparent result; then enforce an exact five-letter schema.
5. Compare a fixed opening word with each policy’s preferred opening.
6. Repeat sampled decoding across multiple seeds and quantify variance.
7. Stratify answers by repeated letters, frequency, and initial candidate-set size.

## Questions to answer

- What is the weakest baseline that still uses feedback correctly?
- Does the base model fail because it chooses poor words, violates constraints, or produces invalid text?
- Is the strong reference truly comparable in available information and number of calls?
- How large must the test set be to distinguish a five-percentage-point improvement?
- Which metrics reveal behavior hidden by win rate?
- What counts as inference compute when comparing local and hosted models?

## Deliverables

- A versioned benchmark manifest containing test targets, seed, environment version, and policy settings.
- Implementations of random and heuristic policies.
- A common adapter for local and optional hosted LLM policies.
- A baseline results table with confidence intervals and compute/cost columns.
- Saved raw trajectories and an error taxonomy for invalid or failed games.
- A concise baseline report stating the observed gap between the small model and strong reference.

**Exit criterion:** every later experiment can be compared against this frozen benchmark without changing its rules, targets, or accounting method.
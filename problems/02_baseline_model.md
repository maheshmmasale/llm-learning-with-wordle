# Problem 2: Establish a Small-Language-Model Wordle Baseline

## Module context

Without baselines, an apparent improvement may come from an easier test set,
a lucky first guess, answer leakage, or extra inference calls. Build the
comparison ladder — random, heuristic, base model, prompted model, strong
reference — before trying to improve anything.

- Theory: `theory/01_ablations.md`, `theory/06_evaluation_and_statistics.md`
- Reference solution: `solutions/02_baseline/`
- Maintained library: `src/evaluation/` (run it now:
  `python -m src.evaluation.benchmark --policy solver --limit 50`)

## Objective

Build and evaluate a reproducible baseline in which a small pretrained language model plays the deterministic Wordle environment. The target model scale is approximately 0.2–0.5 billion parameters. The deliverable should define a stable inference pipeline, a robust output parser, and a fixed benchmark protocol that measures win rate, average guesses, and invalid-guess rate. It must also compare the small model with a clearly identified strong reference model under the same game rules and answer schedule.

## Background

Language models do not naturally interact with Wordle as stateful agents. A model receives a textual representation of prior guesses and feedback, generates unconstrained text, and must have some portion of that text interpreted as the next five-letter guess. Every design choice in this bridge—prompt formatting, decoding settings, parser rules, retry policy, and context construction—can affect measured performance. A baseline that omits these details is not reproducible, and a parser that silently repairs arbitrary model output may measure the repair code more than the model.

The experiment should use the deterministic Wordle class and validated word lists from Problem 1. The hidden answer must never appear in the model prompt, logs available to the model, parser diagnostics fed back into context, or other agent-visible state. Use a fixed benchmark answer schedule so every compared model sees the same targets. The small model should be an openly identifiable checkpoint in the 0.2–0.5B range and loaded with a documented framework, revision, dtype, device policy, and tokenizer. The strong reference model may be substantially larger or accessed through another inference route, but comparison requires equivalent prompting intent, game protocol, parsing standards, and opportunity to guess.

This assignment is about establishing an honest floor and a trustworthy harness, not maximizing scores through extensive prompt engineering. Prompt exploration belongs in the next problem. Here, select one simple baseline prompt in advance, freeze it, and characterize how the model behaves.

## Exact Requirements

1. Load a named pretrained causal language model with approximately 0.2–0.5 billion parameters. Pin or record the exact model identifier, revision or commit, tokenizer version, inference library versions, dtype, and hardware/device configuration.
2. Make generation reproducible. Specify and set all relevant seeds, deterministic framework settings where feasible, decoding parameters, maximum generated tokens, stopping conditions, and chat-template behavior. If exact bitwise reproducibility is not achievable on the chosen backend, characterize the remaining source of variation.
3. Define a single baseline prompt that explains the task, feedback symbols, valid response format, and previous-game state without revealing the answer. Keep it fixed throughout the benchmark.
4. Implement a deterministic parser that converts raw model text into at most one proposed five-letter guess. Document case normalization, punctuation handling, multiple candidates, quoted words, explanatory text, empty output, Unicode, and malformed tokens.
5. Do not silently substitute an oracle-selected legal word when parsing fails or the model proposes an invalid word. Define a bounded retry or reprompt policy, if any, and count every invalid proposal. Clarify whether invalid proposals consume environmental attempts, model turns, or both.
6. Record raw generation, parsed output, validity decision, accepted guess, feedback, and terminal status for every turn. Keep hidden targets in evaluator-only records and ensure they never enter subsequent prompts.
7. Evaluate on a fixed, reproducibly ordered benchmark drawn from the answer list. The benchmark must be large enough to make rates meaningful; justify its size and include the exact answer-selection seed or immutable answer manifest.
8. Report at minimum win rate, average accepted guesses, average model turns, and invalid-guess rate. Define denominators precisely. Report conditional average guesses among wins as well as an all-games measure that handles losses explicitly.
9. Evaluate a strong reference model against exactly the same answer schedule and six-guess game limit. Identify the model and inference configuration. Avoid giving it privileged target information, extra attempts, or parser repair unavailable to the small model.
10. Provide an executable benchmark entry point and machine-readable per-game results sufficient to recompute every aggregate. The benchmark must resume safely or overwrite intentionally without mixing configurations.

## Acceptance Criteria

- The chosen small model falls within the stated 0.2–0.5B scale and can complete the benchmark using the documented setup.
- Two runs with identical settings produce the same answer order, parsed guesses, and aggregate results, or any backend nondeterminism is quantified with repeated-run evidence.
- The parser has unit tests covering clean guesses, verbose answers, multiple five-letter strings, punctuation, invalid vocabulary entries, blank output, and malformed Unicode.
- Benchmark artifacts include configuration metadata and one record per game and turn.
- Win rate, average guesses, and invalid-guess rate are reported with explicit formulas and denominators.
- The strong reference model is evaluated fairly under the same environment, answer schedule, prompt intent, parser policy, and attempt budget.
- Manual inspection of a sample of transcripts confirms no target leakage.
- Failed generations, timeouts, and parsing failures are retained as failures rather than dropped from the benchmark.

## Expected Experiments

Run a small smoke test first to validate prompt construction, parser behavior, logging, and game termination. Freeze the baseline configuration before executing the primary benchmark. Run the small model twice with the same seeds and compare raw text, parsed guesses, complete transcripts, and aggregate metrics. If the platform is nondeterministic, run enough replicates to estimate variability and distinguish parser determinism from generation variability.

Evaluate the strong reference model on the identical answer order. Stratify outcomes by answer characteristics such as repeated letters, uncommon letters, and whether the answer was previously proposed as an invalid or duplicate guess. Perform parser audits on a random transcript sample and on every failure mode. Optionally compare greedy decoding with one predeclared seeded sampling configuration, but do not search settings against the test answers.

## What to Measure/Metrics

Measure game-level win rate, loss rate, accepted guesses per win, accepted guesses per game, model turns per game, invalid proposals per turn, parse-failure rate, duplicate-guess rate, and fraction of games exhausting the model-turn budget before six accepted guesses. Report median and distribution of guesses, not only means. Include total inference tokens, latency or throughput, and benchmark completion rate when feasible. For comparison, report absolute and relative differences between the small and strong models, paired per-answer outcome differences, and uncertainty intervals from an appropriate paired or bootstrap analysis.

## Questions to Answer

1. Which part of observed failure comes from language reasoning, output-format compliance, vocabulary mismatch, or parser behavior?
2. What exact conditions make the generation pipeline reproducible, and which remain platform-dependent?
3. How sensitive are reported averages to the treatment of losses and invalid proposals?
4. Does the strong reference model improve mainly by winning more games, using fewer guesses, or producing fewer invalid outputs?
5. Are repeated-letter answers disproportionately difficult for either model?
6. Could any log field, retry message, or exception inadvertently expose the target to the next model call?
7. Is the benchmark large and fixed enough to support later prompt comparisons without test-set tuning?

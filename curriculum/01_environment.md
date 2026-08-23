# Module 1 — Build a Deterministic Wordle Environment

## Why this module matters

Before testing a language model, you need an environment whose behavior is exact, reproducible, and independently testable. Wordle looks simple, but repeated letters create subtle correctness bugs. A flawed evaluator can reward illegal behavior, leak the answer, or make later results impossible to trust. In this module, you will treat the environment as scientific infrastructure rather than incidental game code.

## Learning objectives

By the end of this module, you should be able to:

- Specify Wordle as a deterministic, finite-horizon decision process.
- Implement exact green/yellow/gray feedback, including repeated letters.
- Separate the answer list from the larger allowed-guess list.
- Design a minimal API suitable for humans, LLMs, solvers, and batch evaluation.
- Represent game state without exposing the hidden target.
- Build property-based and example-based tests for correctness.
- Make evaluation reproducible through seeded sampling and versioned word lists.

## Key concepts and resources

A game state contains prior guesses, feedback for each guess, the turn count, terminal status, and optionally derived constraints. The target belongs inside the environment and must never appear in the observation passed to a model. Use a stable feedback encoding such as `0=gray`, `1=yellow`, `2=green`; display emojis only at the UI boundary.

Feedback should be computed in two passes: first mark exact-position matches and decrement their letter counts; then mark yellow letters only while unmatched counts remain. This prevents a guess such as `EERIE` from receiving too many yellow marks against a target containing one `E`.

Recommended reading:

- [Official Wordle introduction](https://www.nytimes.com/games/wordle/index.html)
- [Python `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [pytest documentation](https://docs.pytest.org/)
- [Hypothesis property-based testing](https://hypothesis.readthedocs.io/)
- [Gymnasium environment design](https://gymnasium.farama.org/api/env/)

## Suggested API

Implement a small interface such as:

```python
env = WordleEnv(answer_words, allowed_guesses, max_turns=6)
obs, info = env.reset(target="cigar")
obs, reward, terminated, truncated, info = env.step("crane")
```

The observation should contain public information only. Decide whether invalid guesses consume a turn, and document the policy. Provide pure helper functions such as `score_guess(target, guess)` and `filter_candidates(words, history)` so they can be tested without creating an environment instance. Add serialization for states used in prompts and datasets.

## Suggested experiments

1. **Repeated-letter test matrix:** Construct at least 25 hand-verified target/guess pairs covering zero, one, and multiple repeated letters.
2. **Exhaustive self-match:** Verify that every answer scored against itself returns five greens.
3. **Candidate consistency:** For thousands of sampled games, confirm that the true target is never removed by the candidate filter.
4. **Determinism:** Run the same seeded benchmark twice and compare every target, guess, and feedback token.
5. **Throughput:** Measure games or `score_guess` calls per second. This will matter when generating hundreds of thousands of examples.
6. **API adversarial tests:** Check uppercase input, nonalphabetic input, incorrect length, unknown words, post-terminal actions, and duplicate reset calls.

## Questions to answer

- What information is part of the hidden simulator state versus the model-visible observation?
- Why does a one-pass yellow-letter algorithm fail?
- Should every dictionary word be an allowable answer? Why or why not?
- How will you version and cite the word lists?
- Which invariants make environment bugs easy to detect?
- Can a model infer the target from any unintended field in `info`, logs, or serialized prompts?

## Deliverables

- A documented `WordleEnv` implementation and pure feedback function.
- Versioned answer and allowed-guess lists with provenance and licenses.
- Unit and property-based tests, including repeated-letter cases.
- A command-line demo that plays one game without revealing the target.
- A batch runner that accepts a seed and emits machine-readable trajectories.
- A short environment report describing API choices, invalid-action policy, test coverage, throughput, and known limitations.

**Exit criterion:** another person can install the repository, run the tests, reproduce a fixed set of games, and trust that no target information is exposed to the player policy.
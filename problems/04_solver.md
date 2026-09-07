# Problem 4: Deterministic Constraint Solver and Hybrid LLM Agent

## Module context

A model may know useful word statistics while failing at exact bookkeeping.
Separate the two: the solver owns feasibility, the model ranks or selects.
This decomposition also tells you what the model actually contributes.

- Theory: `theory/04_search_and_solver.md`
- Reference solution: `solutions/04_solver/`
- Maintained library: `src/search/` (tested by `tests/test_search.py`)

## Objective

Implement a deterministic Wordle candidate-constraint solver that exactly preserves all answer candidates consistent with observed guesses and feedback, including repeated-letter cases. Integrate the solver into an evaluation framework that compares three agent conditions: an LLM acting alone, a deterministic solver acting alone, and a hybrid in which the solver constructs the legal candidate set while an LLM ranks or selects among candidates. The goal is to separate constraint correctness from strategic ranking and language-model behavior.

## Background

Every Wordle feedback row imposes constraints on the hidden answer. Greens fix letters at positions. Yellows establish presence while excluding specific positions. Blacks usually eliminate letters, but repeated letters complicate that interpretation: if a guess contains two copies of a letter and only one receives a non-black mark, the answer contains exactly one usable occurrence, not zero. Across multiple guesses, the solver must reconcile positional restrictions with lower and upper bounds on letter counts.

A robust way to define consistency is behavioral: a candidate is consistent with a history if scoring each prior guess against that candidate reproduces the exact recorded feedback. This definition provides a useful oracle for testing any optimized constraint representation. The assignment requires a deterministic filter, but does not prescribe its internal algorithm. Whatever representation is chosen must correctly capture repeated letters and be auditable against the game engine.

The hybrid condition should not let the LLM invent out-of-set words and call them solver-assisted. The solver owns feasibility; the LLM’s role is ranking or selection among a supplied, deterministic candidate set. Because a full-size answer list may exceed practical prompt limits, the system must define a reproducible candidate-presentation or ranking interface without using the hidden answer. Comparisons must use the same fixed benchmark, environment, vocabularies, and game budget.

## Exact Requirements

1. Implement a deterministic function or class that accepts public guess-feedback history and returns exactly the answer-list words consistent with every row.
2. Correctly handle repeated letters by enforcing positional constraints and letter-count bounds implied by mixed green, yellow, and black marks. A letter marked black in one position must not be globally eliminated when another occurrence of that letter is green or yellow in the same guess.
3. Define candidate consistency in relation to the authoritative Wordle scorer. Provide a simple oracle check that rescoring all historical guesses against a candidate reproduces the history, then test the production filter against it.
4. Preserve deterministic ordering. Given the same answer list and history, the candidate sequence and any downstream tie-breaking must be identical across runs and processes.
5. Reject impossible, malformed, or contradictory histories explicitly. Do not return a fabricated fallback candidate when the set is empty. Include diagnostics that reveal violated public constraints without revealing the actual target.
6. Implement a solver-only policy. It must choose guesses deterministically using a documented ranking criterion, tie-break rule, and policy for whether guesses may come from the full valid-guess list or only the remaining answer candidates.
7. Implement an LLM-alone condition using the frozen baseline or selected prompt and parser policy. It must not receive candidate sets or solver-derived private information.
8. Implement a solver-plus-LLM condition in which the deterministic solver first filters candidates and the LLM ranks or selects among allowed options. Define how candidates are presented when the set is large, how truncation or pre-ranking works, and how the final choice is validated as belonging to the permitted set.
9. If the hybrid LLM outputs an invalid or out-of-set choice, record the event and apply a fixed fallback policy that does not consult the target. The fallback must be identical across all games and declared before evaluation.
10. Evaluate all three conditions—LLM alone, solver alone, and solver plus LLM ranking—on the same immutable answer schedule, word lists, maximum six accepted guesses, and scoring implementation.
11. Log candidate-set size before and after every accepted feedback row, selected guess, ranking inputs, output validity, feedback, and terminal state. Evaluator-only target fields must never enter model-visible data.
12. Include pytest tests and randomized or exhaustive differential tests emphasizing duplicate letters, histories with several repeated-letter clues, singleton candidate sets, empty sets, and contradictory histories.

## Acceptance Criteria

- For every tested history, the optimized filter returns exactly the same set as the rescore-based consistency oracle.
- Repeated-letter unit tests cover lower bounds, upper bounds, mixed black/non-black copies, multiple greens of one letter, and constraints accumulated across turns.
- Filtering is deterministic, preserves documented ordering, and never uses the hidden answer directly.
- Contradictory histories produce a clear empty-set or explicit error outcome according to the documented API.
- The solver-only policy and hybrid fallback have stable tie-breaking and produce identical transcripts under repeated runs.
- The hybrid’s submitted guess is always from the presented or otherwise permitted candidate set after fallback handling.
- All three systems are evaluated on paired benchmark answers, and per-game records allow every aggregate to be recomputed.
- No model prompt, ranking input, exception, or debug field exposes the benchmark target.

## Expected Experiments

First, validate filtering independently of agent strategy. Generate answers and legal or synthetic guess histories, then compare the production filter with brute-force rescoring over the full answer list. Include adversarial histories involving words with doubled and tripled letters. Test monotonicity: adding valid feedback cannot increase the candidate set. Test soundness by confirming the true answer remains in the set for genuine histories, and completeness by confirming every returned candidate reproduces all feedback.

Next, benchmark the three agent conditions on one fixed answer schedule. Use paired outcome tables to show where the solver rescues LLM failures, where the LLM ranking improves or harms solver guess efficiency, and where candidate presentation limits the hybrid. Run ablations on candidate-list size or deterministic pre-ranking only if they are predeclared and do not alter the primary comparison.

Analyze the trajectory of candidate-set sizes across turns. Pay particular attention to cases where the set unexpectedly becomes empty, shrinks insufficiently after informative feedback, or contains many anagrams. Audit all hybrid out-of-set outputs and fallbacks. Repeat the benchmark with identical seeds to verify transcript-level reproducibility.

## What to Measure/Metrics

For filtering, measure oracle agreement rate, false inclusion count, false exclusion count, empty-set frequency on valid histories, runtime per filter call, and candidate-set size before and after each turn. Report shrinkage ratio, median remaining candidates by turn, and separate statistics for answers with repeated letters.

For agents, report win rate, paired win-rate differences, average accepted guesses among wins, loss-adjusted guesses, invalid-guess rate, duplicate-guess rate, and six-turn exhaustion rate. For the hybrid, additionally measure out-of-set proposal rate, fallback rate, candidate-list size shown to the LLM, ranking token cost, and whether the chosen item’s deterministic rank predicts success. Include uncertainty intervals for paired comparisons and throughput or latency where operationally relevant.

## Questions to Answer

1. How does the implementation derive minimum and maximum occurrence counts from repeated-letter feedback?
2. What evidence shows the optimized filter is both sound and complete relative to rescoring?
3. When does solver-only performance exceed LLM-alone performance, and is the difference due to validity, constraint tracking, or ranking?
4. Does LLM ranking improve guess efficiency once feasibility is guaranteed, or does it underperform deterministic ranking?
5. How are large candidate sets reduced for the hybrid without introducing target leakage or nondeterminism?
6. What happens when the history is contradictory or the hybrid proposes an out-of-set word?
7. Are conclusions stable for repeated-letter answers, rare words, and late-game singleton candidate sets?

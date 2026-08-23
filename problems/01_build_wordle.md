# Problem 1: Build a Deterministic Wordle Environment

## Objective

Implement a production-quality, deterministic Wordle environment that can serve as the experimental foundation for later language-model and search-based agents. The environment must expose a small, well-documented guess API, apply official-style feedback rules—including the nontrivial handling of repeated letters—and support large-scale reproducible evaluation. The assignment is not merely to make a playable game: it is to create a trustworthy research instrument whose state transitions, input validation, randomization, and information boundaries can be tested independently.

## Background

Wordle asks a player to identify a hidden five-letter answer in at most six guesses. After each valid guess, the game returns one feedback symbol per character: 🟩 means that the letter is in the correct position, 🟨 means that the letter occurs elsewhere in the answer, and ⬛ means that the guessed letter cannot receive either of those matches. Repeated letters make feedback computation subtle. A guessed letter may appear more times than it occurs in the answer, and only the answer’s available occurrences may be colored green or yellow. Any implementation that independently checks whether each guessed letter appears somewhere in the answer will therefore be wrong.

The environment will later be used for controlled comparisons among prompting strategies, language models, and deterministic solvers. Small ambiguities can invalidate those comparisons. For example, a hidden answer accidentally included in serialized state would create target leakage; nondeterministic answer selection would make paired experiments incomparable; inconsistent word-list normalization could change the denominator of a reported win rate. Treat the environment as a compact benchmark package, not as a demo script.

Use two distinct vocabularies: a valid-guess list of approximately 12,000 five-letter words and an answer list of approximately 2,300 five-letter words. Every answer must be a valid guess, but most valid guesses need not be eligible answers. The exact checked-in sources and normalization policy must be documented so another researcher can recreate the effective lists.

## Exact Requirements

1. Implement a `Wordle` class with an explicit constructor and a deterministic reset mechanism. Its configuration must include the valid-guess vocabulary, answer vocabulary, maximum number of guesses, and either a supplied answer or a reproducible random seed.
2. Expose a guess API such as `guess(word)` that validates game state and input, records accepted guesses, and returns structured feedback. The public result must include the five feedback symbols and enough non-secret state to tell whether the game was won, lost, or remains active.
3. Enforce five-letter normalized words and reject guesses not in the valid list. Define whether normalization accepts uppercase input and surrounding whitespace. Invalid guesses must not consume an attempt unless the specification explicitly justifies a different choice.
4. Implement exact feedback using a two-stage allocation rule: correct-position matches must be accounted for before misplaced matches, and no answer-letter occurrence may be allocated more than once. Cover cases where the answer repeats a letter, the guess repeats a letter, or both do.
5. Use the symbols ⬛, 🟨, and 🟩 in the user-visible feedback representation. A machine-readable representation may also be provided, but its ordering and semantics must be documented.
6. Load and validate a roughly 12k-word valid-guess list and roughly 2.3k-word answer list. Fail loudly on malformed words, duplicates after normalization, or answers absent from the valid list. Record actual effective counts in test or benchmark output.
7. Prevent the hidden answer from leaking through normal public attributes, `repr`, returned dictionaries, logs, exceptions, or serialized observations before game termination. Internal implementation may retain the answer, but agent-facing state must not expose it.
8. Provide pytest coverage for state transitions, invalid inputs, terminal behavior, reproducibility, vocabulary invariants, all feedback colors, and adversarial repeated-letter examples.
9. Add a reproducibility test or benchmark that runs 1,000 complete games from a fixed seed or fixed answer schedule and demonstrates identical answers, transcripts, and aggregate outcomes across repeated runs.
10. Document API contracts, error behavior, seed semantics, answer-selection semantics, and any permitted access to the answer after termination. Do not couple the core engine to terminal input/output or a specific agent implementation.

## Acceptance Criteria

- All pytest tests pass in a clean environment and require no network access.
- The repeated-letter logic agrees with an independently specified oracle on exhaustive or broad property-based checks.
- A fixed seed produces the same 1,000-game answer sequence and identical feedback for identical guesses.
- Invalid words, malformed inputs, and post-terminal guesses behave consistently and do not corrupt state.
- Public observations and standard object representations do not reveal the target during an active game.
- Vocabulary validation confirms the expected scale (about 12,000 valid guesses and 2,300 answers), with the precise counts reported.
- The game ends after a correct guess or six accepted guesses by default, and status fields remain internally consistent.
- The implementation can be imported and driven programmatically without interactive prompts.

## Expected Experiments

Construct a compact test matrix of hand-designed answer/guess pairs emphasizing repeated letters. Include guesses with too many copies of a letter, answers with multiple copies, overlapping green and yellow matches, all-black guesses, and all-green guesses. Supplement examples with randomized differential tests against a separately written scoring oracle or mathematically stated invariants.

Run two independent 1,000-game sweeps using the same configuration and seed. Generate complete legal transcripts with a deterministic baseline policy, then compare per-game answers, accepted guesses, feedback, terminal states, and aggregate checksums. Repeat with a different seed to verify that the sequence changes while remaining valid. Also probe accidental leakage by inspecting documented public state, `repr`, exception messages, and common serialization paths during active games.

## What to Measure/Metrics

Report effective valid-list and answer-list sizes, duplicate and malformed-entry counts before cleaning, pytest case count, repeated-letter case count, and property-based examples executed if applicable. For reproducibility, report the seed, number of games, transcript checksum, number of mismatches across duplicate runs, and answer-frequency summary. Record invalid-guess handling, average accepted guesses in the deterministic sweep, win count, loss count, and any runtime or throughput measurement useful for later large benchmarks.

## Questions to Answer

1. What invariant guarantees that each answer-letter occurrence contributes to at most one green or yellow mark?
2. Which repeated-letter examples would fail under a naive “letter appears in answer” implementation?
3. What information is intentionally exposed to an agent after each guess, and what remains private?
4. How are seeds translated into answer schedules, and is behavior stable across processes?
5. What vocabulary normalization decisions were made, and could they change benchmark comparability?
6. How does the API distinguish invalid input, an already completed game, and an ordinary accepted guess?
7. What evidence demonstrates that the environment is sufficiently deterministic and leak-resistant for subsequent model evaluations?

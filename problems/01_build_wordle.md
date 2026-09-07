# Problem 1: Build a Deterministic Wordle Environment

## Module context

Before testing a language model, you need an environment whose behavior is
exact, reproducible, and independently testable. A flawed evaluator can
reward illegal behavior, leak the answer, or make later results untrustworthy.

- Theory: `theory/01_ablations.md`, `theory/06_evaluation_and_statistics.md`
- Reference solution: `src/solutions/01_environment/`
- Maintained library: `src/environment/`

## Objective

Build a trustworthy research instrument, not a playable game: a deterministic
`WordleEnv` with exact duplicate-letter scoring, strict input validation,
and a leak-proof public observation — testable independently of any agent.

## Requirements

1. `WordleEnv(target, allowed_guesses, max_turns=None)`; turns default to
   word length. Reference: `src/environment/wordle.py`.
2. `step(guess)` validates, records, and returns a turn with B/Y/G feedback
   (greens allocated before yellows; each answer letter used at most once).
   Status via `won`/`done`; `observe()` must never contain the target.
3. Normalize words of the list's length (5 default; 6–9 sets ship too);
   reject off-list guesses without consuming a turn.
4. Load `data/` lists with `src/environment/vocab.py`; fail loudly on
   malformed words or answers missing from guesses; report loader counts.
5. No leakage through attributes, `repr`, exceptions, logs, or serialized
   state during an active game.

## Done when

- `pytest tests/test_environment.py tests/test_vocab.py` passes, including
  adversarial repeated-letter cases (e.g. `ppppp` vs `apple` → `BGGBB`).
- A fixed seed reproduces identical 1,000-game transcripts across runs.
- Public observations inspected mid-game reveal nothing about the target.

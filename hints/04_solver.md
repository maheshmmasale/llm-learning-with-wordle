# Hints: Deterministic Solver and Search

> **Try without hints first.** The goal is not to hide all reasoning in a tool; it is to measure which responsibilities the model can perform reliably.

## Level 1 — Identify what is deterministic

Given a candidate answer, every previous guess has one exact feedback pattern. Therefore a word remains possible only if replaying every guess against it reproduces the observed feedback exactly.

This observation can produce a correct filter without manually writing a large set of special-case constraints.

## Level 2 — Separate constraint tracking from decision-making

Use a deterministic component to maintain legal candidates, then let the policy choose among actions. Compare at least:

- LLM alone,
- deterministic filter plus LLM ranking,
- deterministic filter plus algorithmic ranking/search.

This decomposition makes a meaningful claim possible: whether gains come from accurate bookkeeping, better action selection, or both.

## Level 3 — Filter by feedback equivalence

For each previous `(guess, observed_pattern)` and proposed candidate `word`, compute:

```text
score_guess(word, guess)
```

If the result differs from `observed_pattern`, reject `word`. This automatically handles duplicate letters if `score_guess` is correct.

Be careful to distinguish:

- the answer vocabulary from the allowed-guess vocabulary,
- selecting a possible answer from selecting an exploratory probe word,
- filtering candidates from ranking the next guess.

## Level 4 — Candidate filter sketch

```python
from collections.abc import Iterable, Sequence

Pattern = tuple[int, ...]
History = Sequence[tuple[str, Pattern]]

def is_consistent(candidate: str, history: History) -> bool:
    return all(
        score_guess(candidate, previous_guess) == observed
        for previous_guess, observed in history
    )


def filter_candidates(
    answer_words: Iterable[str], history: History
) -> list[str]:
    return [w for w in answer_words if is_consistent(w, history)]
```

Test invariants:

- the true target is never removed,
- adding evidence never enlarges the candidate set,
- equivalent histories produce the same set,
- duplicate-letter cases match the environment.

Once filtering is correct, create a separate scorer—candidate probability, expected entropy reduction, expected remaining set size, or lookahead value. Keeping filter and ranker separate will make later ablations clean.

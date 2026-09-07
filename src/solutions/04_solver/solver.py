"""Exact constraint-based Wordle solver with duplicate-letter support."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import log2
from typing import Iterable, Sequence

VALID_FEEDBACK = frozenset("GYB")


def score_guess(answer: str, guess: str) -> str:
    """Score ``guess`` against ``answer`` using Wordle's two-pass algorithm."""
    answer, guess = answer.lower(), guess.lower()
    if len(answer) != len(guess):
        raise ValueError("answer and guess must have the same length")
    marks = ["B"] * len(answer)
    remaining: Counter[str] = Counter()
    for i, (actual, proposed) in enumerate(zip(answer, guess)):
        if actual == proposed:
            marks[i] = "G"
        else:
            remaining[actual] += 1
    for i, proposed in enumerate(guess):
        if marks[i] == "B" and remaining[proposed]:
            marks[i] = "Y"
            remaining[proposed] -= 1
    return "".join(marks)


@dataclass(frozen=True)
class Constraints:
    """Human-readable constraints derived from the observation history."""

    fixed: tuple[str | None, ...]
    forbidden_positions: dict[str, frozenset[int]]
    minimum_counts: dict[str, int]
    maximum_counts: dict[str, int]


class ConstraintSolver:
    """Filter candidate answers by requiring exact feedback consistency.

    Exact replay is less error-prone than applying independent letter rules:
    a candidate survives only when it would have produced every observed
    pattern, including mixed green/yellow/gray copies of the same letter.
    """

    def __init__(self, candidates: Iterable[str]) -> None:
        words = tuple(dict.fromkeys(w.strip().lower() for w in candidates if w.strip()))
        if not words:
            raise ValueError("candidates must not be empty")
        self.word_length = len(words[0])
        if any(len(w) != self.word_length or not w.isalpha() for w in words):
            raise ValueError("candidates must be same-length alphabetic words")
        self._all = words
        self._remaining = words
        self.history: list[tuple[str, str]] = []

    @property
    def remaining(self) -> tuple[str, ...]:
        """Candidate answers consistent with all observations."""
        return self._remaining

    def reset(self) -> None:
        """Discard observations and restore the original candidate set."""
        self.history.clear()
        self._remaining = self._all

    def add_feedback(self, guess: str, feedback: str) -> tuple[str, ...]:
        """Apply one observation and return the surviving candidates.

        Feedback may be supplied in either case and must use G/Y/B. The solver
        accepts guesses outside the candidate answer list, as Wordle does.
        """
        guess, feedback = guess.strip().lower(), feedback.strip().upper()
        if len(guess) != self.word_length or not guess.isalpha():
            raise ValueError(f"guess must be an alphabetic {self.word_length}-letter word")
        if len(feedback) != self.word_length or set(feedback) - VALID_FEEDBACK:
            raise ValueError("feedback must contain exactly one G/Y/B mark per letter")
        self.history.append((guess, feedback))
        self._remaining = tuple(
            word for word in self._remaining if score_guess(word, guess) == feedback
        )
        return self._remaining

    def is_consistent(self, word: str) -> bool:
        """Return whether a word satisfies the complete observation history."""
        word = word.strip().lower()
        return len(word) == self.word_length and all(
            score_guess(word, guess) == feedback for guess, feedback in self.history
        )

    @property
    def constraints(self) -> Constraints:
        """Summarize positional and letter-count implications for inspection."""
        fixed: list[str | None] = [None] * self.word_length
        forbidden: dict[str, set[int]] = {}
        minimum: dict[str, int] = {}
        maximum: dict[str, int] = {}

        for guess, feedback in self.history:
            positive = Counter(letter for letter, mark in zip(guess, feedback) if mark != "B")
            total = Counter(guess)
            for letter, count in positive.items():
                minimum[letter] = max(minimum.get(letter, 0), count)
            # A gray occurrence alongside positive copies proves an exact upper bound.
            for letter, count in total.items():
                if count > positive[letter]:
                    maximum[letter] = min(maximum.get(letter, self.word_length), positive[letter])
            for index, (letter, mark) in enumerate(zip(guess, feedback)):
                if mark == "G":
                    fixed[index] = letter
                else:
                    forbidden.setdefault(letter, set()).add(index)

        return Constraints(
            tuple(fixed),
            {letter: frozenset(indices) for letter, indices in forbidden.items()},
            minimum,
            maximum,
        )

    def best_guess(self, allowed_guesses: Sequence[str] | None = None) -> str:
        """Choose the guess with maximum expected information gain.

        For each guess, surviving answers are partitioned by possible feedback;
        Shannon entropy ranks guesses. Ties prefer a possible answer and then
        lexical order. This exact method is intended for modest word lists.
        """
        if not self._remaining:
            raise RuntimeError("observations are contradictory; no candidates remain")
        guesses = self._remaining if allowed_guesses is None else tuple(
            dict.fromkeys(g.strip().lower() for g in allowed_guesses)
        )
        if not guesses or any(len(g) != self.word_length or not g.isalpha() for g in guesses):
            raise ValueError("allowed guesses must be same-length alphabetic words")

        n = len(self._remaining)

        def rank(guess: str) -> tuple[float, bool]:
            buckets = Counter(score_guess(answer, guess) for answer in self._remaining)
            entropy = -sum((size / n) * log2(size / n) for size in buckets.values())
            return entropy, guess in self._remaining

        # Sorting first makes equal-rank ties deterministic and lexical.
        return max(sorted(guesses), key=rank)

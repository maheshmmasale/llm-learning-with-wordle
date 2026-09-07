"""A small deterministic Wordle environment with official duplicate-letter scoring."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import random
from typing import Iterable, Optional

GREEN = "G"
YELLOW = "Y"
GRAY = "B"


def score_guess(answer: str, guess: str) -> str:
    """Return a G/Y/B pattern, consuming duplicate letters exactly once.

    Greens are assigned first.  Remaining answer letters are then consumed by
    yellows from left to right, matching Wordle's handling of repeated letters.
    """
    answer, guess = answer.lower(), guess.lower()
    if len(answer) != len(guess):
        raise ValueError("answer and guess must have the same length")

    result = [GRAY] * len(answer)
    remaining: Counter[str] = Counter()
    for i, (actual, proposed) in enumerate(zip(answer, guess)):
        if actual == proposed:
            result[i] = GREEN
        else:
            remaining[actual] += 1

    for i, proposed in enumerate(guess):
        if result[i] == GRAY and remaining[proposed] > 0:
            result[i] = YELLOW
            remaining[proposed] -= 1
    return "".join(result)


@dataclass(frozen=True)
class StepResult:
    """Result returned by :meth:`WordleEnv.step`."""

    guess: str
    feedback: str
    reward: float
    terminated: bool
    attempts_used: int


class WordleEnv:
    """Dependency-free Wordle environment with reproducible answer selection.

    Args:
        answers: Words from which answers are selected.
        allowed_guesses: Accepted guesses. Defaults to ``answers``.
        max_attempts: Number of guesses allowed per episode.
        seed: Seed for the environment-owned random generator.
    """

    def __init__(
        self,
        answers: Iterable[str],
        allowed_guesses: Optional[Iterable[str]] = None,
        max_attempts: int = 6,
        seed: int = 0,
    ) -> None:
        self.answers = self._clean_words(answers)
        if not self.answers:
            raise ValueError("answers must contain at least one word")
        self.word_length = len(self.answers[0])
        if any(len(word) != self.word_length for word in self.answers):
            raise ValueError("all answers must have the same length")

        guesses = self.answers if allowed_guesses is None else self._clean_words(allowed_guesses)
        if any(len(word) != self.word_length for word in guesses):
            raise ValueError("all allowed guesses must match the answer length")
        self.allowed_guesses = frozenset((*guesses, *self.answers))
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self.max_attempts = max_attempts
        self._rng = random.Random(seed)
        self.answer = ""
        self.history: list[tuple[str, str]] = []
        self.done = True

    @staticmethod
    def _clean_words(words: Iterable[str]) -> tuple[str, ...]:
        cleaned = tuple(dict.fromkeys(word.strip().lower() for word in words if word.strip()))
        if any(not word.isalpha() for word in cleaned):
            raise ValueError("words must contain letters only")
        return cleaned

    def reset(self, *, seed: Optional[int] = None, answer: Optional[str] = None) -> dict:
        """Start an episode and return an observation.

        Supplying ``answer`` is useful for evaluation. Supplying ``seed``
        restarts the deterministic random sequence.
        """
        if seed is not None:
            self._rng.seed(seed)
        if answer is None:
            self.answer = self._rng.choice(self.answers)
        else:
            answer = answer.strip().lower()
            if answer not in self.answers:
                raise ValueError("answer must be in the answer list")
            self.answer = answer
        self.history = []
        self.done = False
        return self.observation

    @property
    def observation(self) -> dict:
        """Return public episode state without exposing the answer."""
        return {
            "history": tuple(self.history),
            "attempts_remaining": self.max_attempts - len(self.history),
            "word_length": self.word_length,
        }

    def step(self, guess: str) -> StepResult:
        """Score one guess; reward is 1 only when the answer is found."""
        if self.done:
            raise RuntimeError("episode is finished; call reset()")
        guess = guess.strip().lower()
        if guess not in self.allowed_guesses:
            raise ValueError(f"guess is not allowed: {guess!r}")

        feedback = score_guess(self.answer, guess)
        self.history.append((guess, feedback))
        won = feedback == GREEN * self.word_length
        self.done = won or len(self.history) >= self.max_attempts
        return StepResult(guess, feedback, float(won), self.done, len(self.history))

"""Deterministic Wordle environment used by the starter implementation."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence


class Mark(str, Enum):
    ABSENT = "B"   # black/gray
    PRESENT = "Y"  # yellow
    CORRECT = "G"  # green


Feedback = tuple[Mark, ...]


def score_guess(target: str, guess: str) -> Feedback:
    """Score a guess with Wordle's two-pass duplicate-letter rule.

    Green matches consume target letters first; yellow matches then consume only
    the remaining letter counts. Thus, guessing two Es against a target with one
    E can never award two yellow/green marks.
    """
    target, guess = target.lower(), guess.lower()
    if len(target) != 5 or len(guess) != 5 or not target.isalpha() or not guess.isalpha():
        raise ValueError("target and guess must be five alphabetic characters")

    result = [Mark.ABSENT] * 5
    remaining: dict[str, int] = {}
    for i, (t, g) in enumerate(zip(target, guess)):
        if t == g:
            result[i] = Mark.CORRECT
        else:
            remaining[t] = remaining.get(t, 0) + 1
    for i, g in enumerate(guess):
        if result[i] is Mark.CORRECT:
            continue
        if remaining.get(g, 0) > 0:
            result[i] = Mark.PRESENT
            remaining[g] -= 1
    return tuple(result)


def feedback_code(feedback: Sequence[Mark | str]) -> str:
    """Return compact ``BYG`` feedback representation."""
    return "".join(Mark(x).value for x in feedback)


@dataclass(frozen=True)
class Turn:
    guess: str
    feedback: Feedback


class WordleEnv:
    """A six-turn deterministic Wordle game.

    A target is supplied by the evaluator, never included in observations.
    ``allowed_guesses`` controls validation independently of possible answers.
    """

    def __init__(self, target: str, allowed_guesses: Iterable[str], max_turns: int = 6):
        target = target.lower()
        self.allowed_guesses = {w.strip().lower() for w in allowed_guesses if len(w.strip()) == 5}
        if target not in self.allowed_guesses:
            raise ValueError("target must be in allowed_guesses")
        self._target = target
        self.max_turns = max_turns
        self.history: list[Turn] = []

    @property
    def done(self) -> bool:
        return self.won or len(self.history) >= self.max_turns

    @property
    def won(self) -> bool:
        return bool(self.history and self.history[-1].guess == self._target)

    def observe(self) -> tuple[Turn, ...]:
        """Return immutable public history; the target is intentionally omitted."""
        return tuple(self.history)

    def step(self, guess: str) -> Turn:
        """Validate and apply one guess."""
        if self.done:
            raise RuntimeError("game is already finished")
        guess = guess.strip().lower()
        if guess not in self.allowed_guesses:
            raise ValueError(f"invalid guess: {guess!r}")
        turn = Turn(guess, score_guess(self._target, guess))
        self.history.append(turn)
        return turn

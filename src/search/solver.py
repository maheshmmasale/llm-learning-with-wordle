"""Exact Wordle constraint filtering."""
from __future__ import annotations

from collections.abc import Iterable, Sequence

from src.environment.state import GuessRecord
from src.environment.wordle import feedback_code, score_guess


class ConstraintSolver:
    """Maintain possible targets by replaying exact Wordle feedback.

    Replay-based filtering is concise and automatically handles repeated-letter
    lower/upper bounds, unlike independent green/yellow/gray rules.
    """

    def __init__(self, answers: Iterable[str]):
        self.all_answers = tuple(dict.fromkeys(w.lower() for w in answers))
        self.history: list[GuessRecord] = []
        self.candidates = list(self.all_answers)

    def update(self, guess: str, feedback: str) -> list[str]:
        record = GuessRecord(guess.lower(), feedback.upper())
        self.history.append(record)
        self.candidates = [
            target for target in self.candidates
            if feedback_code(score_guess(target, record.guess)) == record.feedback
        ]
        return self.candidates.copy()

    def reset(self) -> None:
        self.history.clear()
        self.candidates = list(self.all_answers)

    def rebuild(self, history: Sequence[GuessRecord]) -> list[str]:
        self.reset()
        for record in history:
            self.update(record.guess, record.feedback)
        return self.candidates.copy()

"""Serializable public game-state structures."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable

from .wordle import Mark, score_guess


@dataclass(frozen=True)
class GuessRecord:
    guess: str
    feedback: str

    def __post_init__(self) -> None:
        if len(self.guess) != 5 or len(self.feedback) != 5:
            raise ValueError("guess and feedback must have length five")
        if any(c not in "BYG" for c in self.feedback):
            raise ValueError("feedback must use only B, Y, G")


@dataclass
class GameState:
    """Public Wordle history plus optional legal-candidate cache."""
    history: list[GuessRecord] = field(default_factory=list)
    candidates: list[str] | None = None

    def add(self, guess: str, feedback: str) -> None:
        self.history.append(GuessRecord(guess.lower(), feedback.upper()))

    def accepts(self, candidate: str) -> bool:
        """Return whether a possible target reproduces every observed pattern."""
        return all(
            "".join(m.value for m in score_guess(candidate, record.guess)) == record.feedback
            for record in self.history
        )

    def filter(self, words: Iterable[str]) -> list[str]:
        return [w for w in words if self.accepts(w)]

    def to_dict(self) -> dict[str, Any]:
        return {"history": [asdict(x) for x in self.history], "candidates": self.candidates}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        return cls([GuessRecord(**x) for x in data.get("history", [])], data.get("candidates"))

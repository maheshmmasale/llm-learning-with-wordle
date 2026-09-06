"""Aggregate metrics for reproducible Wordle evaluation."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from statistics import mean, median
from typing import Any, Iterable


@dataclass(frozen=True)
class GameResult:
    target: str
    won: bool
    guesses: int
    invalid_guesses: int = 0
    model_calls: int = 0
    generated_tokens: int = 0
    wall_seconds: float = 0.0
    trajectory: tuple[tuple[str, str], ...] = ()
    """Per-attempt (guess, feedback-code) pairs; invalid guesses map to "INVALID"."""


def summarize(results: Iterable[GameResult]) -> dict[str, Any]:
    """Compute metrics using all games; unsolved games count at max turns."""
    rows = list(results)
    if not rows:
        raise ValueError("cannot summarize zero games")
    wins = [r for r in rows if r.won]
    distribution = Counter(str(r.guesses) if r.won else "fail" for r in rows)
    total_calls = sum(r.model_calls for r in rows)
    return {
        "games": len(rows),
        "wins": len(wins),
        "win_rate": len(wins) / len(rows),
        "average_guesses_all": mean(r.guesses for r in rows),
        "average_guesses_wins": mean(r.guesses for r in wins) if wins else None,
        "median_guesses_wins": median(r.guesses for r in wins) if wins else None,
        "invalid_guess_rate": sum(r.invalid_guesses for r in rows) / max(1, sum(r.guesses + r.invalid_guesses for r in rows)),
        "guess_distribution": dict(sorted(distribution.items())),
        "model_calls": total_calls,
        "generated_tokens": sum(r.generated_tokens for r in rows),
        "tokens_per_game": sum(r.generated_tokens for r in rows) / len(rows),
        "wall_seconds": sum(r.wall_seconds for r in rows),
        "seconds_per_game": sum(r.wall_seconds for r in rows) / len(rows),
        "raw": [asdict(r) for r in rows],
    }

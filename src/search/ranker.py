"""Information-theoretic Wordle guess ranking."""
from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Sequence

from src.environment.wordle import feedback_code, score_guess


def pattern_histogram(guess: str, possible_targets: Sequence[str]) -> Counter[str]:
    """Count feedback partitions induced by a guess."""
    return Counter(feedback_code(score_guess(target, guess)) for target in possible_targets)


def entropy_bits(guess: str, possible_targets: Sequence[str]) -> float:
    """Expected information in bits under a uniform target prior."""
    n = len(possible_targets)
    if n == 0:
        return float("-inf")
    return -sum((count / n) * math.log2(count / n) for count in pattern_histogram(guess, possible_targets).values())


def expected_remaining(guess: str, possible_targets: Sequence[str]) -> float:
    """Expected candidate-set size after making ``guess``."""
    n = len(possible_targets)
    if n == 0:
        return float("inf")
    return sum(count * count for count in pattern_histogram(guess, possible_targets).values()) / n


def rank_guesses(
    guesses: Iterable[str],
    possible_targets: Sequence[str],
    *,
    top_k: int | None = None,
) -> list[tuple[str, float]]:
    """Rank guesses by entropy, preferring possible answers on exact ties."""
    possible = set(possible_targets)
    ranked = sorted(
        ((g, entropy_bits(g, possible_targets)) for g in guesses),
        key=lambda x: (x[1], x[0] in possible, x[0]),
        reverse=True,
    )
    return ranked[:top_k]

"""Vocabulary loading and validation utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable


def normalize_words(words: Iterable[str]) -> list[str]:
    """Normalize, validate, de-duplicate, and sort five-letter words."""
    cleaned = {w.strip().lower() for w in words}
    invalid = sorted(w for w in cleaned if len(w) != 5 or not w.isalpha() or not w.isascii())
    if invalid:
        preview = ", ".join(repr(w) for w in invalid[:5])
        raise ValueError(f"invalid five-letter words: {preview}")
    return sorted(cleaned)


def load_words(path: str | Path) -> list[str]:
    """Load one word per line; blank lines and ``#`` comments are ignored."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return normalize_words(line for line in lines if line.strip() and not line.lstrip().startswith("#"))


def split_vocabulary(answers: Iterable[str], guesses: Iterable[str]) -> tuple[list[str], list[str]]:
    """Return normalized answers and legal guesses, ensuring answers are legal."""
    answer_list = normalize_words(answers)
    guess_list = normalize_words(guesses)
    missing = set(answer_list) - set(guess_list)
    if missing:
        raise ValueError(f"{len(missing)} answers are absent from allowed guesses")
    return answer_list, guess_list

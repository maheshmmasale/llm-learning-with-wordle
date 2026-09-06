"""Vocabulary loading and validation utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable


def normalize_words(words: Iterable[str], length: int | None = None) -> list[str]:
    """Normalize, validate, de-duplicate, and sort words.

    When length is None it is inferred from the first word; every word must
    then share it. Pass length explicitly to enforce a given word length.
    """
    cleaned = [w.strip().lower() for w in words if w.strip()]
    if not cleaned:
        raise ValueError("no words to normalize")
    if length is None:
        length = len(cleaned[0])
    invalid = sorted(
        {w for w in cleaned if len(w) != length or not w.isalpha() or not w.isascii()}
    )
    if invalid:
        preview = ", ".join(repr(w) for w in invalid[:5])
        raise ValueError(f"invalid {length}-letter words: {preview}")
    return sorted(set(cleaned))


def load_words(path: str | Path) -> list[str]:
    """Load one word per line; blank lines and ``#`` comments are ignored."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return normalize_words(line for line in lines if line.strip() and not line.lstrip().startswith("#"))


def split_vocabulary(answers: Iterable[str], guesses: Iterable[str]) -> tuple[list[str], list[str]]:
    """Return normalized answers and legal guesses, ensuring answers are legal.

    Word length is inferred from the answers; guesses must match it, so a
    5-letter answer list can never pair with 6-letter guesses by accident.
    """
    answer_list = normalize_words(answers)
    guess_list = normalize_words(guesses, length=len(answer_list[0]))
    missing = set(answer_list) - set(guess_list)
    if missing:
        raise ValueError(f"{len(missing)} answers are absent from allowed guesses")
    return answer_list, guess_list

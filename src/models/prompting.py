"""Prompt construction and robust guess extraction."""
from __future__ import annotations

import re
from collections.abc import Sequence

from src.environment.state import GuessRecord

WORD_RE = re.compile(r"\b[a-zA-Z]{5}\b")


def render_history(history: Sequence[GuessRecord]) -> str:
    """Render state without ever mentioning the hidden target."""
    if not history:
        return "No guesses yet."
    return "\n".join(f"{i + 1}. {x.guess.upper()} -> {x.feedback}" for i, x in enumerate(history))


def build_prompt(
    history: Sequence[GuessRecord],
    *,
    candidates: Sequence[str] | None = None,
    request_reasoning: bool = False,
) -> str:
    """Build a compact instruction prompt with an output contract."""
    candidate_text = ""
    if candidates is not None:
        visible = ", ".join(w.upper() for w in candidates[:200])
        candidate_text = f"\nRemaining candidate answers ({len(candidates)}): {visible}"
    reasoning = (
        "Briefly check green positions, yellow exclusions, and letter multiplicities, then "
        if request_reasoning else ""
    )
    return (
        "You are selecting the next legal five-letter Wordle guess. Feedback uses G=correct "
        "position, Y=present elsewhere, B=absent after duplicate-letter accounting.\n"
        f"History:\n{render_history(history)}{candidate_text}\n"
        f"{reasoning}finish with exactly: GUESS: WORD"
    )


def extract_guess(text: str, allowed: set[str] | None = None) -> str | None:
    """Extract the first explicit/legal five-letter guess from model text."""
    explicit = re.search(r"GUESS\s*:\s*([A-Za-z]{5})\b", text, re.IGNORECASE)
    words = ([explicit.group(1)] if explicit else []) + WORD_RE.findall(text)
    for word in words:
        word = word.lower()
        if allowed is None or word in allowed:
            return word
    return None

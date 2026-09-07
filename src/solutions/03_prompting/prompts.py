"""Six progressively more structured Wordle prompting strategies."""

from __future__ import annotations

from collections.abc import Callable, Sequence

History = Sequence[tuple[str, str]]


def _history(history: History) -> str:
    return "\n".join(f"- {g.upper()} -> {f}" for g, f in history) or "- none"


def simple(history: History, length: int = 5) -> str:
    """Minimal task-only instruction."""
    return f"Play Wordle. History:\n{_history(history)}\nGive one {length}-letter guess."


def explain_feedback(history: History, length: int = 5) -> str:
    """Define the feedback alphabet explicitly."""
    return (
        f"Guess the hidden {length}-letter word. G means correct position, "
        "Y means present in another position, and B means absent (unless that "
        f"letter is duplicated).\nHistory:\n{_history(history)}\nReturn one guess."
    )


def dictionary_only(history: History, length: int = 5) -> str:
    """Constrain response syntax and word validity."""
    return (
        f"Solve this {length}-letter Wordle. Feedback: G=correct position, "
        f"Y=wrong position, B=not present.\n{_history(history)}\n"
        f"Output exactly one common lowercase {length}-letter dictionary word; "
        "no punctuation or explanation."
    )


def evidence_first(history: History, length: int = 5) -> str:
    """Ask the model to distinguish information gathering from solving."""
    return (
        f"Choose the best next guess for a {length}-letter Wordle. G=green, "
        f"Y=yellow, B=gray.\nHistory:\n{_history(history)}\n"
        "Prefer a likely solution; if evidence is sparse, prefer a valid word "
        "that tests frequent, distinct letters. Output only the final guess."
    )


def constraint_check(history: History, length: int = 5) -> str:
    """Direct the model to verify positional and multiplicity constraints."""
    return (
        f"Find the next {length}-letter Wordle guess.\nHistory:\n{_history(history)}\n"
        "Before choosing, internally enforce every green position, move every "
        "yellow to a different position, exclude gray letters, and respect "
        "duplicate counts (a gray copy can cap a letter already marked G/Y). "
        "Return only one lowercase word."
    )


def structured_reasoning(history: History, length: int = 5) -> str:
    """Use an explicit internal checklist while keeping output machine-readable."""
    return (
        f"Solve this {length}-letter Wordle. G=exact, Y=present elsewhere, "
        f"B=absent/excess duplicate.\nObservations:\n{_history(history)}\n"
        "Silently build: (1) fixed positions, (2) forbidden letter-position "
        "pairs, (3) minimum and maximum count for each letter, and (4) candidate "
        "words satisfying all constraints. Select the candidate with the best "
        "information value. Respond as JSON only: "
        '{"guess":"lowercase_word"}.'
    )


STRATEGIES: dict[str, Callable[[History, int], str]] = {
    "simple": simple,
    "explain_feedback": explain_feedback,
    "dictionary_only": dictionary_only,
    "evidence_first": evidence_first,
    "constraint_check": constraint_check,
    "structured_reasoning": structured_reasoning,
}


def build_prompt(strategy: str, history: History, length: int = 5) -> str:
    """Build a prompt by strategy name."""
    try:
        factory = STRATEGIES[strategy]
    except KeyError as exc:
        raise ValueError(f"unknown strategy {strategy!r}; choose from {sorted(STRATEGIES)}") from exc
    return factory(history, length)

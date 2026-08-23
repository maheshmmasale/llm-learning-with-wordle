#!/usr/bin/env python3
"""Generate supervised Wordle state/action examples using an entropy oracle.

Each JSONL row contains a machine-readable state plus a ``prompt``/``completion``
pair that can be consumed directly by the fine-tuning script in solution 06.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

Feedback = str  # Five characters: G=green, Y=yellow, B=absent.


def load_words(path: Path, length: int = 5) -> list[str]:
    """Load, normalize, and deduplicate alphabetic words of a fixed length."""
    words = {line.strip().lower() for line in path.read_text().splitlines()}
    result = sorted(word for word in words if len(word) == length and word.isalpha())
    if not result:
        raise ValueError(f"No {length}-letter words found in {path}")
    return result


def feedback(guess: str, answer: str) -> Feedback:
    """Return official Wordle-style feedback, including duplicate-letter rules."""
    marks = ["B"] * len(answer)
    remaining: Counter[str] = Counter()
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            marks[i] = "G"
        else:
            remaining[a] += 1
    for i, g in enumerate(guess):
        if marks[i] == "B" and remaining[g]:
            marks[i] = "Y"
            remaining[g] -= 1
    return "".join(marks)


def compatible(word: str, history: Sequence[tuple[str, Feedback]]) -> bool:
    """Whether ``word`` would reproduce every observation in ``history``."""
    return all(feedback(guess, word) == marks for guess, marks in history)


def entropy_bits(guess: str, candidates: Sequence[str]) -> float:
    """Expected information gain of a guess over a uniform answer posterior."""
    if not candidates:
        return 0.0
    buckets = Counter(feedback(guess, answer) for answer in candidates)
    total = len(candidates)
    return -sum((n / total) * math.log2(n / total) for n in buckets.values())


def best_entropy_guess(
    candidates: Sequence[str], allowed: Sequence[str], used: set[str]
) -> tuple[str, float]:
    """Choose the maximum-entropy unused guess with deterministic tie-breaking."""
    legal = (word for word in allowed if word not in used)
    scored = ((entropy_bits(word, candidates), word in candidates, word) for word in legal)
    try:
        score, _, word = max(scored)
    except ValueError as exc:
        raise RuntimeError("No unused guesses remain") from exc
    return word, score


def make_prompt(history: Sequence[tuple[str, Feedback]], candidates: Sequence[str], cap: int) -> str:
    """Render a compact instruction prompt; expose candidates only when practical."""
    turns = ", ".join(f"{g}:{m}" for g, m in history) or "none"
    visible = ", ".join(candidates) if len(candidates) <= cap else "omitted"
    return (
        "Choose one legal five-letter Wordle guess that maximizes expected information.\n"
        f"History (G=correct, Y=present, B=absent): {turns}\n"
        f"Remaining answers ({len(candidates)}): {visible}\nGuess:"
    )


def generate_rows(
    answers: Sequence[str],
    allowed: Sequence[str],
    episodes: int,
    max_turns: int,
    prompt_candidate_cap: int,
    rng: random.Random,
    include_answer: bool = False,
) -> Iterable[dict]:
    """Yield oracle trajectories sampled from the answer vocabulary."""
    for episode in range(episodes):
        target = rng.choice(answers)
        history: list[tuple[str, Feedback]] = []
        used: set[str] = set()
        for turn in range(1, max_turns + 1):
            candidates = [word for word in answers if compatible(word, history)]
            action, score = best_entropy_guess(candidates, allowed, used)
            row = {
                "episode": episode,
                "turn": turn,
                "state": {
                    "history": [{"guess": g, "feedback": m} for g, m in history],
                    "candidates": candidates,
                    "candidate_count": len(candidates),
                },
                "action": action,
                "entropy_bits": round(score, 6),
                "prompt": make_prompt(history, candidates, prompt_candidate_cap),
                "completion": " " + action,
            }
            if include_answer:
                row["answer"] = target
            yield row
            marks = feedback(action, target)
            history.append((action, marks))
            used.add(action)
            if marks == "G" * len(target):
                break


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True, help="One valid answer per line")
    parser.add_argument("--allowed", type=Path, help="Optional larger allowed-guess list")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL path")
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--max-turns", type=int, default=6)
    parser.add_argument("--prompt-candidate-cap", type=int, default=200)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--include-answer", action="store_true", help="Debug only; leaks the label")
    args = parser.parse_args()

    answers = load_words(args.answers)
    allowed = load_words(args.allowed) if args.allowed else answers
    allowed = sorted(set(allowed) | set(answers))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in generate_rows(
            answers, allowed, args.episodes, args.max_turns,
            args.prompt_candidate_cap, rng, args.include_answer,
        ):
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()

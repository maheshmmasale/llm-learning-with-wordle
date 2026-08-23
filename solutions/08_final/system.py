#!/usr/bin/env python3
"""Integrated neuro-symbolic Wordle solver using a LoRA model and search-time scaling."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

# Reuse the tested inference-time scaling component from solution 07.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "07_scaling"))
from inference import ScaledDecoder  # noqa: E402

History = list[tuple[str, str]]


def load_words(path: Path) -> list[str]:
    """Load normalized five-letter words."""
    words = sorted({line.strip().lower() for line in path.read_text().splitlines()})
    words = [word for word in words if len(word) == 5 and word.isalpha()]
    if not words:
        raise ValueError(f"No five-letter words in {path}")
    return words


def feedback(guess: str, answer: str) -> str:
    """Compute duplicate-aware Wordle feedback (G/Y/B)."""
    marks = ["B"] * 5
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


def entropy(guess: str, candidates: Sequence[str]) -> float:
    """Expected information gain under a uniform posterior."""
    counts = Counter(feedback(guess, answer) for answer in candidates)
    total = len(candidates)
    return -sum((n / total) * math.log2(n / total) for n in counts.values())


def remaining_answers(answers: Sequence[str], history: History) -> list[str]:
    """Filter answers to those exactly consistent with all observations."""
    return [
        word for word in answers
        if all(feedback(guess, word) == marks for guess, marks in history)
    ]


def prompt_for(history: History, candidates: Sequence[str], candidate_cap: int = 200) -> str:
    """Render the same prompt schema used by the dataset generator."""
    turns = ", ".join(f"{guess}:{marks}" for guess, marks in history) or "none"
    visible = ", ".join(candidates) if len(candidates) <= candidate_cap else "omitted"
    return (
        "Choose one legal five-letter Wordle guess that maximizes expected information.\n"
        f"History (G=correct, Y=present, B=absent): {turns}\n"
        f"Remaining answers ({len(candidates)}): {visible}\nGuess:"
    )


def extract_words(text: str, legal: set[str]) -> list[str]:
    """Extract unique legal guesses from a model continuation."""
    return list(dict.fromkeys(word.lower() for word in re.findall(r"\b[A-Za-z]{5}\b", text) if word.lower() in legal))


class WordleSystem:
    """Combine stochastic proposals, beam/search proposals, and an entropy verifier."""

    def __init__(self, decoder: ScaledDecoder, answers: list[str], allowed: list[str]) -> None:
        self.decoder = decoder
        self.answers = answers
        self.allowed = sorted(set(allowed) | set(answers))
        self.legal = set(self.allowed)

    def choose(
        self,
        history: History,
        samples: int = 16,
        oracle_candidates: int = 12,
        search_nodes: int = 0,
        reward_weight: float = 2.0,
    ) -> tuple[str, list[dict]]:
        """Propose guesses in several ways, then rerank with the symbolic verifier."""
        candidates = remaining_answers(self.answers, history)
        if not candidates:
            raise ValueError("Feedback history is inconsistent with the answer list")
        used = {guess for guess, _ in history}
        if len(candidates) == 1:
            return candidates[0], [{"text": candidates[0], "forced": True}]

        prompt = prompt_for(history, candidates)
        proposals: list[str] = []
        votes: Counter[str] = Counter()
        for completion in self.decoder.sample(prompt, n=samples, max_new_tokens=12):
            words = extract_words(completion, self.legal)
            proposals.extend(words)
            votes.update(words[:1])  # one semantic vote per sampled continuation
        for completion in self.decoder.beam(prompt, beams=8, returns=4, max_new_tokens=12):
            proposals.extend(extract_words(completion, self.legal))
        if search_nodes:
            searched = self.decoder.best_first_search(
                prompt, width=5, max_new_tokens=12, max_nodes=search_nodes, returns=4
            )
            for row in searched:
                proposals.extend(extract_words(row["text"], self.legal))

        # A symbolic shortlist guarantees useful choices even if generation is malformed.
        oracle = sorted(
            ((entropy(word, candidates), word in candidates, word) for word in self.allowed if word not in used),
            reverse=True,
        )[:oracle_candidates]
        proposals.extend(word for _, _, word in oracle)
        proposals = [word for word in dict.fromkeys(proposals) if word not in used]

        entropy_scale = max(math.log2(len(candidates)), 1.0)

        def verifier(completion: str) -> float:
            word = completion.strip().lower()
            information = entropy(word, candidates) / entropy_scale
            consensus = votes[word] / max(samples, 1)
            return information + 0.25 * consensus

        # Leading space matches the completion format produced by solution 05.
        ranked = self.decoder.rerank(
            prompt, [" " + word for word in proposals], verifier, reward_weight=reward_weight
        )
        diagnostics = [
            {
                "text": row.text.strip(),
                "model_logprob": round(row.model_logprob, 4),
                "verifier_reward": round(row.reward, 4),
                "combined_score": round(row.score, 4),
                "entropy_bits": round(entropy(row.text.strip(), candidates), 4),
                "votes": votes[row.text.strip()],
            }
            for row in ranked
        ]
        return ranked[0].text.strip(), diagnostics

    def play(
        self,
        target: str | None,
        max_turns: int,
        samples: int,
        search_nodes: int,
        reward_weight: float,
    ) -> bool:
        """Play against a known target, or prompt for feedback interactively."""
        history: History = []
        for turn in range(1, max_turns + 1):
            pool = remaining_answers(self.answers, history)
            guess, ranked = self.choose(
                history, samples=samples, search_nodes=search_nodes, reward_weight=reward_weight
            )
            print(json.dumps({
                "turn": turn,
                "remaining": len(pool),
                "guess": guess,
                "top_candidates": ranked[:5],
            }, indent=2))
            marks = feedback(guess, target) if target else input(f"Feedback for {guess} [G/Y/B]: ").strip().upper()
            if not re.fullmatch(r"[GYB]{5}", marks):
                raise ValueError("Feedback must contain exactly five G, Y, or B characters")
            history.append((guess, marks))
            if marks == "GGGGG":
                print(f"Solved in {turn} turn(s): {guess}")
                return True
        print(f"Not solved after {max_turns} turns; {len(remaining_answers(self.answers, history))} answers remain")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Base model id or path")
    parser.add_argument("--adapter", help="LoRA adapter from solution 06")
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--allowed", type=Path)
    parser.add_argument("--target", help="Simulate this answer; omit for interactive feedback")
    parser.add_argument("--max-turns", type=int, default=6)
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--search-nodes", type=int, default=0, help="Enable best-first proposals with this node budget")
    parser.add_argument("--reward-weight", type=float, default=2.0)
    args = parser.parse_args()

    answers = load_words(args.answers)
    allowed = load_words(args.allowed) if args.allowed else answers
    if args.target and args.target.lower() not in answers:
        parser.error("--target must occur in --answers")
    decoder = ScaledDecoder.from_pretrained(args.model, args.adapter)
    system = WordleSystem(decoder, answers, allowed)
    solved = system.play(
        args.target.lower() if args.target else None,
        args.max_turns,
        args.samples,
        args.search_nodes,
        args.reward_weight,
    )
    raise SystemExit(0 if solved else 1)


if __name__ == "__main__":
    main()

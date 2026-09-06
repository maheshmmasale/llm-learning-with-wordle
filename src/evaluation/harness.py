"""The one eval that matters: an LLM plays N Wordle games, we count
solved vs unsolved and time each game.

Protocol: targets are sampled WITH replacement from the answers file with
a fixed seed, so any N works (final grading uses 100,000). Same seed +
same model + same lists = identical scorecard, bit for bit except timing.

Usage (smoke test, no model needed)::

    python -m src.evaluation.harness --policy solver --games 200

Real grading run::

    python -m src.evaluation.harness --model <hf-id-or-path> --games 100000
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.environment.vocab import load_words
from src.evaluation.benchmark import (
    entropy_policy_factory,
    play_game,
    random_policy_factory,
    solver_policy_factory,
)

PolicyFactory = Callable[[], Callable[..., str]]


def run_harness(
    targets: Sequence[str],
    allowed_guesses: Sequence[str],
    policy_factory: PolicyFactory,
    *,
    max_turns: int | None = None,
) -> dict[str, Any]:
    """Play every target once; split results into solved vs unsolved."""
    allowed = set(allowed_guesses)
    results = [
        play_game(target, allowed, policy_factory(), max_turns=max_turns)
        for target in targets
    ]
    solved = [r for r in results if r.won]
    unsolved = [r for r in results if not r.won]
    return {
        "games": len(results),
        "solved": len(solved),
        "unsolved": len(unsolved),
        "trajectories": [
            {
                "target": r.target,
                "won": r.won,
                "seconds": r.wall_seconds,
                "turns": [
                    {"attempt": i + 1, "guess": guess, "feedback": fb}
                    for i, (guess, fb) in enumerate(r.trajectory)
                ],
            }
            for r in results
        ],
        "win_rate": len(solved) / len(results) if results else 0.0,
        "avg_seconds_solve": mean(r.wall_seconds for r in solved) if solved else None,
        "avg_seconds_fail": mean(r.wall_seconds for r in unsolved) if unsolved else None,
        "avg_attempts_solve": mean(r.guesses for r in solved) if solved else None,
        "model_calls": sum(r.model_calls for r in results),
        "invalid_guess_rate": (
            sum(r.invalid_guesses for r in results)
            / max(1, sum(r.guesses + r.invalid_guesses for r in results))
        ),
    }


def sample_schedule(answers: Sequence[str], games: int, seed: int) -> list[str]:
    """Draw the graded target schedule: N samples with replacement."""
    return random.Random(seed).choices(list(answers), k=games)


def main(argv: Sequence[str] | None = None) -> dict[str, Any]:
    parser = argparse.ArgumentParser(description="Grade an LLM at Wordle.")
    parser.add_argument("--model", default=None,
                        help="HF model id or local path (needs torch)")
    parser.add_argument("--policy", choices=("random", "solver", "entropy"),
                        default="solver", help="non-LLM smoke policies")
    parser.add_argument("--answers", default="data/answers.txt")
    parser.add_argument("--guesses", default="data/guesses.txt")
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-turns", type=int, default=None,
                        help="default: one turn per letter")
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    answers = load_words(args.answers)
    guesses = load_words(args.guesses)
    if args.model is not None:
        from src.models.agent import llm_policy_factory

        factory = llm_policy_factory(args.model, answers)
        label = args.model
    else:
        label = f"{args.policy} (smoke, not a model)"
        if args.policy == "random":
            factory = random_policy_factory(args.seed)
        elif args.policy == "solver":
            factory = solver_policy_factory(answers)
        else:
            factory = entropy_policy_factory(answers, guesses)

    summary = run_harness(
        sample_schedule(answers, args.games, args.seed),
        guesses, factory, max_turns=args.max_turns,
    )
    if args.output is not None:
        Path(args.output).write_text(json.dumps(summary, indent=2) + "\n")

    def fmt(seconds: float | None) -> str:
        return f"{seconds:.3f}s" if seconds is not None else "n/a"

    print(f"player   : {label}")
    print(f"games    : {summary['games']}")
    print(f"solved   : {summary['solved']}")
    print(f"unsolved : {summary['unsolved']}")
    print(f"win rate : {summary['win_rate']:.1%}")
    print(f"avg time per solve : {fmt(summary['avg_seconds_solve'])}")
    print(f"avg time per fail  : {fmt(summary['avg_seconds_fail'])}")
    print(f"avg tries per solve: {summary['avg_attempts_solve']}")
    return summary


if __name__ == "__main__":
    main()

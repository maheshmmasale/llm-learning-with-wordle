"""The grade. One eval: your LLM plays N Wordle games through the harness.

Score = solved/unsolved win rate (80 pts) + solve speed (20 pts).
Run it::

    python -m src.evaluation.autograde --model <hf-id-or-path> [--games N]

Final grading uses --games 100000. No model given: SKIP (nothing to grade).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.environment.vocab import load_words
from src.evaluation.harness import run_harness, sample_schedule

SPEED_TARGET_SECONDS = 5.0  # full game on CPU, per problems/08


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Grade a Wordle LLM.")
    parser.add_argument("--model", default=None)
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    if args.model is None:
        print("SKIP: no --model given, nothing to grade.")
        return 0

    from src.models.agent import llm_policy_factory

    answers = load_words(ROOT / "data/answers.txt")
    guesses = load_words(ROOT / "data/guesses.txt")
    summary = run_harness(
        sample_schedule(answers, args.games, args.seed),
        guesses,
        llm_policy_factory(args.model, answers),
    )
    win_rate = summary["win_rate"]
    avg_solve = summary["avg_seconds_solve"] or float("inf")
    speed = min(1.0, SPEED_TARGET_SECONDS / avg_solve)
    score = round(80 * win_rate + 20 * speed, 1)

    print(f"model    : {args.model}")
    print(f"games    : {summary['games']}")
    print(f"solved   : {summary['solved']}")
    print(f"unsolved : {summary['unsolved']}")
    print(f"win rate : {win_rate:.1%}  ({round(80 * win_rate, 1)}/80)")
    print(f"avg sec/solve: {avg_solve:.3f}  ({round(20 * speed, 1)}/20)")
    print(f"avg sec/fail : {summary['avg_seconds_fail'] or float('nan'):.3f}")
    print(f"SCORE: {score}/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

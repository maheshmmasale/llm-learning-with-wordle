"""Benchmark runner with deterministic target order and JSON output.

CLI usage (from the repository root)::

    python -m src.evaluation.benchmark --answers data/answers.txt \\
        --guesses data/guesses.txt --policy solver --limit 50 --seed 0
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

if __name__ == "__main__" and __package__ is None:  # allow `python src/.../benchmark.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.environment.state import GuessRecord
from src.environment.vocab import load_words, split_vocabulary
from src.environment.wordle import WordleEnv, feedback_code
from src.search.ranker import rank_guesses
from src.search.solver import ConstraintSolver

try:
    from .metrics import GameResult, summarize
except ImportError:  # direct script execution: `python src/evaluation/benchmark.py`
    from src.evaluation.metrics import GameResult, summarize

Policy = Callable[[tuple[Any, ...], set[str]], str]


def play_game(target: str, allowed: set[str], policy: Policy, max_turns: int = 6) -> GameResult:
    """Play one game; invalid policy outputs consume attempts to avoid free retries."""
    env = WordleEnv(target, allowed, max_turns=max_turns)
    invalid = calls = 0
    started = time.perf_counter()
    while not env.done:
        calls += 1
        guess = str(policy(env.observe(), allowed)).strip().lower()
        if guess not in allowed:
            invalid += 1
            # Count an invalid output against the fixed six-call interaction budget.
            if calls >= max_turns:
                break
            continue
        env.step(guess)
        if calls >= max_turns and not env.done:
            break
    return GameResult(
        target=target,
        won=env.won,
        guesses=len(env.history),
        invalid_guesses=invalid,
        model_calls=calls,
        wall_seconds=time.perf_counter() - started,
    )


def run_benchmark(
    targets: Sequence[str],
    allowed_guesses: Iterable[str],
    policy_factory: Callable[[], Policy],
    *,
    seed: int = 0,
    limit: int | None = None,
    output: str | Path | None = None,
) -> dict[str, Any]:
    """Evaluate a fresh policy per game and optionally atomically write JSON."""
    ordered = list(targets)
    random.Random(seed).shuffle(ordered)
    if limit is not None:
        ordered = ordered[:limit]
    allowed = set(allowed_guesses)
    results = [play_game(target, allowed, policy_factory()) for target in ordered]
    report = {"seed": seed, "targets": len(ordered), "metrics": summarize(results)}
    if output is not None:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        temporary.replace(destination)
    return report


def _history_records(history: tuple[Any, ...]) -> list[GuessRecord]:
    """Convert benchmark Turn history to solver-ready records."""
    return [GuessRecord(t.guess, feedback_code(t.feedback)) for t in history]


def random_policy_factory(seed: int = 0) -> Callable[[], Policy]:
    """Build a uniform-random-guess policy factory."""
    rng = random.Random(seed)

    def make() -> Policy:
        def policy(history: tuple[Any, ...], allowed: set[str]) -> str:
            used = {t.guess for t in history}
            pool = sorted(allowed - used) or sorted(allowed)
            return rng.choice(pool)

        return policy

    return make


def solver_policy_factory(answers: Sequence[str]) -> Callable[[], Policy]:
    """Build a constraint-filter policy factory (first live candidate)."""

    def make() -> Policy:
        solver = ConstraintSolver(answers)

        def policy(history: tuple[Any, ...], allowed: set[str]) -> str:
            candidates = solver.rebuild(_history_records(history))
            used = {t.guess for t in history}
            for word in candidates:
                if word in allowed and word not in used:
                    return word
            return min(allowed - used)

        return policy

    return make


def entropy_policy_factory(
    answers: Sequence[str], allowed_guesses: Sequence[str]
) -> Callable[[], Policy]:
    """Build a max-entropy-guess policy factory."""

    def make() -> Policy:
        solver = ConstraintSolver(answers)

        def policy(history: tuple[Any, ...], allowed: set[str]) -> str:
            candidates = solver.rebuild(_history_records(history)) or list(answers)
            used = {t.guess for t in history}
            pool = [w for w in allowed_guesses if w in allowed and w not in used]
            return rank_guesses(pool, candidates, top_k=1)[0][0]

        return policy

    return make


POLICIES = ("random", "solver", "entropy")


def main(argv: Sequence[str] | None = None) -> dict[str, Any]:
    """CLI entry point: run the benchmark and print aggregate metrics."""
    parser = argparse.ArgumentParser(description="Benchmark Wordle policies.")
    parser.add_argument("--answers", default="data/answers.txt")
    parser.add_argument("--guesses", default="data/guesses.txt")
    parser.add_argument("--policy", choices=POLICIES, default="solver")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-turns", type=int, default=6)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    answers, guesses = split_vocabulary(
        load_words(args.answers), load_words(args.guesses)
    )
    if args.policy == "random":
        factory = random_policy_factory(args.seed)
    elif args.policy == "solver":
        factory = solver_policy_factory(answers)
    else:
        factory = entropy_policy_factory(answers, guesses)
    report = run_benchmark(
        answers,
        guesses,
        factory,
        seed=args.seed,
        limit=args.limit,
        output=args.output,
    )
    metrics = report["metrics"]
    print(f"policy   : {args.policy}")
    print(f"games    : {metrics['games']}")
    print(f"won/lost : {metrics['wins']}/{metrics['games'] - metrics['wins']}")
    print(f"win rate : {metrics['win_rate']:.1%}")
    avg = metrics["average_guesses_wins"]
    print(f"avg tries (wins): {avg if avg is not None else 'n/a'}")
    return report


if __name__ == "__main__":
    main()

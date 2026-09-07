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
from src.utils.config import load_config

try:
    from .metrics import GameResult, summarize
except ImportError:  # direct script execution: `python src/evaluation/benchmark.py`
    from src.evaluation.metrics import GameResult, summarize

Policy = Callable[[tuple[Any, ...], set[str]], str]


def play_game(
    target: str, allowed: set[str], policy: Policy, max_turns: int | None = None
) -> GameResult:
    """Play one game; invalid policy outputs consume attempts to avoid free retries."""
    env = WordleEnv(target, allowed, max_turns=max_turns)
    budget = env.max_turns
    invalid = calls = 0
    trail: list[tuple[str, str]] = []
    started = time.perf_counter()
    while not env.done:
        calls += 1
        guess = str(policy(env.observe(), allowed)).strip().lower()
        if guess not in allowed:
            invalid += 1
            trail.append((guess, "INVALID"))
            # Count an invalid output against the interaction budget.
            if calls >= budget:
                break
            continue
        turn = env.step(guess)
        trail.append((turn.guess, feedback_code(turn.feedback)))
        if calls >= budget and not env.done:
            break
    return GameResult(
        target=target,
        won=env.won,
        guesses=len(env.history),
        invalid_guesses=invalid,
        model_calls=calls,
        wall_seconds=time.perf_counter() - started,
        trajectory=tuple(trail),
    )


def run_benchmark(
    targets: Sequence[str],
    allowed_guesses: Iterable[str],
    policy_factory: Callable[[], Policy],
    *,
    seed: int = 0,
    limit: int | None = None,
    output: str | Path | None = None,
    max_turns: int | None = None,
) -> dict[str, Any]:
    """Evaluate a fresh policy per game and optionally atomically write JSON."""
    ordered = list(targets)
    random.Random(seed).shuffle(ordered)
    if limit is not None:
        ordered = ordered[:limit]
    allowed = set(allowed_guesses)
    results = [
        play_game(target, allowed, policy_factory(), max_turns=max_turns)
        for target in ordered
    ]
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


def _config_section(args: argparse.Namespace) -> tuple[dict, dict, dict]:
    if args.config is None:
        return {}, {}, {}
    root = Path(__file__).resolve().parents[2]
    cfg = load_config(args.config if Path(args.config).is_absolute() else root / args.config)
    return cfg.get("data", {}), cfg.get("evaluation", {}), cfg.get("experiment", {})


def _resolve(path: str) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        return path
    return str(Path(__file__).resolve().parents[2] / candidate)


def main(argv: Sequence[str] | None = None) -> dict[str, Any]:
    """CLI entry point: run the benchmark and print aggregate metrics."""
    parser = argparse.ArgumentParser(description="Benchmark Wordle policies.")
    parser.add_argument("--config", default=None,
                        help="YAML config; explicit flags override it")
    parser.add_argument("--answers", default=None)
    parser.add_argument("--guesses", default=None)
    parser.add_argument("--policy", choices=POLICIES, default="solver")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max-turns", type=int, default=None,
                        help="default: one turn per letter")
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)
    data, evaluation, experiment = _config_section(args)

    answers_path = _resolve(args.answers or data.get("answers", "data/answers.txt"))
    guesses_path = _resolve(args.guesses or data.get("allowed_guesses", "data/guesses.txt"))
    seed = args.seed if args.seed is not None else experiment.get("seed", 0)
    max_turns = args.max_turns if args.max_turns is not None else evaluation.get("max_turns")
    answers, guesses = split_vocabulary(
        load_words(answers_path), load_words(guesses_path)
    )
    if args.policy == "random":
        factory = random_policy_factory(seed)
    elif args.policy == "solver":
        factory = solver_policy_factory(answers)
    else:
        factory = entropy_policy_factory(answers, guesses)
    output = args.output
    if output is None and args.config is not None:
        outdir = experiment.get("output_dir", "experiments/results")
        name = experiment.get("name", args.policy)
        output = str(Path(_resolve(outdir)) / f"{name}-s{seed}.json")
    report = run_benchmark(
        answers,
        guesses,
        factory,
        seed=seed,
        limit=args.limit,
        output=output,
        max_turns=max_turns,
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

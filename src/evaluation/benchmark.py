"""Benchmark runner with deterministic target order and JSON output."""
from __future__ import annotations

import json
import random
import time
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

from src.environment.wordle import WordleEnv
from .metrics import GameResult, summarize

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

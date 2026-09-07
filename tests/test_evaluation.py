"""Tests for src/evaluation: metrics, benchmark determinism, and the CLI."""

import json
from pathlib import Path

import pytest

from src.evaluation.benchmark import main, play_game, run_benchmark
from src.evaluation.metrics import GameResult, summarize

DATA = Path(__file__).resolve().parents[1] / "data"
ANSWERS = ["apple", "grape", "mango"]
ALLOWED = {"apple", "grape", "mango", "ppppp"}


def _first_candidate(history, allowed):
    return min(allowed)


def test_summarize_counts_and_distribution():
    rows = [
        GameResult("apple", True, 2),
        GameResult("grape", True, 4),
        GameResult("mango", False, 6),
    ]
    summary = summarize(rows)
    assert (summary["games"], summary["wins"]) == (3, 2)
    assert summary["win_rate"] == pytest.approx(2 / 3)
    assert summary["average_guesses_wins"] == pytest.approx(3.0)
    assert summary["guess_distribution"] == {"2": 1, "4": 1, "fail": 1}
    assert len(summary["raw"]) == 3


def test_summarize_rejects_empty():
    with pytest.raises(ValueError):
        summarize([])


def test_play_game_counts_invalid_outputs():
    result = play_game("apple", ALLOWED, lambda h, a: "zzzzz", max_turns=3)
    assert not result.won
    assert result.invalid_guesses == 3
    assert result.model_calls == 3


def test_benchmark_deterministic_and_writes_json(tmp_path):
    factory = lambda: _first_candidate
    first = run_benchmark(ANSWERS, ALLOWED, factory, seed=7)
    second = run_benchmark(ANSWERS, ALLOWED, factory, seed=7)
    timing = {"wall_seconds", "seconds_per_game", "raw"}
    stable = lambda m: {k: v for k, v in m.items() if k not in timing}
    assert stable(first["metrics"]) == stable(second["metrics"])
    outcome = lambda m: [(r["target"], r["won"], r["guesses"]) for r in m["raw"]]
    assert outcome(first["metrics"]) == outcome(second["metrics"])
    out = tmp_path / "report.json"
    run_benchmark(ANSWERS, ALLOWED, factory, seed=7, limit=2, output=out)
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["seed"] == 7 and saved["targets"] == 2
    assert not list(tmp_path.glob("*.tmp"))


def test_cli_main_reads_config_and_explicit_flags_win(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "r.json"
    report = main(
        [
            "--config", "experiments/configs/base.yaml",
            "--limit", "5",
            "--seed", "0",
            "--output", str(out),
        ]
    )
    assert report["metrics"]["games"] == 5
    assert out.is_file()
    assert (root / "experiments/configs/base.yaml").is_file()


def test_cli_main_runs_on_shipped_data():
    report = main(
        [
            "--answers", str(DATA / "answers.txt"),
            "--guesses", str(DATA / "guesses.txt"),
            "--policy", "solver",
            "--limit", "5",
            "--seed", "0",
        ]
    )
    assert report["metrics"]["games"] == 5
    assert report["metrics"]["wins"] == 5

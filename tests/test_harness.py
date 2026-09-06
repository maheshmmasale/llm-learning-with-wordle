"""Tests for the grading harness: solved/unsolved split and timing."""

from src.evaluation.harness import run_harness, sample_schedule

ANSWERS = ["apple", "grape", "mango"]
GUESSES = ["apple", "grape", "mango", "ppppp"]


def test_harness_splits_solved_unsolved():
    summary = run_harness(ANSWERS, GUESSES, lambda: (lambda h, a: min(a)))
    assert summary["games"] == 3
    assert summary["solved"] == 1  # min(allowed) == "apple" wins once
    assert summary["unsolved"] == 2
    assert summary["win_rate"] == 1 / 3


def test_harness_all_solved_reports_no_fail_time():
    summary = run_harness(["apple"], GUESSES, lambda: (lambda h, a: "apple"))
    assert (summary["solved"], summary["unsolved"]) == (1, 0)
    assert summary["avg_seconds_fail"] is None
    assert summary["avg_seconds_solve"] is not None
    assert summary["avg_seconds_solve"] >= 0
    assert summary["avg_attempts_solve"] == 1


def test_schedule_is_deterministic_and_sized():
    first = sample_schedule(ANSWERS, 1000, seed=0)
    assert first == sample_schedule(ANSWERS, 1000, seed=0)
    assert len(first) == 1000
    assert set(first) <= set(ANSWERS)

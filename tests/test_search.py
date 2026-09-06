"""Tests for src/search: constraint solver and entropy ranker."""

import math

from src.search.ranker import entropy_bits, expected_remaining, rank_guesses
from src.search.solver import ConstraintSolver

ANSWERS = ["apple", "grape", "mango", "peach", "berry"]


def test_solver_narrows_and_keeps_truth():
    solver = ConstraintSolver(ANSWERS)
    remaining = solver.update("ppppp", "BGGBB")
    assert "apple" in remaining
    assert "grape" not in remaining
    assert len(remaining) < len(ANSWERS)


def test_solver_rebuild_and_reset():
    solver = ConstraintSolver(ANSWERS)
    solver.update("ppppp", "BGGBB")
    solver.reset()
    assert solver.candidates == ANSWERS
    rebuilt = solver.rebuild(solver.history)
    assert rebuilt == ANSWERS  # empty history restores the full list


def test_entropy_prefers_splitting_guess():
    # "apple" splits the set; "berry"-style guess matches fewer patterns.
    assert entropy_bits("apple", ANSWERS) >= 0
    assert entropy_bits("zzzzz", ANSWERS) == 0
    assert entropy_bits("apple", []) == float("-inf")
    assert expected_remaining("apple", []) == float("inf")


def test_rank_guesses_sorted_top_k_and_tiebreak():
    ranked = rank_guesses(["apple", "grape", "mango"], ANSWERS, top_k=2)
    assert len(ranked) == 2
    assert ranked[0][1] >= ranked[1][1]
    full = rank_guesses(["apple", "grape", "mango"], ANSWERS)
    assert len(full) == 3
    assert all(isinstance(score, float) and math.isfinite(score) for _, score in full)

"""Tests for the reference Wordle environment."""

import pytest

from wordle import WordleEnv, score_guess


def test_exact_match_and_absent_letters() -> None:
    assert score_guess("cigar", "cigar") == "GGGGG"
    assert score_guess("cigar", "blunt") == "BBBBB"


def test_duplicate_guess_letters_are_consumed_once() -> None:
    # The answer has one L; the first guessed L is green, so the second is gray.
    assert score_guess("cello", "hello") == "BGGGG"
    assert score_guess("cigar", "array") == "BYBGB"


def test_duplicate_answer_letters_can_both_match() -> None:
    assert score_guess("level", "allee") == "BYYGY"


def test_seeded_resets_are_reproducible() -> None:
    first = WordleEnv(["cigar", "rebut", "sissy"], seed=17)
    second = WordleEnv(["cigar", "rebut", "sissy"], seed=17)
    assert [first.reset()["word_length"] and first.answer for _ in range(8)] == [
        second.reset()["word_length"] and second.answer for _ in range(8)
    ]


def test_episode_lifecycle() -> None:
    env = WordleEnv(["cigar", "rebut"], max_attempts=2)
    observation = env.reset(answer="cigar")
    assert observation["attempts_remaining"] == 2
    miss = env.step("rebut")
    assert miss.reward == 0.0 and not miss.terminated
    win = env.step("cigar")
    assert win.reward == 1.0 and win.terminated
    with pytest.raises(RuntimeError):
        env.step("cigar")

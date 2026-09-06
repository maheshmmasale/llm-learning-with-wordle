"""Tests for src/environment: scoring, state, vocab-adjacent env rules."""

import pytest

from src.environment.state import GameState, GuessRecord
from src.environment.wordle import Mark, WordleEnv, feedback_code, score_guess


@pytest.mark.parametrize(
    ("target", "guess", "expected"),
    [
        ("apple", "apple", "GGGGG"),
        ("apple", "rusty", "BBBBB"),
        ("apple", "ppppp", "BGGBB"),  # duplicate guess vs single answer letter
        ("apple", "leapt", "YYYYB"),  # yellows must not steal later greens
        ("apple", "allay", "GYBBB"),  # second A grey: single A used by green
        ("eerie", "reeve", "YGYBG"),
    ],
)
def test_score_guess_matrix(target, guess, expected):
    assert feedback_code(score_guess(target, guess)) == expected


@pytest.mark.parametrize(
    ("target", "guess"),
    [("apple", "app"), ("apples", "apple"), ("apple", "ab12!"), ("12345", "apple")],
)
def test_score_guess_rejects_malformed(target, guess):
    with pytest.raises(ValueError):
        score_guess(target, guess)


def test_score_guess_case_insensitive():
    assert feedback_code(score_guess("APPLE", "apple")) == "GGGGG"


@pytest.mark.parametrize(
    ("target", "guess", "expected"),
    [
        ("planet", "planet", "GGGGGG"),
        ("banana", "bandana"[:6], "GGGBYY"),
        ("captain", "captain", "GGGGGGG"),
        ("blanket", "blinker", "GGBGGGB"),
    ],
)
def test_score_guess_other_lengths(target, guess, expected):
    assert feedback_code(score_guess(target, guess)) == expected


def test_score_guess_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        score_guess("apple", "planets")


def test_env_other_length():
    env = WordleEnv("planet", ["planet", "garden", "coffee"])
    assert env.word_length == 6
    env.step("garden")
    turn = env.step("planet")
    assert turn.feedback == (Mark.CORRECT,) * 6
    assert env.won


def test_feedback_code_accepts_marks_and_strings():
    assert feedback_code([Mark.CORRECT, "Y", Mark.ABSENT, "B", "G"]) == "GYBBG"


def _env():
    return WordleEnv("apple", ["apple", "ppppp", "leapt", "grape"])


def test_win_and_history():
    env = _env()
    turn = env.step("apple")
    assert turn.guess == "apple"
    assert env.won and env.done
    assert isinstance(env.observe(), tuple)


def test_loss_after_six_turns():
    env = _env()
    for _ in range(6):
        env.step("ppppp")
    assert env.done and not env.won
    with pytest.raises(RuntimeError):
        env.step("apple")


def test_invalid_guess_rejected_without_consuming_turn():
    env = _env()
    with pytest.raises(ValueError):
        env.step("zzzzz")
    assert len(env.history) == 0


def test_target_must_be_allowed():
    with pytest.raises(ValueError):
        WordleEnv("mango", ["apple"])


def test_observation_never_exposes_target():
    env = _env()
    env.step("ppppp")
    assert "apple" not in repr(env.observe())


def test_guess_record_validation():
    with pytest.raises(ValueError):
        GuessRecord("apple", "GXBYY")
    with pytest.raises(ValueError):
        GuessRecord("app", "BBBBB")


def test_game_state_filter_keeps_true_target():
    state = GameState()
    state.add("ppppp", "BGGBB")
    assert "apple" in state.filter(["apple", "grape", "mango"])
    assert "grape" not in state.filter(["apple", "grape"])
    roundtripped = GameState.from_dict(state.to_dict())
    assert roundtripped.history == state.history

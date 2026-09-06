"""Tests for src/environment/vocab.py including the shipped data lists."""

from pathlib import Path

import pytest

from src.environment.vocab import load_words, normalize_words, split_vocabulary

DATA = Path(__file__).resolve().parents[1] / "data"


def test_normalize_dedupes_sorts_and_lowercases():
    assert normalize_words(["  Apple ", "apple", "CRANE"]) == ["apple", "crane"]


def test_normalize_rejects_bad_words_with_preview():
    with pytest.raises(ValueError, match="friend"):
        normalize_words(["apple", "friend", "toolongword"])


def test_load_words_skips_comments_and_blanks(tmp_path):
    path = tmp_path / "words.txt"
    path.write_text("# comment\n\napple\n\n# another\ncrane\n", encoding="utf-8")
    assert load_words(path) == ["apple", "crane"]


def test_split_requires_answers_in_guesses():
    with pytest.raises(ValueError, match="absent from allowed guesses"):
        split_vocabulary(["apple"], ["crane"])


def test_shipped_data_lists_validate():
    answers, guesses = split_vocabulary(
        load_words(DATA / "answers.txt"), load_words(DATA / "guesses.txt")
    )
    assert len(answers) >= 50
    assert len(guesses) > len(answers)
    assert set(answers) <= set(guesses)
    assert all(len(w) == 5 and w.isalpha() for w in guesses)


@pytest.mark.parametrize(
    ("answers_file", "guesses_file", "length", "min_answers"),
    [
        ("answers.txt", "guesses.txt", 5, 50),
        ("answers6.txt", "guesses6.txt", 6, 30),
        ("answers7.txt", "guesses7.txt", 7, 30),
    ],
)
def test_shipped_data_lists_all_lengths(
    answers_file, guesses_file, length, min_answers
):
    answers, guesses = split_vocabulary(
        load_words(DATA / answers_file), load_words(DATA / guesses_file)
    )
    assert len(answers) >= min_answers
    assert set(answers) <= set(guesses)
    assert all(len(w) == length for w in answers + guesses)


def test_split_rejects_mixed_lengths():
    with pytest.raises(ValueError):
        split_vocabulary(["apple"], ["planets"])

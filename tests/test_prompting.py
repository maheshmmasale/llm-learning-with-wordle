"""Tests for src/models/prompting.py: prompt building and guess extraction."""

from src.environment.state import GuessRecord
from src.models.prompting import build_prompt, extract_guess, render_history

ALLOWED = {"apple", "grape", "mango"}


def test_render_history_empty():
    assert render_history([]) == "No guesses yet."


def test_prompt_hides_target_and_states_contract():
    history = [GuessRecord("grape", "BBYBB")]
    prompt = build_prompt(history, candidates=["apple", "mango"])
    assert "GUESS: WORD" in prompt
    assert "GRAPE" in prompt  # past guesses are visible
    assert "APPLE" in prompt  # candidate list is visible
    assert "mango".upper() in prompt


def test_extract_prefers_explicit_guess_tag():
    text = "Reasoning about mango...\nGUESS: apple\nmaybe grape"
    assert extract_guess(text, ALLOWED) == "apple"


def test_extract_falls_back_to_first_legal_word():
    assert extract_guess("I think grape then mango", ALLOWED) == "grape"


def test_extract_returns_none_without_legal_word():
    assert extract_guess("I have no idea, zzzzz", ALLOWED) is None
    assert extract_guess("", ALLOWED) is None

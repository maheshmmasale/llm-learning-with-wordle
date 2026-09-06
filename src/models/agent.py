"""LLM player: turns a causal LM into a benchmark-ready Wordle policy.

The model proposes; the deterministic solver supplies candidates and the
fallback. Invalid model outputs are handled by the benchmark (they consume
a turn), so the score always reflects the model, never a repair loop.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from src.environment.state import GuessRecord
from src.environment.wordle import feedback_code
from src.models.prompting import build_prompt, extract_guess
from src.search.solver import ConstraintSolver

Policy = Callable[[tuple[Any, ...], set[str]], str]


def llm_policy_factory(
    model_name: str,
    answers: Sequence[str],
    *,
    temperature: float = 0.0,
    max_new_tokens: int = 64,
) -> Callable[[], Policy]:
    """Build an LLM-guess policy factory. Needs torch + transformers."""
    from src.models.model import Generator, load_model

    model, tokenizer = load_model(model_name)
    generate = Generator(model, tokenizer)

    def make() -> Policy:
        solver = ConstraintSolver(answers)

        def policy(history: tuple[Any, ...], allowed: set[str]) -> str:
            records = [
                GuessRecord(t.guess, feedback_code(t.feedback)) for t in history
            ]
            candidates = solver.rebuild(records)
            prompt = build_prompt(records, candidates=candidates)
            text = generate(
                prompt, max_new_tokens=max_new_tokens, temperature=temperature,
                do_sample=temperature > 0,
            )
            guess = extract_guess(text, allowed)
            if guess is not None and guess not in {t.guess for t in history}:
                return guess
            used = {t.guess for t in history}
            for word in candidates:
                if word in allowed and word not in used:
                    return word  # fallback: solver pick, model gets no credit
            return min(allowed - used)

        return policy

    return make

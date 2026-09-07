"""Run a greedy small-language-model baseline on the reference Wordle task."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Sequence

# Make the sibling reference environment importable when this file is run directly.
ENV_DIR = Path(__file__).resolve().parents[1] / "01_environment"
sys.path.insert(0, str(ENV_DIR))
from wordle import WordleEnv  # noqa: E402


@dataclass
class EvaluationResult:
    """Aggregate metrics for a benchmark run."""

    games: int
    wins: int
    total_attempts: int
    invalid_outputs: int

    @property
    def win_rate(self) -> float:
        return self.wins / self.games if self.games else 0.0

    @property
    def mean_attempts(self) -> float:
        return self.total_attempts / self.games if self.games else 0.0


class HFWordleBaseline:
    """Greedy Hugging Face causal-LM policy for Wordle."""

    def __init__(self, model_name: str, device: str = "auto") -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Install torch and transformers to run this baseline") from exc

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map=device,
        )
        self.model.eval()

    @staticmethod
    def make_prompt(history: Sequence[tuple[str, str]], word_length: int) -> str:
        """Create the intentionally simple zero-shot baseline prompt."""
        turns = "\n".join(f"{guess.upper()} -> {feedback}" for guess, feedback in history)
        if not turns:
            turns = "(no guesses yet)"
        return (
            f"Play Wordle. The hidden word has {word_length} letters. "
            "Feedback uses G=correct place, Y=present elsewhere, B=absent.\n"
            f"Previous guesses:\n{turns}\n"
            f"Reply with exactly one {word_length}-letter English word."
        )

    def generate(self, prompt: str, max_new_tokens: int = 16) -> str:
        """Generate a deterministic response from the loaded model."""
        messages = [{"role": "user", "content": prompt}]
        if getattr(self.tokenizer, "chat_template", None):
            text = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            text = prompt
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        with self.torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        completion = output[0, inputs["input_ids"].shape[1] :]
        return self.tokenizer.decode(completion, skip_special_tokens=True).strip()

    @staticmethod
    def extract_guess(text: str, allowed: set[str], length: int) -> str | None:
        """Extract the first generated dictionary word of the required length."""
        for token in re.findall(r"[A-Za-z]+", text.lower()):
            if len(token) == length and token in allowed:
                return token
        return None


def evaluate(
    policy: HFWordleBaseline,
    answers: Sequence[str],
    allowed_guesses: Sequence[str] | None = None,
    max_attempts: int = 6,
) -> EvaluationResult:
    """Evaluate one fixed episode per answer and return aggregate metrics."""
    answers = tuple(word.strip().lower() for word in answers)
    guesses = tuple(word.strip().lower() for word in (allowed_guesses or answers))
    allowed = set(guesses) | set(answers)
    env = WordleEnv(answers, guesses, max_attempts=max_attempts, seed=0)
    wins = total_attempts = invalid_outputs = 0

    for answer in answers:
        env.reset(answer=answer)
        used: set[str] = set()
        while not env.done:
            prompt = policy.make_prompt(env.history, env.word_length)
            raw = policy.generate(prompt)
            guess = policy.extract_guess(raw, allowed, env.word_length)
            if guess is None or guess in used:
                invalid_outputs += 1
                guess = next((w for w in guesses if w not in used), guesses[0])
            used.add(guess)
            result = env.step(guess)
        wins += int(env.history[-1][1] == "G" * env.word_length)
        total_attempts += len(env.history)

    return EvaluationResult(len(answers), wins, total_attempts, invalid_outputs)


def load_words(path: str) -> list[str]:
    """Load one lowercase alphabetic word per line, ignoring blank lines."""
    words = [line.strip().lower() for line in Path(path).read_text().splitlines()]
    words = [word for word in words if word]
    if not words or any(not word.isalpha() for word in words):
        raise ValueError("word file must contain one alphabetic word per line")
    return words


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("words", help="answer list, one word per line")
    parser.add_argument("--guesses", help="optional larger allowed-guess list")
    parser.add_argument(
        "--model",
        default="HuggingFaceTB/SmolLM-360M-Instruct",
        help="e.g. HuggingFaceTB/SmolLM-360M-Instruct or Qwen/Qwen2-0.5B-Instruct",
    )
    parser.add_argument("--device", default="auto", help="transformers device_map value")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    answers = load_words(args.words)[: args.limit]
    guesses = load_words(args.guesses) if args.guesses else answers
    result = evaluate(HFWordleBaseline(args.model, args.device), answers, guesses)
    print(f"games={result.games}")
    print(f"wins={result.wins}")
    print(f"win_rate={result.win_rate:.3f}")
    print(f"mean_attempts={result.mean_attempts:.2f}")
    print(f"invalid_outputs={result.invalid_outputs}")


if __name__ == "__main__":
    main()

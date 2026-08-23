#!/usr/bin/env python3
"""Inference-time scaling: self-consistency, reranking, beam, and best-first search."""

from __future__ import annotations

import argparse
import heapq
import json
import math
import re
from dataclasses import asdict, dataclass
from typing import Callable, Iterable

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


@dataclass
class RankedCandidate:
    """A candidate and the components of its reranking score."""

    text: str
    model_logprob: float
    reward: float
    score: float


class ScaledDecoder:
    """Reusable decoding and inference-time compute methods for a causal LM."""

    def __init__(self, model, tokenizer) -> None:
        self.model = model.eval()
        self.tokenizer = tokenizer
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
        self.device = next(model.parameters()).device

    @classmethod
    def from_pretrained(cls, model_name: str, adapter: str | None = None) -> "ScaledDecoder":
        """Load a base model and, optionally, a PEFT adapter."""
        tokenizer = AutoTokenizer.from_pretrained(adapter or model_name, use_fast=True)
        dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else None
        model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, device_map="auto" if torch.cuda.is_available() else None
        )
        if adapter:
            from peft import PeftModel

            model = PeftModel.from_pretrained(model, adapter)
        return cls(model, tokenizer)

    @torch.inference_mode()
    def sample(self, prompt: str, n: int = 8, temperature: float = 0.8,
               top_p: float = 0.95, max_new_tokens: int = 32) -> list[str]:
        """Draw independent continuations from the model."""
        batch = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(
            **batch,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            num_return_sequences=n,
            max_new_tokens=max_new_tokens,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        prefix = batch["input_ids"].shape[1]
        return [self.tokenizer.decode(row[prefix:], skip_special_tokens=True).strip() for row in output]

    def self_consistency(
        self,
        prompt: str,
        n: int = 16,
        normalize: Callable[[str], str] | None = None,
        **sample_kwargs,
    ) -> dict:
        """Sample many solutions and return the answer with the plurality vote.

        ``normalize`` should extract the semantic answer (for example, a final word)
        from a free-form continuation. Ties are resolved by mean model log-probability.
        """
        normalize = normalize or (lambda text: " ".join(text.lower().split()))
        samples = self.sample(prompt, n=n, **sample_kwargs)
        groups: dict[str, list[str]] = {}
        for text in samples:
            groups.setdefault(normalize(text), []).append(text)
        scored = []
        for key, members in groups.items():
            mean_lp = sum(self.sequence_logprob(prompt, text) for text in members) / len(members)
            scored.append((len(members), mean_lp, key))
        votes, _, answer = max(scored)
        return {
            "answer": answer,
            "votes": votes,
            "total_samples": n,
            "vote_counts": {key: len(value) for key, value in groups.items()},
            "samples": samples,
        }

    @torch.inference_mode()
    def sequence_logprob(self, prompt: str, completion: str) -> float:
        """Return mean conditional token log-probability of one completion."""
        prefix = self.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        suffix = self.tokenizer(completion, add_special_tokens=False)["input_ids"]
        if not suffix:
            return -math.inf
        if not prefix:
            bos = self.tokenizer.bos_token_id or self.tokenizer.eos_token_id
            prefix = [bos]
        ids = torch.tensor([prefix + suffix], device=self.device)
        logits = self.model(input_ids=ids).logits[0, :-1]
        log_probs = F.log_softmax(logits.float(), dim=-1)
        start = len(prefix) - 1
        positions = torch.arange(start, start + len(suffix), device=self.device)
        targets = ids[0, len(prefix):]
        return float(log_probs[positions, targets].mean())

    def rerank(
        self,
        prompt: str,
        candidates: Iterable[str],
        reward_fn: Callable[[str], float] | None = None,
        reward_weight: float = 1.0,
    ) -> list[RankedCandidate]:
        """Rerank candidates by conditional likelihood plus an external reward."""
        reward_fn = reward_fn or (lambda _: 0.0)
        rows = []
        for text in dict.fromkeys(candidates):
            model_score = self.sequence_logprob(prompt, text)
            reward = float(reward_fn(text))
            rows.append(RankedCandidate(text, model_score, reward, model_score + reward_weight * reward))
        return sorted(rows, key=lambda row: row.score, reverse=True)

    @torch.inference_mode()
    def beam(self, prompt: str, beams: int = 8, returns: int = 4,
             max_new_tokens: int = 32, diversity_penalty: float = 0.0) -> list[str]:
        """Generate high-likelihood sequences with beam or diverse-beam search."""
        batch = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        groups = beams if diversity_penalty > 0 else 1
        output = self.model.generate(
            **batch,
            do_sample=False,
            num_beams=beams,
            num_beam_groups=groups,
            diversity_penalty=diversity_penalty,
            num_return_sequences=min(returns, beams),
            max_new_tokens=max_new_tokens,
            early_stopping=True,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        prefix = batch["input_ids"].shape[1]
        return [self.tokenizer.decode(row[prefix:], skip_special_tokens=True).strip() for row in output]

    @torch.inference_mode()
    def best_first_search(
        self,
        prompt: str,
        width: int = 5,
        max_new_tokens: int = 32,
        max_nodes: int = 256,
        returns: int = 4,
        length_penalty: float = 0.7,
    ) -> list[dict]:
        """Search the token tree by normalized cumulative log-probability.

        Unlike fixed-width beam search, this uses a global priority queue, so compute
        can follow whichever partial hypothesis currently looks most promising.
        """
        prefix = self.tokenizer(prompt, add_special_tokens=True)["input_ids"]
        eos = self.tokenizer.eos_token_id
        serial = 0
        frontier = [(0.0, serial, prefix, 0.0)]
        finished: list[tuple[float, list[int], float]] = []
        expanded = 0

        def priority(logp: float, generated: int) -> float:
            norm = ((5.0 + max(generated, 1)) / 6.0) ** length_penalty
            return logp / norm

        while frontier and expanded < max_nodes and len(finished) < returns:
            _, _, ids, logp = heapq.heappop(frontier)
            generated = len(ids) - len(prefix)
            if generated >= max_new_tokens or (generated and ids[-1] == eos):
                finished.append((priority(logp, generated), ids, logp))
                continue
            tensor = torch.tensor([ids], device=self.device)
            next_logp = F.log_softmax(self.model(input_ids=tensor).logits[0, -1].float(), dim=-1)
            values, tokens = torch.topk(next_logp, k=width)
            for value, token in zip(values.tolist(), tokens.tolist()):
                serial += 1
                new_ids = ids + [token]
                score = logp + value
                heapq.heappush(frontier, (-priority(score, generated + 1), serial, new_ids, score))
            expanded += 1

        for _, _, ids, logp in frontier[: max(0, returns - len(finished))]:
            generated = len(ids) - len(prefix)
            finished.append((priority(logp, generated), ids, logp))
        finished.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "text": self.tokenizer.decode(ids[len(prefix):], skip_special_tokens=True).strip(),
                "score": score,
                "logprob_sum": logp,
            }
            for score, ids, logp in finished[:returns]
        ]


def word_normalizer(text: str) -> str:
    """Extract the first standalone five-letter word, useful for Wordle outputs."""
    match = re.search(r"\b[a-zA-Z]{5}\b", text)
    return match.group(0).lower() if match else text.strip().lower()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--method", choices=("self-consistency", "rerank", "beam", "search"), default="self-consistency")
    parser.add_argument("--candidate", action="append", default=[])
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    args = parser.parse_args()

    decoder = ScaledDecoder.from_pretrained(args.model, args.adapter)
    if args.method == "self-consistency":
        result = decoder.self_consistency(
            args.prompt, n=args.samples, normalize=word_normalizer,
            max_new_tokens=args.max_new_tokens,
        )
    elif args.method == "rerank":
        if not args.candidate:
            parser.error("--rerank requires at least one --candidate")
        result = [asdict(row) for row in decoder.rerank(args.prompt, args.candidate)]
    elif args.method == "beam":
        result = decoder.beam(args.prompt, max_new_tokens=args.max_new_tokens)
    else:
        result = decoder.best_first_search(args.prompt, max_new_tokens=args.max_new_tokens)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

"""Hugging Face causal-language-model loading and generation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_MODEL = "HuggingFaceTB/SmolLM-360M-Instruct"


def load_model(
    model_name: str = DEFAULT_MODEL,
    *,
    device_map: str | dict[str, Any] = "auto",
    dtype: str = "auto",
    trust_remote_code: bool = False,
):
    """Load tokenizer/model and ensure a usable padding token."""
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=trust_remote_code)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    torch_dtype: Any = dtype
    if dtype != "auto":
        torch_dtype = getattr(torch, dtype)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device_map,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
    )
    model.eval()
    return model, tokenizer


@dataclass
class Generator:
    """Small generation wrapper that returns continuations only."""
    model: Any
    tokenizer: Any

    @torch.inference_mode()
    def __call__(self, prompt: str, *, max_new_tokens: int = 32, **generation_kwargs: Any) -> str:
        batch = self.tokenizer(prompt, return_tensors="pt")
        device = next(self.model.parameters()).device
        batch = {k: v.to(device) for k, v in batch.items()}
        output = self.model.generate(
            **batch,
            max_new_tokens=max_new_tokens,
            pad_token_id=self.tokenizer.pad_token_id,
            **generation_kwargs,
        )
        continuation = output[0, batch["input_ids"].shape[1] :]
        return self.tokenizer.decode(continuation, skip_special_tokens=True).strip()

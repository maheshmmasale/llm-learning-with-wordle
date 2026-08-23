"""JSONL loading and tokenization for supervised Wordle examples."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from torch.utils.data import Dataset


class WordleSFTDataset(Dataset):
    """Tokenized prompt/completion dataset.

    Expected JSONL rows contain ``prompt`` and ``completion`` strings. Prompt
    tokens receive label ``-100`` so loss is computed on the answer only.
    """

    def __init__(self, path: str | Path, tokenizer: Any, max_length: int = 512):
        self.rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        self.tokenizer = tokenizer
        self.max_length = max_length
        if not self.rows:
            raise ValueError(f"empty dataset: {path}")
        for row in self.rows:
            if not isinstance(row.get("prompt"), str) or not isinstance(row.get("completion"), str):
                raise ValueError("each row requires string prompt and completion fields")

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, list[int]]:
        row = self.rows[index]
        prompt_ids = self.tokenizer(row["prompt"], add_special_tokens=True)["input_ids"]
        completion = row["completion"] + (self.tokenizer.eos_token or "")
        answer_ids = self.tokenizer(completion, add_special_tokens=False)["input_ids"]
        input_ids = (prompt_ids + answer_ids)[: self.max_length]
        prompt_length = min(len(prompt_ids), len(input_ids))
        labels = [-100] * prompt_length + input_ids[prompt_length:]
        return {"input_ids": input_ids, "attention_mask": [1] * len(input_ids), "labels": labels}


class CompletionOnlyCollator:
    """Pad inputs, masks, and labels while preserving ignored prompt labels."""

    def __init__(self, tokenizer: Any):
        self.tokenizer = tokenizer

    def __call__(self, features: list[dict[str, list[int]]]):
        import torch

        width = max(len(x["input_ids"]) for x in features)
        pad = self.tokenizer.pad_token_id
        right = self.tokenizer.padding_side != "left"
        rows = []
        for feature in features:
            n = width - len(feature["input_ids"])
            if right:
                rows.append((feature["input_ids"] + [pad] * n, feature["attention_mask"] + [0] * n, feature["labels"] + [-100] * n))
            else:
                rows.append(([pad] * n + feature["input_ids"], [0] * n + feature["attention_mask"], [-100] * n + feature["labels"]))
        return {key: torch.tensor([r[i] for r in rows], dtype=torch.long) for i, key in enumerate(("input_ids", "attention_mask", "labels"))}

#!/usr/bin/env python3
"""Supervised LoRA fine-tuning for prompt/completion JSON or JSONL datasets."""

from __future__ import annotations

import argparse
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from datasets import DatasetDict, load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    set_seed,
)


@dataclass
class CompletionCollator:
    """Dynamically pad causal-LM examples while preserving masked labels."""

    tokenizer: Any
    pad_to_multiple_of: int = 8

    def __call__(self, features: list[dict[str, list[int]]]) -> dict[str, torch.Tensor]:
        width = max(len(item["input_ids"]) for item in features)
        width = ((width + self.pad_to_multiple_of - 1) // self.pad_to_multiple_of) * self.pad_to_multiple_of
        ids, masks, labels = [], [], []
        for item in features:
            n = width - len(item["input_ids"])
            ids.append(item["input_ids"] + [self.tokenizer.pad_token_id] * n)
            masks.append(item["attention_mask"] + [0] * n)
            labels.append(item["labels"] + [-100] * n)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(masks, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Hugging Face model id or local path")
    parser.add_argument("--train-file", type=Path, required=True)
    parser.add_argument("--validation-file", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--gradient-accumulation", type=int, default=8)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument(
        "--target-modules",
        help="Comma-separated projection names (e.g. q_proj,v_proj); PEFT infers them if omitted",
    )
    parser.add_argument("--eval-fraction", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--resume-from-checkpoint")
    parser.add_argument("--gradient-checkpointing", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)

    files = {"train": str(args.train_file)}
    if args.validation_file:
        files["validation"] = str(args.validation_file)
    raw: DatasetDict = load_dataset("json", data_files=files)
    if "validation" not in raw:
        split = raw["train"].train_test_split(test_size=args.eval_fraction, seed=args.seed)
        raw = DatasetDict(train=split["train"], validation=split["test"])

    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    eos_id = tokenizer.eos_token_id
    if eos_id is None:
        raise ValueError("The tokenizer must define an EOS token")

    def tokenize(row: dict[str, Any]) -> dict[str, list[int]]:
        """Tokenize a row and mask prompt tokens from the supervised loss."""
        prompt = row.get("prompt")
        completion = row.get("completion", row.get("action"))
        if prompt is None or completion is None:
            raise ValueError("Every row needs prompt and completion (or action) fields")
        prompt_ids = tokenizer(str(prompt), add_special_tokens=False)["input_ids"]
        answer_ids = tokenizer(str(completion), add_special_tokens=False)["input_ids"] + [eos_id]
        input_ids = (prompt_ids + answer_ids)[: args.max_length]
        labels = ([-100] * len(prompt_ids) + answer_ids)[: args.max_length]
        return {"input_ids": input_ids, "attention_mask": [1] * len(input_ids), "labels": labels}

    tokenized = raw.map(tokenize, remove_columns=raw["train"].column_names)
    tokenized = tokenized.filter(lambda row: any(label != -100 for label in row["labels"]))

    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else None
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=dtype)
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
    model.config.use_cache = False

    targets = [part.strip() for part in args.target_modules.split(",")] if args.target_modules else None
    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=targets,
        bias="none",
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    training_kwargs = dict(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation,
        logging_steps=10,
        eval_steps=100,
        save_steps=100,
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        remove_unused_columns=False,
        bf16=bool(dtype == torch.bfloat16),
        fp16=bool(torch.cuda.is_available() and dtype is None),
        seed=args.seed,
    )
    evaluation_name = (
        "eval_strategy" if "eval_strategy" in inspect.signature(TrainingArguments).parameters
        else "evaluation_strategy"
    )
    training_kwargs[evaluation_name] = "steps"
    training = TrainingArguments(**training_kwargs)
    trainer = Trainer(
        model=model,
        args=training,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        data_collator=CompletionCollator(tokenizer),
    )
    trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))


if __name__ == "__main__":
    main()

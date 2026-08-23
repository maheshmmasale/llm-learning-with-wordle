"""Reusable LoRA supervised fine-tuning helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

from .dataset import CompletionOnlyCollator, WordleSFTDataset


def build_lora_model(model_name: str, *, rank: int = 16, alpha: int = 32, dropout: float = 0.05):
    """Load a causal LM and attach broadly compatible attention LoRA adapters."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
    config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=rank,
        lora_alpha=alpha,
        lora_dropout=dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        bias="none",
    )
    return get_peft_model(model, config), tokenizer


def train_sft(
    model: Any,
    tokenizer: Any,
    train_path: str,
    eval_path: str,
    output_dir: str,
    **training_overrides: Any,
) -> Trainer:
    """Train and save adapters, returning the completed Trainer."""
    train = WordleSFTDataset(train_path, tokenizer)
    valid = WordleSFTDataset(eval_path, tokenizer)
    defaults = dict(
        output_dir=output_dir,
        learning_rate=2e-4,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        warmup_ratio=0.03,
        weight_decay=0.01,
        logging_steps=20,
        eval_strategy="steps",
        eval_steps=250,
        save_steps=250,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        fp16=False,
        bf16=True,
    )
    defaults.update(training_overrides)
    args = TrainingArguments(**defaults)
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train,
        eval_dataset=valid,
        data_collator=CompletionOnlyCollator(tokenizer),
    )
    trainer.train()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    return trainer

# 06 — LoRA fine-tuning

`train.py` performs completion-only supervised fine-tuning with Hugging Face `Trainer` and PEFT LoRA. Prompt tokens and padding are masked from loss, evaluation data is created reproducibly when no validation file is supplied, and only adapter weights are saved.

## Install

```bash
pip install torch transformers datasets peft accelerate
```

## Train

```bash
python solutions/06_finetuning/train.py \
  --model Qwen/Qwen2.5-0.5B \
  --train-file data/wordle_train.jsonl \
  --output-dir checkpoints/wordle-lora \
  --epochs 3 --batch-size 4 --gradient-accumulation 8 \
  --gradient-checkpointing
```

Rows must contain `prompt` and `completion`; the `action` field from solution 05 is also accepted as a completion fallback. For architectures PEFT cannot infer, pass projection names explicitly, for example:

```bash
--target-modules q_proj,k_proj,v_proj,o_proj
```

The output directory is a PEFT adapter plus tokenizer, not a merged full model. Load it with `PeftModel.from_pretrained(base_model, adapter_dir)`. Use a held-out `--validation-file` for final experiments; the automatic split is intended for quick iteration.

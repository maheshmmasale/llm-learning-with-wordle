# LoRA: Low-Rank Adaptation (Hu et al., 2021)

## Gist

Finetuning updates every weight — expensive and storage-heavy per task.
LoRA freezes the model and learns the update as a product of two **tiny
rank-r matrices** added to attention layers. A 175B model's task adapter
shrinks from gigabytes to megabytes with no inference slowdown. This is how
small teams finetune at all.

## How it works

Replace the update ΔW with a low-rank factorization **BA**, where B is d×r
and A is r×d with r like 8 or 16. Initialize A from a small Gaussian and B
to zero, so training starts exactly at the pretrained model and only the
adapter moves. Scale the update by α/r. Train with the base weights frozen —
optimizer states exist only for the tiny matrices, so VRAM collapses. At
inference, fold BA back into W: zero latency cost, and swapping tasks means
swapping megabyte adapters on one shared base.

## Key concepts

- **Low-rank update**: ΔW = BA with r ≪ d. If task adaptation lives in a
  small subspace, full-matrix updates are waste.
- **Rank r**: the single knob — capacity of the adapter. Typical values 8–64.
- **Frozen base + merged adapters**: at inference the adapter folds back
  into W, so zero latency cost. Swap adapters per task for free.
- **Target modules**: usually query/value projections; the paper shows
  which layer subsets matter.
- **Alpha scaling**: lora_alpha/r controls update magnitude — the second
  knob in any LoRA config.

## Why learn this

LoRA is the purest example of a recurring engineering pattern: freeze the
big thing, train a small delta. Adapters, prefix tuning, and even
quantization-aware tricks rhyme with it. Internalize "rank as capacity knob"
and you can reason about any parameter-efficient method in minutes.

## Links

- Paper: https://arxiv.org/abs/2106.09685
- Video: [What is LoRA — explained by the inventor, Edward Hu](https://www.youtube.com/watch?v=DhRoTONcyZE)

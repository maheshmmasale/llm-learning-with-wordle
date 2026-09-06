# LoRA: Low-Rank Adaptation (Hu et al., 2021)

## Gist

Finetuning updates every weight — expensive and storage-heavy per task.
LoRA freezes the model and learns the update as a product of two **tiny
rank-r matrices** added to attention layers. A 175B model's task adapter
shrinks from gigabytes to megabytes with no inference slowdown. This is how
you will finetune on a laptop.

## Key concepts

- **Low-rank update**: ΔW = BA with r ≪ d. If task adaptation lives in a
  small subspace, full-matrix updates are waste.
- **Rank r**: the single knob — capacity of the adapter. Your milestone 6
  sweeps it; typical values 8–64.
- **Frozen base + merged adapters**: at inference the adapter folds back
  into W, so zero latency cost. Swap adapters per task for free.
- **Target modules**: usually query/value projections; the paper shows
  which layer subsets matter (your `target_modules` config).
- **Alpha scaling**: lora_alpha/r controls update magnitude — the second
  knob in `src/training/sft.py`.

## Why it matters here

Milestone 6 is LoRA, full stop. `build_lora_model` in `src/training/sft.py`
is this paper in ~15 lines: rank, alpha, dropout, target modules. Read the
file with the paper's Figure 1 in mind.

## Links

- Paper: https://arxiv.org/abs/2106.09685
- Video: [What is LoRA — explained by the inventor, Edward Hu](https://www.youtube.com/watch?v=DhRoTONcyZE)

# QLoRA (Dettmers et al., 2023)

## Gist

LoRA still needs the full model in memory. QLoRA quantizes the frozen base
to **4-bit NormalFloat** and backpropagates through it into LoRA adapters,
finetuning a 65B model on one 48GB GPU with no quality loss. Three tricks:
NF4 (optimal for normally-distributed weights), double quantization
(compress the quantization constants), paged optimizers (no memory spikes).

## Key concepts

- **4-bit NormalFloat (NF4)**: a datatype shaped to the actual distribution
  of neural weights — more precision where weights actually live.
- **Double quantization**: even the per-block scale factors get quantized,
  saving ~0.4 bits/parameter. Small, free, always on.
- **Paged optimizers**: overflow-safe memory handling so long sequences
  don't OOM mid-training.
- **Frozen 4-bit base + trainable LoRA**: gradients flow through quantized
  weights without updating them — the memory trick in one sentence.
- **Guanaco result**: QLoRA-tuned models reached ~99% of ChatGPT on Vicuna
  benchmarks, proving quantization doesn't cost capability.

## Why it matters here

If LoRA doesn't fit your hardware, QLoRA is plan B for milestone 6 — and
its NF4/quantization ideas are why your small models can run inference
locally at all. The bitsandbytes line in `requirements-ml.txt` is this paper.

## Links

- Paper: https://arxiv.org/abs/2305.14314
- Video: [What Breaks Below 4-Bit? NF4 and QLoRA Explained](https://www.youtube.com/watch?v=BIjo8GKOiqA)

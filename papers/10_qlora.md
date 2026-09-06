# QLoRA (Dettmers et al., 2023)

## Gist

LoRA still needs the full model in memory. QLoRA quantizes the frozen base
to **4-bit NormalFloat** and backpropagates through it into LoRA adapters,
finetuning a 65B model on one 48GB GPU with no quality loss. Three tricks:
NF4 (optimal for normally-distributed weights), double quantization
(compress the quantization constants), paged optimizers (no memory spikes).

## How it works

Weights are approximately normal, so quantization bins are placed at the
**quantiles of N(0,1)** — equal probability mass per bin, which is
information-theoretically optimal and beats naive uniform bins. Quantization
happens in small blocks, each with its own scale constant; **double
quantization** then quantizes those constants too, clawing back ~0.4
bits/parameter. The 4-bit base stays frozen while gradients flow through it
(dequantized on the fly in BF16) into the LoRA adapters. **Paged optimizers**
spill momentary memory spikes to CPU RAM instead of OOM-crashing. Net
effect: ~0.5 bits/parameter overhead for the base model.

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

## Why learn this

QLoRA teaches **memory math**: budgeting bits per parameter is the skill
behind running anything big on small hardware. The pattern — match the
datatype to the data distribution, compress the metadata too, page the
spikes — transfers to every resource-constrained system you'll ever build.

## Links

- Paper: https://arxiv.org/abs/2305.14314
- Video: [What Breaks Below 4-Bit? NF4 and QLoRA Explained](https://www.youtube.com/watch?v=BIjo8GKOiqA)

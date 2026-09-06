# LLaMA: Open and Efficient Foundation Language Models (Touvron et al., 2023)

## Gist

Meta trained 7B–65B models **only on public data** and showed a 13B model
beating 175B GPT-3 on most benchmarks. The message: open weights plus
Chinchilla-style long training democratize capable models. LLaMA's release
(and leak) ignited the open-model ecosystem — SmolLM, Qwen, and TinyLlama
are its philosophical children.

## Key concepts

- **Open weights**: releasing parameters, not just API access. Everything
  local in this course depends on this decision existing.
- **Public-data-only training**: competitive models need no secret crawl —
  reproducibility becomes possible for outsiders.
- **Architectural tweaks that stuck**: RMSNorm, SwiGLU activations, rotary
  embeddings (RoPE). Your models use all three; RoPE is why position
  handling differs from the original Transformer.
- **Efficient inference**: smaller models at more tokens each — the recipe
  your laptop-grade agents copy.
- **The leak effect**: LLaMA's torrent leak proved demand for runnable
  models and forced the open ecosystem (Alpaca, Vicuna, finetune tooling).

## Why it matters here

Your base models exist because LLaMA proved small-and-open works. When you
load SmolLM-360M or Qwen2-0.5B, you are standing on this paper's training
recipe and its licensing fight.

## Links

- Paper: https://arxiv.org/abs/2302.13971
- Video: [LLaMA: Open and Efficient Foundation Language Models — Yannic Kilcher](https://www.youtube.com/watch?v=E5OnoYF2oAk)

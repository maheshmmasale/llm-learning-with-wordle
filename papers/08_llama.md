# LLaMA: Open and Efficient Foundation Language Models (Touvron et al., 2023)

## Gist

Meta trained 7B–65B models **only on public data** and showed a 13B model
beating 175B GPT-3 on most benchmarks. The message: open weights plus
Chinchilla-style long training democratize capable models. LLaMA's release
(and leak) ignited the open-model ecosystem — SmolLM, Qwen, and TinyLlama
are its philosophical children.

## How it works

Decoder-only Transformer with three tweaks that all stuck: **RMSNorm**
(pre-normalization using root-mean-square instead of mean-variance —
cheaper, equally stable), **SwiGLU** activations (gated linear units that
outperform ReLU/GELU in the feed-forward blocks), and **rotary position
embeddings (RoPE)**, which encode relative position by rotating query/key
vectors instead of adding absolute signals. Trained ~1–1.4T tokens of public
sources with a standard BPE tokenizer plus byte fallback. The 13B checkpoint
beat GPT-3 nearly everywhere while fitting on one server node.

## Key concepts

- **Open weights**: releasing parameters, not just API access. Local,
  inspectable, finetunable models depend on this decision existing.
- **Public-data-only training**: competitive models need no secret crawl —
  reproducibility becomes possible for outsiders.
- **Architectural tweaks that stuck**: RMSNorm, SwiGLU, RoPE. You will meet
  all three in every modern model card; this is where they were popularized.
- **Efficient inference**: smaller models at more tokens each — the recipe
  laptop-grade agents copy.
- **The leak effect**: LLaMA's torrent leak proved demand for runnable
  models and forced the open ecosystem (Alpaca, Vicuna, finetune tooling).

## Why learn this

Every model card you will ever read is written in LLaMA's vocabulary —
RMSNorm, SwiGLU, RoPE, tokens-per-parameter. Learning this paper is learning
to read the spec sheet: you can look at any new release and know within
minutes what actually changed versus what is marketing.

## Links

- Paper: https://arxiv.org/abs/2302.13971
- Video: [LLaMA: Open and Efficient Foundation Language Models — Yannic Kilcher](https://www.youtube.com/watch?v=E5OnoYF2oAk)

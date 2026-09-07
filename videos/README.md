# Curated Video Lectures

A deliberately short list of high-signal lectures and code-alongs. The list is ordered roughly from fundamentals to systems and research extensions. Watching is not completion: pause, predict the next step, reproduce code, and record one experiment idea.

> Links were checked when this repository was prepared in August 2026. Recommended videos are free to view; no channel endorsement is implied.

## Core path: watch these first

1. **[The spelled-out intro to neural networks and backpropagation — Andrej Karpathy](https://www.youtube.com/watch?v=VMj-3S1tku0)** — Builds a tiny autograd engine from scalar operations, making gradients and backpropagation concrete.
2. **[The spelled-out intro to language modeling: building makemore — Andrej Karpathy](https://www.youtube.com/watch?v=PaCmpygFfXo)** — Moves from counts to a trainable character-level language model and introduces sampling and loss.
3. **[Let's build GPT: from scratch, in code, spelled out — Andrej Karpathy](https://www.youtube.com/watch?v=kCc8FmEb1nY)** — Implements a decoder-only Transformer and explains masking, attention heads, residual paths, and generation. **Required.**
4. **[The Narrated Transformer Language Model — Jay Alammar](https://www.youtube.com/watch?v=-QH8fRhqFHM)** — A visual, compact explanation of tokenization, embeddings, self-attention, and next-token prediction.
5. **[Stanford CS25: Introduction to Transformers — Andrej Karpathy](https://www.youtube.com/watch?v=XfpMkf4rD6E)** — Places Transformers in historical context and explains why the architecture scales across domains.
6. **[Solving Wordle using information theory — 3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA)** — Derives entropy-based guess selection and connects uncertainty reduction to a practical solver. **Required before the search milestone.**

## Building and training language models

7. **[[1hr Talk] Intro to Large Language Models — Andrej Karpathy](https://www.youtube.com/watch?v=zjkBMFhNj_g)** — High-level map of pretraining, fine-tuning, RLHF, scaling, tools, and limitations; useful before committing to architecture choices.
8. **[Deep Dive into LLMs like ChatGPT — Andrej Karpathy](https://www.youtube.com/watch?v=7xTGNNLPyMI)** — Detailed walkthrough of data, tokenization, pretraining, post-training, inference, and evaluation in modern LLMs.
9. **[Let's build the GPT Tokenizer — Andrej Karpathy](https://www.youtube.com/watch?v=zduSFxRajkE)** — Implements byte-pair encoding and exposes tokenization edge cases that matter for five-letter actions.
10. **[Let's reproduce GPT-2 (124M) — Andrej Karpathy](https://www.youtube.com/watch?v=l8pRSuU81PU)** — Reproduces a real training recipe while covering initialization, optimization, distributed training, and throughput measurement.
11. **[State of GPT — Andrej Karpathy](https://www.youtube.com/watch?v=bZQun8Y4L2A)** — Explains the pretraining/SFT/reward-model/RLHF pipeline and provides vocabulary for discussing model development.
12. **[Stanford CS229: Building Large Language Models — Yann Dubois](https://www.youtube.com/watch?v=9vM4p9NN0Ts)** — Connects data, autoregressive objectives, scaling, evaluation, post-training, and systems in one university lecture.

## Reasoning, inference-time compute, and systems

13. **[Stanford CME295: Transformers & Large Language Models](https://www.youtube.com/watch?v=Q5baLehv5So)** — Covers decoding, temperature, beam search, chain of thought, self-consistency, KV caching, and PagedAttention in one coherent lecture.
14. **[Stanford CME295: LLM Training](https://www.youtube.com/watch?v=VlA_jt_3Qc4)** — Surveys pretraining compute, Chinchilla scaling, ZeRO, FlashAttention, mixed precision, SFT, LoRA, and QLoRA.
15. **[Stanford CME295: LLM Reasoning](https://www.youtube.com/watch?v=k5Fh-UgTuCo)** — Reviews reasoning-model evaluation, pass@k, test-time scaling, GRPO/PPO, and length bias; best treated as an advanced inference-scaling resource.
16. **[Stanford CS25: Emergent Abilities and Scaling in LLMs — Jason Wei](https://www.youtube.com/watch?v=tVtOevLrt5U)** — Presents scaling behavior and prompts questions about whether observed capability jumps depend on metrics or model size.

## Optional reinforcement learning and broader perspective

17. **[David Silver RL Course: Policy Gradient Methods](https://www.youtube.com/watch?v=KHZVXao4qXs)** — Derives REINFORCE and actor–critic ideas needed before PPO; watch only if attempting the RL stretch goal.
18. **[How Could Machines Reach Human-Level Intelligence? — Yann LeCun](https://www.youtube.com/watch?v=xL6Y0dpXEwc)** — A critical perspective on autoregressive LLM limitations, world models, reasoning, and planning; useful for challenging assumptions in the final discussion.

## Active-watching prompts

For each video, write no more than five bullets:

- What is the central claim or technique?
- What assumption does it make?
- Which part can be tested cheaply in Wordle?
- What metric would reveal whether it helped?
- What could confound that conclusion?

## Suggested viewing order

| Milestone | Videos |
|---|---|
| M1 environment | 6 |
| M2 baselines | 1–5, 7 |
| M3 prompting | 11, 16 |
| M4 solver | 13 |
| M5 dataset | 2, 9 |
| M6 finetuning | 8, 10, 12, 14 |
| M7 scaling | 15, 17 |
| M8 final | 18 and revisit the videos directly cited in the final report |

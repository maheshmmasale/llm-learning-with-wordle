# Papers and Core Resources

## The 20 papers: read the brief first

Each file below fits on one screen: what the paper shows, how it works,
the concepts it needs, why it is worth learning, plus paper and video
links. In a hurry, the brief alone suffices; curious, follow the links.

Foundations: [01 Attention](01_attention-is-all-you-need.md) ·
[02 BERT](02_bert.md) · [03 GPT-2](03_gpt2.md) · [04 GPT-3](04_gpt3.md) ·
[05 SentencePiece](05_sentencepiece.md)

Scale: [06 Scaling Laws](06_scaling-laws.md) ·
[07 Chinchilla](07_chinchilla.md) · [08 LLaMA](08_llama.md)

Training: [09 LoRA](09_lora.md) · [10 QLoRA](10_qlora.md) ·
[11 InstructGPT](11_instructgpt.md) · [12 PPO](12_ppo.md) ·
[13 DPO](13_dpo.md) · [14 GRPO/DeepSeekMath](14_grpo-deepseekmath.md)

Data: [15 Self-Instruct](15_self-instruct.md) ·
[16 Data Cards](16_data-cards.md)

Reasoning at inference: [17 Chain-of-Thought](17_chain-of-thought.md) ·
[18 Self-Consistency](18_self-consistency.md) ·
[19 Tree of Thoughts](19_tree-of-thoughts.md) ·
[20 Verify Step by Step](20_verify-step-by-step.md)

---

A curated path from transformer fundamentals to the research questions in this project. Each item includes **why it matters** for a small-model Wordle system. Do not try to read everything at once: use the **Start here** items first, then read the papers relevant to the experiment you are running.

> Links were checked when this repository was prepared in August 2026. Papers may later receive revised versions; record the version you used in your experiment notes.

## 1. Transformer fundamentals

1. **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — Introduces the Transformer; understand scaled dot-product attention, causal masking, residual blocks, and positional encodings. **Start here.**
2. **[The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)** — Builds visual intuition for queries, keys, values, multi-head attention, and autoregressive decoding before you face the equations. **Start here.**
3. **[The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)** — A line-by-line PyTorch implementation that connects the original paper's equations to working code.
4. **[Language Models are Unsupervised Multitask Learners (GPT-2)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)** — Shows the decoder-only, next-token-prediction recipe underlying the model family used in this project.
5. **[Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)** — Establishes in-context learning and gives useful background for separating prompting gains from training gains.
6. **[SentencePiece](https://arxiv.org/abs/1808.06226)** — Explains subword tokenization; useful when diagnosing why a model may represent five-letter words awkwardly.

## 2. Language-model training and fine-tuning

7. **[nanoGPT](https://github.com/karpathy/nanoGPT)** — A compact, readable GPT training implementation and a practical reference for data loading, optimization, checkpointing, and sampling. **Start here.**
8. **[Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)** — Karpathy implements a small GPT while explaining every major component and tensor shape. **Start here.**
9. **[Hugging Face: Fine-tuning](https://huggingface.co/docs/transformers/training)** — Official path for loading a pretrained causal LM and adapting it with `Trainer`.
10. **[Hugging Face: Causal language modeling](https://huggingface.co/docs/transformers/tasks/language_modeling)** — End-to-end example of tokenization, collation, training, and perplexity evaluation for a causal LM.
11. **[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)** — Introduces parameter-efficient adapters that reduce trainable parameters and optimizer memory.
12. **[QLoRA](https://arxiv.org/abs/2305.14314)** — Shows how quantization plus LoRA can make fine-tuning much larger models feasible on limited hardware.
13. **[Hugging Face PEFT documentation](https://huggingface.co/docs/peft/index)** — Practical, maintained documentation for applying LoRA and related parameter-efficient methods.

## 3. Scaling laws and compute allocation

14. **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** — Kaplan et al. quantify power-law relationships among parameters, data, compute, and loss; essential context for a fixed-budget project.
15. **[Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)** — Revises the preferred balance of model size and training tokens and motivates careful compute allocation. **Start here.**
16. **[Scaling Data-Constrained Language Models](https://arxiv.org/abs/2305.16264)** — Studies repeated data and constrained corpora, directly relevant when synthetic Wordle states are finite or reused.
17. **[Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)** — Warns how optimizing a proxy reward can eventually reduce true quality, a key concern for verifier or RL experiments.
18. **[Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)** — Provides a framework for allocating inference compute and motivates compute/performance frontiers instead of a single score.

## 4. Reasoning, verification, and search

19. **[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)** — Establishes intermediate reasoning prompts as a baseline, while leaving open whether traces are faithful.
20. **[Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171)** — Samples multiple reasoning paths and aggregates answers; a natural inference-time-scaling baseline.
21. **[Tree of Thoughts](https://arxiv.org/abs/2305.10601)** — Treats reasoning as explicit search over candidate thoughts, providing a template for branching and lookahead.
22. **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** — Interleaves reasoning with tool actions, useful for designing an LLM that calls a deterministic constraint solver.
23. **[PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435)** — Separates natural-language decomposition from exact program execution, closely matching the model-versus-solver question.
24. **[STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)** — Iteratively generates and filters rationales for training, a possible route to better synthetic Wordle traces.
25. **[Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)** — Demonstrates sampling candidate solutions and using a learned verifier, analogous to generating and reranking guesses.

## 5. Reinforcement learning and preference optimization

26. **[Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)** — The core clipped policy-gradient algorithm behind many RLHF systems; read before attempting the stretch goal.
27. **[Training Language Models to Follow Instructions with Human Feedback (InstructGPT)](https://arxiv.org/abs/2203.02155)** — Explains the SFT → reward model → PPO pipeline and the engineering decisions behind RLHF.
28. **[Direct Preference Optimization](https://arxiv.org/abs/2305.18290)** — Recasts preference learning as a simple classification-style objective without online reward-model RL.
29. **[DeepSeekMath](https://arxiv.org/abs/2402.03300)** — Introduces Group Relative Policy Optimization (GRPO) in a verifiable reasoning domain and is useful context for outcome-based Wordle rewards.
30. **[A Survey of Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2307.04964)** — Organizes reward modeling, policy optimization, evaluation, and open problems into one reference.

## 6. Training and inference systems

31. **[PyTorch Profiler documentation](https://docs.pytorch.org/docs/stable/profiler.html)** — Official reference for measuring CPU/GPU time, memory, kernels, and trace events instead of guessing where time goes.
32. **[Getting Started with Distributed Data Parallel](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html)** — Shows PyTorch's standard multi-GPU training pattern and the synchronization assumptions behind it.
33. **[Introducing PyTorch Fully Sharded Data Parallel](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/)** — Explains how sharding parameters, gradients, and optimizer state changes memory scaling.
34. **[FlashAttention](https://arxiv.org/abs/2205.14135)** — Uses IO-aware exact attention to reduce memory traffic and improve training/inference efficiency.
35. **[Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM)](https://arxiv.org/abs/2309.06180)** — Explains KV-cache paging and continuous batching for high-throughput serving.

## 7. Wordle, entropy, and optimal play

36. **[Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)** — 3Blue1Brown turns feedback patterns into entropy and expected information gain; the clearest conceptual entry point. **Start here.**
37. **[3Blue1Brown's Wordle simulation code](https://github.com/3b1b/videos/tree/master/_2022/wordle)** — Source code behind the video, useful for auditing pattern matrices, priors, and entropy calculations rather than copying them blindly.
38. **[Wordle is NP-hard](https://arxiv.org/abs/2203.05024)** — Formalizes generalized Wordle's computational difficulty and clarifies why exact planning can become expensive.
39. **[deedy/wordle-solver](https://github.com/deedy/wordle-solver)** — A compact search/entropy implementation with benchmark discussion; useful as an independent reference baseline.
40. **[Wordle Guessers](https://github.com/ngoldfine/wordle-guessers)** — Compares random, similarity, vocabulary-minimizing, and entropy strategies under a shared interface.

## Suggested reading order by project week

| Week | Read first | Then consult |
|---:|---|---|
| 1 | Items 36, 40 | Items 3, 38 |
| 2 | Items 1, 2, 8 | Items 4–6 |
| 3 | Items 5, 19 | Items 20, 22 |
| 4 | Items 21–23, 38 | Items 25, 39 |
| 5 | Items 16, 24 | Items 17, 40 |
| 6 | Items 9–13 | Items 31–35 |
| 7 | Items 18, 20, 25 | Items 26–30, 35 |
| 8 | Items 14–18 | Revisit the papers needed to justify conclusions |

## Reading-note template

For every paper you rely on in the final report, capture:

- **Claim:** What is the central claim?
- **Mechanism:** What method produces the result?
- **Evidence:** What baselines, datasets, metrics, and compute support it?
- **Assumptions:** Which assumptions may not hold for Wordle or a 0.2B–0.5B model?
- **Transfer:** What is one testable idea you can adapt?
- **Falsifier:** What result would convince you the adapted idea did not help?

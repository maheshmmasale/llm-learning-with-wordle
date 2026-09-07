# Hands-on Tutorials

These resources prioritize **doing** over passive reading. Follow the suggested path, complete the checkpoint, and save your notes or code in your own working branch. Treat third-party implementations as references after you have attempted the assignment—not as drop-in solutions.

> Links were checked when this repository was prepared in August 2026. Library interfaces change; note package versions in every experiment.

## Suggested path

1. PyTorch foundations
2. Transformers from first principles
3. Hugging Face inference and fine-tuning
4. Profiling and reproducible experiments
5. Wordle solvers and information gain
6. Optional distributed training and RL

## 1. PyTorch foundations

- **[PyTorch: Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)** — A short sequence covering tensors, datasets, models, autograd, optimization, and saving/loading. *Checkpoint: train and reload a tiny classifier.*
- **[PyTorch: The Fundamentals of Autograd](https://docs.pytorch.org/tutorials/beginner/introyt/autogradyt_tutorial.html)** — Builds a concrete mental model of computation graphs and gradients. *Checkpoint: inspect gradients before and after `backward()`.*
- **[PyTorch reproducibility notes](https://docs.pytorch.org/docs/stable/notes/randomness.html)** — Documents seeds, deterministic algorithms, and platform caveats. *Checkpoint: reproduce one run twice and record any remaining nondeterminism.*
- **[Weights & Biases: Track experiments with PyTorch](https://docs.wandb.ai/tutorials/pytorch/)** — Demonstrates logging metrics, hyperparameters, and artifacts. *Checkpoint: compare two runs from a single dashboard or exported table.*

## 2. Transformers from first principles

- **[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)** — Karpathy's build-from-scratch sequence from autograd through language models, GPT, and tokenization. *Checkpoint: complete the GPT lecture exercises before using a high-level trainer.*
- **[The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)** — Executable explanation of each Transformer component. *Checkpoint: trace tensor shapes through one attention head and the causal mask.*
- **[nanoGPT](https://github.com/karpathy/nanoGPT)** — Minimal GPT training code designed to be read and modified. *Checkpoint: overfit a tiny corpus and explain every field in the training log.*
- **[minGPT](https://github.com/karpathy/minGPT)** — Small, education-oriented GPT implementation with a deliberately simple API. *Checkpoint: identify where token embeddings, positional embeddings, and causal masking enter the forward pass.*
- **[minBPE](https://github.com/karpathy/minbpe)** — Minimal byte-pair encoding tokenizer implementation and exercise set. *Checkpoint: inspect how several Wordle words split under two tokenizers.*

## 3. Hugging Face model use and supervised fine-tuning

- **[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)** — Free course on Transformers, tokenizers, datasets, fine-tuning, sharing, and advanced LLM topics. *Checkpoint: load a small causal LM and produce deterministic output with a fixed seed.*
- **[Transformers quick tour](https://huggingface.co/docs/transformers/quicktour)** — Introduces `AutoTokenizer`, `AutoModel`, pipelines, batching, and saving/loading. *Checkpoint: write one batch inference function without a pipeline.*
- **[Causal language modeling tutorial](https://huggingface.co/docs/transformers/tasks/language_modeling)** — Official end-to-end causal-LM data preparation and training example. *Checkpoint: adapt the collator and labels to the Wordle state/action format.*
- **[Datasets quickstart](https://huggingface.co/docs/datasets/quickstart)** — Covers loading, mapping, filtering, formatting, and caching datasets. *Checkpoint: construct deterministic train/validation/test splits and fingerprint them.*
- **[Trainer documentation](https://huggingface.co/docs/transformers/main_classes/trainer)** — Complete API reference for training arguments, evaluation, callbacks, checkpointing, and resumption. *Checkpoint: resume from a checkpoint and match the uninterrupted run closely.*
- **[PEFT quicktour](https://huggingface.co/docs/peft/quicktour)** — Practical LoRA setup for parameter-efficient fine-tuning. *Checkpoint: report trainable parameters, peak memory, and validation performance against full fine-tuning or a frozen baseline.*
- **[TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer)** — Supervised fine-tuning utilities for conversational or prompt-completion data. *Checkpoint: verify that loss is applied only to the intended completion tokens.*
- **[Accelerate quicktour](https://huggingface.co/docs/accelerate/quicktour)** — A minimal path from a standard PyTorch loop to device-agnostic and multi-device execution. *Checkpoint: run the same script on CPU and one GPU without code changes.*

## 4. Profiling, memory, and inference

- **[PyTorch Profiler recipe](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)** — Shows how to capture operator time and memory rather than relying on wall-clock intuition. *Checkpoint: identify the top three CUDA or CPU operators in one model call.*
- **[PyTorch `torch.compile` tutorial](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)** — Explains graph capture, compilation, speed measurement, and common graph breaks. *Checkpoint: benchmark eager versus compiled inference after warm-up.*
- **[vLLM quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)** — Covers high-throughput batched generation and OpenAI-compatible serving. *Checkpoint: measure throughput and latency as batch size changes.*
- **[PyTorch DistributedDataParallel tutorial](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html)** — Introduces the standard process-per-GPU training pattern. *Checkpoint: explain when communication overhead makes two GPUs slower than one.*

## 5. Wordle and information-gain implementations

Read these **after** attempting the environment and deterministic solver assignments.

- **[3Blue1Brown Wordle simulation source](https://github.com/3b1b/videos/tree/master/_2022/wordle)** — Code behind the information-theory video; inspect its pattern encoding, priors, and entropy computation. *Checkpoint: write down where its rules or vocabulary differ from your benchmark.*
- **[deedy/wordle-solver](https://github.com/deedy/wordle-solver)** — A concise entropy/search solver with empirical results. *Checkpoint: reproduce one benchmark using your own target list and feedback function.*
- **[Wordle Guessers](https://github.com/ngoldfine/wordle-guessers)** — Shared framework comparing random and heuristic policies. *Checkpoint: port one policy behind your own `Agent` interface without copying environment logic.*
- **[Information-Theoretic Wordle Solver](https://github.com/alitarek75/wordle-solver)** — Clear example of a precomputed guess–target feedback matrix. *Checkpoint: estimate matrix size and benchmark precomputation versus on-demand scoring.*

## 6. Evaluation and experiment design

- **[Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)** — Practical guidance on baselines, instrumentation, data pipelines, and avoiding premature complexity. *Checkpoint: identify the simplest measurable baseline for each milestone.*
- **[Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook)** — A disciplined guide to debugging, scientific hyperparameter tuning, and reporting. *Checkpoint: document the search space and stopping rule before a tuning run.*
- **[scikit-learn: Statistical comparison of models](https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_stats.html)** — Illustrates uncertainty-aware comparison rather than ranking noisy point estimates. *Checkpoint: attach a confidence interval to win rate.*

## 7. Optional reinforcement learning

- **[OpenAI Spinning Up: Introduction to RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)** — Concise definitions of states, actions, policies, returns, value functions, and policy gradients. *Checkpoint: formulate Wordle as an episodic decision process and state what is partially observed.*
- **[OpenAI Spinning Up: PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)** — Explains PPO objectives, clipping, KL early stopping, and pseudocode. *Checkpoint: list diagnostics needed to catch policy collapse or reward hacking.*
- **[Hugging Face TRL documentation](https://huggingface.co/docs/trl/index)** — Practical trainers for SFT, DPO, GRPO, reward modeling, and related post-training methods. *Checkpoint: run RL only after establishing a reproducible SFT baseline and reward-unit tests.*

## How to use an external tutorial responsibly

For every borrowed idea or code fragment:

1. Link the source in your experiment notes and preserve its license notice.
2. State what you changed and why.
3. Test duplicate-letter feedback independently; many Wordle demos get it wrong.
4. Re-evaluate on this repository's frozen target split and rules.
5. Never import a reference implementation into the hidden test evaluator.

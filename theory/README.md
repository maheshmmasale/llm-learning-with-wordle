# Theory Guide

This folder explains the ideas behind the experiments in this repository. It is the bridge between the curated papers and videos and the hands-on problems: read a theory note, make a prediction, run the corresponding local experiment, and compare the result with your prediction.

Everything here assumes a **local-only workflow**. The model, Wordle environment, datasets, training jobs, and evaluation scripts should run on a laptop or workstation you control. No cloud GPU, paid API, or hosted inference endpoint is required. This constraint is part of the lesson: good experimental design and efficient systems often matter more than simply adding compute.

## Recommended Learning Loop

1. Read the relevant theory note before opening a problem.
2. Write down a hypothesis in your experiment log.
3. Implement the smallest experiment that can test that hypothesis.
4. Record accuracy, runtime, memory use, and failure cases.
5. Use an ablation to identify which change actually caused the result.
6. Revisit the theory note and explain any disagreement between prediction and evidence.

## Theory Notes

- [01 — Ablations](01_ablations.md): Design controlled experiments that isolate which parts of the Wordle system produce real gains.
- [02 — Local LLMs](02_local_llms.md): Understand model memory, quantization, CPU/GPU inference, and reproducible local measurement.
- [03 — Prompting and Representation](03_prompting_and_representation.md): Represent Wordle state efficiently and design prompts that small models can follow reliably.
- [04 — Search and Solver](04_search_and_solver.md): Build deterministic filtering, information-gain search, hybrid LLM–solver systems, and inference-time search.
- [05 — Training and SFT](05_training_and_sft.md): Learn supervised fine-tuning, synthetic data generation, parameter-efficient adaptation, and local training practices.
- [06 — Evaluation and Statistics](06_evaluation_and_statistics.md): Measure win rate, uncertainty, paired improvements, failure modes, and compute-performance tradeoffs.

## How the Notes Connect

The concepts are intentionally connected rather than independent. A structured prompt changes the model's input representation. A deterministic solver changes the available actions. SFT changes the policy learned from examples. Evaluation tells you whether those changes generalize, while ablations tell you which change deserves credit. Local resource measurement prevents an apparently stronger system from hiding a large latency or memory cost.

Treat every result as a claim that needs evidence. “The hybrid solver won more games” is incomplete until you state the held-out targets, number of games, random seeds, confidence interval, invalid-word rate, and compute cost. Likewise, “SFT helped” is not established until you compare against the same base model and inference procedure without SFT.

These notes are not substitutes for the papers in [`papers/`](../papers/), the [tutorials](tutorials.md) and [videos](videos.md) lists beside them, or implementation work. They provide a compact conceptual map so that the repository feels like a research apprenticeship rather than a sequence of disconnected coding tasks.

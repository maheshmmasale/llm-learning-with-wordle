# LLM Learning with Wordle

> **Learn LLM fundamentals by teaching a small model to play Wordle**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Model](https://img.shields.io/badge/model-0.2--0.5B-yellow)](https://huggingface.co/)
[![Project](https://img.shields.io/badge/project-8%20weeks-6f42c1)](#eight-week-roadmap)

This is `llm-learning-with-wordle` - a research-apprenticeship style teaching repository for engineering students who want to work at frontier AI labs.

You start with a public 0.2B-0.5B model (SmolLM-360M, Qwen2-0.5B, TinyLlama) and progressively teach it to play Wordle near SOTA level, learning LLM training, prompting, search, data generation, SFT, and inference-time scaling along the way.

> Original project name was `wordle-small-llm` - this is the same curriculum, renamed to `llm-learning-with-wordle` for clarity.

See original comprehensive README in this repo's history - this file is the entry point for GitHub.

## Quick Start

```bash
git clone https://github.com/maheshmmasale/llm-learning-with-wordle
cd llm-learning-with-wordle
pip install -r requirements.txt
pytest src/
python src/evaluation/benchmark.py --model smollm-360m --games 100
```

## Theory

The [`theory/`](theory/) folder connects the reading material to the experiments. All notes assume a local-only workflow with no cloud services or paid APIs.

- [Theory Guide](theory/README.md) — reading order and the theory-to-experiment learning loop.
- [Ablations](theory/01_ablations.md) — controlled comparisons, interaction effects, pitfalls, and required project ablations.
- [Local LLMs](theory/02_local_llms.md) — memory math, quantization, CPU/GPU inference, and local resource measurement.
- [Prompting and Representation](theory/03_prompting_and_representation.md) — raw history, structured constraints, candidate lists, and output reliability.
- [Search and Solver](theory/04_search_and_solver.md) — filtering, entropy, hybrid systems, self-consistency, beam search, and MCTS.
- [Training and SFT](theory/05_training_and_sft.md) — teacher data, LoRA, local training, generalization, and memorization checks.
- [Evaluation and Statistics](theory/06_evaluation_and_statistics.md) — win rate, confidence intervals, paired bootstrap, failure analysis, and Pareto frontiers.

Full docs: see PROBLEM.md, curriculum/, problems/

## Repo Structure

Same as before - see main README content for details. All 73 files preserved.

## Why Wordle?

Controlled, deterministic, cheap-to-evaluate lab for reasoning, planning, constraint tracking, search, and learning from synthetic data.


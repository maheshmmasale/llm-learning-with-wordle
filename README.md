# LLM Learning with Wordle

> **Learn LLM fundamentals by teaching a small model to play Wordle**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Model](https://img.shields.io/badge/model-0.2--0.5B-yellow)](https://huggingface.co/)
[![Project](https://img.shields.io/badge/project-8%20weeks-6f42c1)](#eight-week-roadmap)

This is `llm-learning-with-wordle` - a research-apprenticeship style teaching repository for engineering students who want to work at frontier AI labs.

You start with a public 0.2B-0.5B model (SmolLM-360M, Qwen2-0.5B, TinyLlama) and progressively teach it to play Wordle near SOTA level, learning LLM training, prompting, search, data generation, SFT, and inference-time scaling along the way.

> Original project name was `wordle-small-llm` - this is the same curriculum, renamed to `llm-learning-with-wordle` for clarity.

## Quick Start

```bash
git clone https://github.com/maheshmmasale/llm-learning-with-wordle
cd llm-learning-with-wordle
pip install -r requirements.txt
python -m pytest tests/ solutions/01_environment/
python -m src.evaluation.benchmark --policy solver --limit 50 --seed 0
```

Every command above is verified in CI-less local runs: 47 tests pass and the
solver benchmark wins every game on the shipped word lists. For model
milestones (data generation, SFT, inference scaling):

```bash
pip install -r requirements-ml.txt
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

```text
src/            Maintained library: environment, evaluation, models,
                search, training, utils (tested by tests/).
tests/          Pytest suite for src/ plus the milestone-01 tests.
data/           Shipped word lists: answers.txt (65) + guesses.txt (553).
                Curated common words; swap in licensed full-size lists
                without code changes.
solutions/      Frozen per-milestone reference snapshots. Self-contained
                (they do not import src/) so each milestone reads alone.
                src/ is canonical for new work; solutions/ show one
                working answer per milestone.
problems/       The 8 milestone assignments (start here).
hints/          Leveled hints, one file per milestone.
theory/         Concept notes behind the experiments.
papers/ videos/ tutorials/   Curated external reading/watching.
experiments/    Configs; results/ defines the per-run record layout.
reports/        Final-report checklist.
```

Follow `problems/01_build_wordle.md` … `problems/08_final_challenge.md` in
order; each names its hints, theory, and solution. See `PROBLEM.md` for the
full specification. Grading is one eval, no human involved: your finetuned
LLM plays Wordle through the harness, scored on solved-vs-unsolved plus
solve speed:

```bash
python -m src.evaluation.autograde --model <hf-id-or-path> --games 100000
```

Smoke-test the harness without a model:

```bash
python -m src.evaluation.harness --policy solver --games 200
```

Scoring formula: `grading_rubric.md`.

## Why Wordle?

Controlled, deterministic, cheap-to-evaluate lab for reasoning, planning, constraint tracking, search, and learning from synthetic data.


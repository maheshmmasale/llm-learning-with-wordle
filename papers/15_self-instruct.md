# Self-Instruct (Wang et al., 2022)

## Gist

Instruction tuning needs human-written tasks — slow and expensive. Self-
Instruct bootstraps: seed the model with 175 example tasks, have it
**generate its own** new instructions, inputs, and outputs, filter the junk,
then finetune on the synthetic set. Result: +33% on unseen tasks, near
InstructGPT-level from almost no human data. Synthetic data works if you
filter ruthlessly.

## How it works

Start with 175 seed (instruction, input, output) triples. Loop: prompt the
model with a few seeds to invent new instructions; classify each as
classification-type (needs label options) or not; generate instances
**input-first** (dream up input, then label it) or **output-first** (dream
up output, then invent a matching input). Then the unglamorous part that
decides everything: drop malformed rows, enforce task-type balance, and
Rouge-L-deduplicate against everything kept so far. The surviving 52K rows
finetune the base model — which, served as its own teacher, now follows
instructions it never saw humans write.

## Key concepts

- **Bootstrapping**: the model writes its own training data from a tiny
  seed pool — capability amplifying itself.
- **Instruction/input/output triples**: the schema every SFT row still uses
  (prompt/completion JSONL).
- **Filtering pipeline**: length heuristics, classification-vs-generation
  balance, Rouge-L similarity dedup. Generation is easy; curation is the work.
- **Distillation caveat**: the student can't exceed its teacher's knowledge
  — synthetic labels inherit the generator's blind spots.
- **52k dataset**: the released Self-Instruct set that spawned Alpaca and the
  open-instruction-tuning wave.

## Why learn this

Self-Instruct is the anatomy of every synthetic-data pipeline you'll build:
generate broadly, filter ruthlessly, train narrowly. The enduring lesson is
the ratio of effort — generation is 10% of the work, curation 90% — and the
ceiling rule: seed diversity, not volume, determines what the student can
become.

## Links

- Paper: https://arxiv.org/abs/2212.10560
- Video: [Bootstrapping AI With Self-Generated Instructions — Read A Paper A Day](https://www.youtube.com/watch?v=EjKYoVC43Rc)

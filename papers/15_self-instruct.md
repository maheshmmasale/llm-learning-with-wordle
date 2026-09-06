# Self-Instruct (Wang et al., 2022)

## Gist

Instruction tuning needs human-written tasks — slow and expensive. Self-
Instruct bootstraps: seed the model with 175 example tasks, have it
**generate its own** new instructions, inputs, and outputs, filter the junk
(Rouge-based dedup, validity checks), then finetune on the synthetic set.
Result: +33% on unseen tasks, near InstructGPT-level from almost no human
data. Synthetic data works if you filter ruthlessly.

## Key concepts

- **Bootstrapping**: the model writes its own training data from a tiny
  seed pool — capability amplifying itself.
- **Instruction/input/output triples**: the schema every SFT row still uses
  (your `prompt`/`completion` JSONL is this format).
- **Filtering pipeline**: length heuristics, classification-vs-generation
  balance, Rouge-L similarity dedup. Generation is easy; curation is the work.
- **Distillation caveat**: the student can't exceed its teacher's knowledge
  — synthetic labels inherit the generator's blind spots, including for Wordle.
- **52k dataset**: the released Self-Instruct set that spawned Alpaca and the
  open-instruction-tuning wave.

## Why it matters here

Milestone 5 *is* Self-Instruct for Wordle: your entropy solver is the
"teacher", game states are the "instructions", and your leakage audit is
their filtering pipeline. Read this before writing `generate.py` extensions.

## Links

- Paper: https://arxiv.org/abs/2212.10560
- Video: [Bootstrapping AI With Self-Generated Instructions — Read A Paper A Day](https://www.youtube.com/watch?v=EjKYoVC43Rc)

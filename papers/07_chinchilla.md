# Training Compute-Optimal LLMs / Chinchilla (Hoffmann et al., 2022)

## Gist

Kaplan said "bigger models"; Chinchilla corrected the math. Training 400+
models showed everyone was **undertraining**: for fixed compute, parameters
and training tokens should scale **equally** (~20 tokens per parameter).
A 70B model on 1.4T tokens beat 175B–280B models trained on less. Lesson:
data scale is as important as model scale.

## How it works

Fit a parametric loss L(N,D) = E + A/N^α + B/D^β over 400+ models (70M–16B
params, 5B–500B tokens). For each compute budget, trace the **isoFLOP curve**
— all (N, D) pairs costing the same — and read off its minimum: the
compute-optimal point. Minima line up at roughly equal scaling of N and D,
i.e. ~20 training tokens per parameter. Then the proof: train Chinchilla
(70B, 1.4T tokens) on exactly Gopher's (280B) compute budget and watch it
win uniformly — same FLOPs, far cheaper inference forever after.

## Key concepts

- **Compute-optimal frontier**: the loss-minimizing (parameters, tokens)
  pair per FLOP budget. Chinchilla's rule of thumb: 20 tokens/parameter.
- **Undertraining**: GPT-3-era giants stopped too early; more tokens on a
  smaller model wins — directly motivating 0.5B-class models trained long.
- **Equal scaling**: double parameters → double data, not parameters alone.
- **Inference bonus**: smaller compute-optimal models are also cheaper to
  serve, which is why capable agents can run on a laptop.
- **Empirical refit**: scaling "laws" are fitted, not derived — 400+ runs
  beat theory, a precedent for ablations-over-opinions thinking.

## Why learn this

Chinchilla teaches that established "laws" are just last year's best fit —
 overturnable by better experiments. Practically, it justifies the small-model
bet everywhere: when someone says you need 70B parameters, ask for their
tokens-per-parameter first. Data-rich small models are a strategy, not a
compromise.

## Links

- Paper: https://arxiv.org/abs/2203.15556
- Video: [Chinchilla Paper Deep Dive — TalkTensors](https://www.youtube.com/watch?v=GsVEfSeE6Jo)

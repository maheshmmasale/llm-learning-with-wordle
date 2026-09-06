# Training Compute-Optimal LLMs / Chinchilla (Hoffmann et al., 2022)

## Gist

Kaplan said "bigger models"; Chinchilla corrected the math. Training 400+
models showed everyone was **undertraining**: for fixed compute, parameters
and training tokens should scale **equally** (~20 tokens per parameter).
A 70B model on 1.4T tokens beat 175B–280B models trained on less. Lesson:
data scale is as important as model scale.

## Key concepts

- **Compute-optimal frontier**: the loss-minimizing (parameters, tokens)
  pair per FLOP budget. Chinchilla's rule of thumb: 20 tokens/parameter.
- **Undertraining**: GPT-3-era giants stopped too early; more tokens on a
  smaller model wins — directly motivating 0.5B-class models trained long.
- **Equal scaling**: double parameters → double data, not parameters alone.
- **Inference bonus**: smaller compute-optimal models are also cheaper to
  serve, which is why your Wordle agent can run on a laptop.
- **Empirical refit**: scaling "laws" are fitted, not derived — 400+ runs
  beat theory, a precedent for your own ablations-over-opinions approach.

## Why it matters here

Chinchilla is the license for this entire course: small, well-trained open
models are not toys, they are the compute-optimal regime. It also frames
your data-generation milestone — tokens are half the scaling equation.

## Links

- Paper: https://arxiv.org/abs/2203.15556
- Video: [Chinchilla Paper Deep Dive — TalkTensors](https://www.youtube.com/watch?v=GsVEfSeE6Jo)

# Scaling Laws for Neural Language Models (Kaplan et al., 2020)

## Gist

Model loss follows smooth **power laws** in three things: parameters, data,
and compute. Architecture details barely matter; scale does. The practical
output is a budgeting rule: given fixed compute, there is an optimal way to
split it between bigger models and more training tokens. This paper turned
"just scale it" from folklore into engineering.

## How it works

Train dozens of models spanning 7+ orders of magnitude of compute, varying
one factor (size, data, steps) while holding the rest fixed, and fit loss
curves: L(N) ∝ N^-α, L(D) ∝ D^-β, L(C) ∝ C^-γ. Width-vs-depth ablations show
shape barely matters within wide ranges. The fitted exponents then answer
budget questions analytically — e.g., larger models are more sample-efficient,
so under fixed compute you should train big models but stop early rather
than train small ones to convergence. Overfitting onset gets its own
equation in terms of the size/data ratio.

## Key concepts

- **Power-law scaling**: loss = a·N^-α + b·D^-β + …, so each doubling of
  resources buys a predictable gain. Plot log-loss vs log-compute: a line.
- **Sample efficiency**: bigger models reach the same loss on fewer tokens —
  relevant whenever data is the bottleneck.
- **Compute-optimal allocation**: don't just grow parameters; the paper says
  how to divide a fixed FLOP budget (later corrected by Chinchilla).
- **Overfitting regime**: too-big model on too-little data breaks the curves
  — the formalism behind memorization checks.
- **Weak architecture dependence**: width vs depth barely moves loss, which
  justifies treating most Transformers as "a Transformer, full stop".

## Why learn this

This is budgeting thinking for ML: fit curves, extrapolate, decide *before*
spending. The same habit scales down — learning curves on your own runs tell
you whether more epochs, more data, or a bigger model buys the next point.
And it teaches healthy skepticism: fitted laws describe the past; Chinchilla
showed they can still be wrong.

## Links

- Paper: https://arxiv.org/abs/2001.08361
- Video: [Neural Scaling Laws and GPT-3 — Jared Kaplan (the author himself)](https://www.youtube.com/watch?v=sNfkZFVm_xs)

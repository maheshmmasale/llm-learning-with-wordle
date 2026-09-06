# Scaling Laws for Neural Language Models (Kaplan et al., 2020)

## Gist

Model loss follows smooth **power laws** in three things: parameters, data,
and compute. Architecture details barely matter; scale does. The practical
output is a budgeting rule: given fixed compute, there is an optimal way to
split it between bigger models and more training tokens. This paper turned
"just scale it" from folklore into engineering.

## Key concepts

- **Power-law scaling**: loss = a·N^-α + b·D^-β + …, so each doubling of
  resources buys a predictable gain. Plot log-loss vs log-compute: a line.
- **Sample efficiency**: bigger models reach the same loss on fewer tokens —
  relevant when your dataset is small by web standards.
- **Compute-optimal allocation**: don't just grow parameters; the paper says
  how to divide a fixed FLOP budget (later corrected by Chinchilla).
- **Overfitting regime**: too-big model on too-little data breaks the curves
  — the formalism behind your memorization checks.
- **Weak architecture dependence**: width vs depth barely moves loss, which
  justifies treating your 0.5B model as "a Transformer, full stop".

## Why it matters here

Your whole project is a scaling-law footnote: tiny model, tiny data, tiny
compute. The laws tell you what performance is even plausible and why the
course bets on data quality and inference compute instead of parameters.

## Links

- Paper: https://arxiv.org/abs/2001.08361
- Video: [Neural Scaling Laws and GPT-3 — Jared Kaplan (the author himself)](https://www.youtube.com/watch?v=sNfkZFVm_xs)

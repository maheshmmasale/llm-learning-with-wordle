# Direct Preference Optimization (Rafailov et al., 2023)

## Gist

RLHF works but needs four models and PPO gymnastics. DPO's insight: the
optimal policy for a Bradley-Terry preference model has a **closed form**,
so you can skip the reward model and RL entirely — finetune directly on
(chosen, rejected) pairs with one cross-entropy-like loss. Same alignment
signal, one training run, no PPO instability.

## How it works

Start from the RLHF objective (maximize reward minus β·KL to a reference)
and solve it analytically: the optimal reward can be rewritten purely in
terms of the optimal policy's log-ratios. Plug that expression into the
Bradley-Terry preference model and the reward cancels out — leaving a loss
that raises the winner's likelihood relative to the loser, both measured
against the frozen reference model. One hyperparameter, β, sets how hard
the KL leash pulls. Training is a single supervised run on preference pairs;
no sampling loop, no value network, no clipping.

## Key concepts

- **Preference pairs**: (prompt, winner, loser). Cheaper than rankings,
  sufficient for the Bradley-Terry model underneath.
- **Bradley-Terry model**: P(winner ≻ loser) = σ(r(winner) − r(loser)) —
  human taste as a noisy comparison function.
- **Implicit reward**: DPO never builds an RM; the policy's own log-ratio
  against a frozen reference *is* the reward. "Your language model is
  secretly a reward model."
- **Reference policy**: the KL anchor, usually the SFT model — same leash
  idea as PPO, implemented as a loss term instead of a training loop.
- **Beta**: the single temperature knob trading preference fit against
  staying close to the reference.

## Why learn this

DPO is the art of deleting machinery: a four-model RL pipeline reduced to
one loss function by solving the math first. That move — find the closed
form, dissolve the pipeline — is the highest-leverage skill in ML
engineering, and this paper is its cleanest recent demonstration.

## Links

- Paper: https://arxiv.org/abs/2305.18290
- Video: [DPO paper explained — AI Coffee Break](https://www.youtube.com/watch?v=XZLc09hkMwA)

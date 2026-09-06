# Direct Preference Optimization (Rafailov et al., 2023)

## Gist

RLHF works but needs four models and PPO gymnastics. DPO's insight: the
optimal policy for a Bradley-Terry preference model has a **closed form**,
so you can skip the reward model and RL entirely — finetune directly on
(chosen, rejected) pairs with one cross-entropy-like loss. Same alignment
signal, one training run, no PPO instability.

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

## Why it matters here

DPO is the pragmatic alignment upgrade path after your LoRA milestone: same
preference-pair data idea, none of RLHF's infrastructure. If milestone 8
ever grows teeth, this — not PPO — is the algorithm you'd actually run.

## Links

- Paper: https://arxiv.org/abs/2305.18290
- Video: [DPO paper explained — AI Coffee Break](https://www.youtube.com/watch?v=XZLc09hkMwA)

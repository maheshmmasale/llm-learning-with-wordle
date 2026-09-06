# DeepSeekMath: Pushing the Limits of Mathematical Reasoning (Shao et al., 2024)

## Gist

The paper's headline is math scores, but its lasting contribution is
**GRPO**: PPO needs a learned value network as big as the policy; GRPO
replaces it by sampling a *group* of answers per prompt and normalizing
rewards **within the group**. No critic model, half the memory, better math
— and the algorithm that later trained DeepSeek-R1.

## Key concepts

- **Critic/value model**: PPO's baseline estimator — expensive twin of the
  policy whose only job is "how good is average here?".
- **Group-relative advantage**: generate G answers, score them, advantage =
  (reward − group mean) / group std. The group *is* the baseline.
- **KL penalty kept**: like PPO, GRPO anchors to a reference policy so RL
  doesn't degenerate the language model.
- **Outcome + format rewards**: DeepSeekMath mixed correctness with
  language-mixing penalties — reward design matters as much as algorithm.
- **Iterative SFT↔RL**: the paper alternates data collection and training,
  a loop your dataset milestone could copy at small scale.

## Why it matters here

TRL (already in `requirements-ml.txt`) ships a GRPOTrainer. If you attempt
milestone 8's optional RL, GRPO — not PPO — is the feasible choice on one
GPU, precisely because it drops the critic.

## Links

- Paper: https://arxiv.org/abs/2402.03300
- Video: [GRPO Reinforcement Learning Explained, DeepSeekMath Paper — AI Papers Academy](https://www.youtube.com/watch?v=YCawyzAOg1Y)

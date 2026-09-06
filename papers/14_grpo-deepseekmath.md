# DeepSeekMath: Pushing the Limits of Mathematical Reasoning (Shao et al., 2024)

## Gist

The headline is math scores, but the lasting contribution is **GRPO**: PPO
needs a learned value network as big as the policy; GRPO replaces it by
sampling a *group* of answers per prompt and normalizing rewards **within
the group**. No critic model, half the memory, better math — and the
algorithm that later trained DeepSeek-R1.

## How it works

For each prompt, sample G completions and score them all. Advantage for
completion i = (reward_i − group_mean) / group_std — the group mean is the
baseline, so no value network is ever trained. Plug these advantages into a
PPO-style clipped surrogate with the usual KL-to-reference penalty, and add
outcome rewards (correct math) plus format rewards (e.g., no language
mixing). Around the RL sits an iterative loop: SFT on collected data, RL to
improve, use the improved model to collect harder data, repeat.

## Key concepts

- **Critic/value model**: PPO's baseline estimator — expensive twin of the
  policy whose only job is "how good is average here?".
- **Group-relative advantage**: generate G answers, score them, advantage =
  (reward − group mean) / group std. The group *is* the baseline.
- **KL penalty kept**: like PPO, GRPO anchors to a reference policy so RL
  doesn't degenerate the language model.
- **Outcome + format rewards**: correctness plus style constraints — reward
  design matters as much as algorithm.
- **Iterative SFT↔RL**: alternate data collection and training; each round's
  model generates the next round's training distribution.

## Why learn this

GRPO teaches two portable lessons: baselines are variance-reduction devices
and can be built from data you already have (no critic needed), and RL
success lives or dies on reward design, not algorithm choice. Both apply far
beyond math — anywhere you'd optimize a model against a scorer.

## Links

- Paper: https://arxiv.org/abs/2402.03300
- Video: [GRPO Reinforcement Learning Explained, DeepSeekMath Paper — AI Papers Academy](https://www.youtube.com/watch?v=YCawyzAOg1Y)

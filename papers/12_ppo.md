# Proximal Policy Optimization Algorithms (Schulman et al., 2017)

## Gist

Policy-gradient RL is unstable: one oversized update can collapse a policy
forever. PPO's fix is embarrassingly simple — **clip** how far each update
may move the policy from its previous self. The clipped surrogate objective
keeps the trust-region benefits of complex predecessors (TRPO) with
first-order simplicity. It became the default RL algorithm and the engine
inside RLHF.

## How it works

Standard policy gradient ascends E[ratio × advantage], where the ratio is
how much more likely an action is under the new policy. PPO replaces it with
min(ratio × A, clip(ratio, 1−ε, 1+ε) × A): improvements beyond the trust
boundary simply stop counting, so no minibatch can yank the policy far.
Advantages come from **GAE** (exponentially-weighted multi-step returns
trading bias against variance). Training loops over several epochs of the
same fresh rollouts, jointly fitting a value function and adding an entropy
bonus for exploration. On-policy data only — stable, sample-hungry.

## Key concepts

- **Policy gradient**: reinforce actions that led to reward; the gradient
  points toward "do more of what worked".
- **Trust region**: only update within a safe neighborhood of the current
  policy. TRPO enforced this with hard constraints; PPO approximates it.
- **Clipped objective**: if the probability ratio for an action leaves
  [1−ε, 1+ε], clip it — gains beyond the boundary don't count. Stability
  in one line of code.
- **Advantage estimation (GAE)**: how much better was this action than
  average? PPO's signal quality comes from generalized advantage estimation.
- **On-policy**: learn only from fresh rollouts of the current policy —
  sample-inefficient but stable, the opposite of Q-learning-style replay.

## Why learn this

PPO teaches stability engineering: most RL failures are step-size failures,
and clipping is the general principle "don't move faster than your data
supports." That intuition transfers well beyond RL — to finetuning learning
rates, KL leashes, and any iterative process that can collapse from one bad
update.

## Links

- Paper: https://arxiv.org/abs/1707.06347
- Video: [PPO: Theoretical Foundations of LLM Post-Training — ExplainingML](https://www.youtube.com/watch?v=Zfr9l_4qYwA)

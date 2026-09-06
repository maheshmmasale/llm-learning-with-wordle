# Proximal Policy Optimization Algorithms (Schulman et al., 2017)

## Gist

Policy-gradient RL is unstable: one oversized update can collapse a policy
forever. PPO's fix is embarrassingly simple — **clip** how far each update
may move the policy from its previous self. The clipped surrogate objective
keeps the trust-region benefits of complex predecessors (TRPO) with
first-order simplicity. It became the default RL algorithm and the engine
inside RLHF.

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

## Why it matters here

PPO is the "P" in the RLHF your course deliberately skips — but TRL (in
your requirements) ships PPO and GRPO trainers, and milestone 8's optional
RL track starts here. Understand clipping and you've understood 80% of it.

## Links

- Paper: https://arxiv.org/abs/1707.06347
- Video: [PPO: Theoretical Foundations of LLM Post-Training — ExplainingML](https://www.youtube.com/watch?v=Zfr9l_4qYwA)

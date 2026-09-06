# Let's Verify Step by Step (Lightman et al., 2023)

## Gist

To judge reasoning, grade the **final answer** (outcome supervision) or
**each step** (process supervision)? OpenAI trained both kinds of reward
models on math and found process supervision wins decisively (78% on MATH)
— and exposed why: outcome-supervised models "regularly use incorrect
reasoning to reach the correct final answer." Right answers, wrong reasons.

## Key concepts

- **Outcome supervision (ORM)**: one label per solution — correct or not.
  Cheap, but rewards lucky guesses and hallucinated chains.
- **Process supervision (PRM)**: a label per reasoning step, from the
  800k-label PRM800K dataset the paper released. Expensive, honest.
- **Credit assignment**: which step deserves blame? PRMs localize errors;
  ORMs smear one label over the whole chain.
- **Best-of-N with a verifier**: sample many solutions, let the reward
  model pick — the inference-time pattern your milestone 7 reranker copies.
- **Alignment tax note**: process supervision was *more* interpretable and
  safer while performing better — a rare free lunch, worth remembering.

## Why it matters here

Your verifier in milestone 7 (legality + constraint checks) is a
deterministic baby PRM: it judges the *move*, not just the win. And the
paper's headline finding is your warning about SFT on solver data — a model
can output the right guess for reasons that won't generalize.

## Links

- Paper: https://arxiv.org/abs/2305.20050
- Video: [Reward Models Explained: What Actually Trains Reasoning](https://www.youtube.com/watch?v=xrt7NMDuURc)

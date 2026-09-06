# Self-Consistency Improves Chain of Thought (Wang et al., 2022)

## Gist

Greedy decoding takes the single most likely reasoning path — which may
contain one fatal slip. Self-consistency instead **samples many paths**
(temperature > 0) and takes a **majority vote** on the final answer.
Different paths make different mistakes; the right answer recurs. On GSM8K
math, +18 points over plain CoT. Test-time compute traded directly for
accuracy — no retraining.

## How it works

Replace greedy decode with temperature sampling: generate k full
reasoning-plus-answer paths (k = 5–40 in the paper). Normalize the final
answers (strip formatting so "42" == "forty-two" == "$42$") and take the
mode. Mathematically this marginalizes out the latent reasoning: P(answer) ≈
fraction of paths reaching it. Gains grow with k then saturate; the method
stacks with better base prompts and better models. Failure mode to watch:
if the model is *systematically* wrong (same misconception every path),
voting amplifies the error instead of fixing it.

## Key concepts

- **Greedy vs sampled decoding**: temperature 0 = the likeliest path only;
  higher temperature = diverse attempts, some wrong, collectively wise.
- **Majority vote / marginalization**: P(answer) ≈ fraction of paths
  reaching it. Formally, marginalizing out the latent reasoning.
- **Diversity requirement**: identical samples don't help — track *unique*
  answers, not total samples.
- **Cost model**: k paths = k× inference cost. The cheapest point on every
  inference-scaling curve.
- **Limits**: voting needs a well-defined answer to vote on. Fragmented
  answer spaces (free-form guesses) break the vote — rerank instead.

## Why learn this

Self-consistency is the minimal example of a universal tradeoff: inference
dollars for accuracy points, no training involved. Learning to plot that
curve — and to recognize when voting helps (convergent answers) versus hurts
(shared misconceptions) — prepares you for every fancier inference-scaling
method, which are all elaborations on "spend compute, aggregate smartly."

## Links

- Paper: https://arxiv.org/abs/2203.11171
- Video: [Why Self-Consistency Makes LLMs Smarter — Phenom](https://www.youtube.com/watch?v=dQ6-aGKW2CI)

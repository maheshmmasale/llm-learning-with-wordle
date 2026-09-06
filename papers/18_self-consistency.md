# Self-Consistency Improves Chain of Thought (Wang et al., 2022)

## Gist

Greedy decoding takes the single most likely reasoning path — which may
contain one fatal slip. Self-consistency instead **samples many paths**
(temperature > 0) and takes a **majority vote** on the final answer.
Different paths make different mistakes; the right answer recurs. On GSM8K
math, +18 points over plain CoT. Test-time compute traded directly for
accuracy — no retraining.

## Key concepts

- **Greedy vs sampled decoding**: temperature 0 = the likeliest path only;
  higher temperature = diverse attempts, some wrong, collectively wise.
- **Majority vote / marginalization**: P(answer) ≈ fraction of paths
  reaching it. Formally, marginalizing out the latent reasoning.
- **Diversity requirement**: identical samples don't help — track *unique*
  answers, not total samples (your milestone 7 must log this).
- **Cost model**: k paths = k× inference cost. This is the cheapest point
  on every inference-scaling curve you will plot.
- **Limits**: voting needs a well-defined answer to vote on. Wordle guesses
  fragment the vote — which is why your solver reranks instead.

## Why it matters here

Milestone 7's first technique. `solutions/07_scaling` implements exactly
this (`self_consistency`), and your compute-frontier plots start with the
question: does 8× inference buy enough Wordle wins to matter?

## Links

- Paper: https://arxiv.org/abs/2203.11171
- Video: [Why Self-Consistency Makes LLMs Smarter — Phenom](https://www.youtube.com/watch?v=dQ6-aGKW2CI)

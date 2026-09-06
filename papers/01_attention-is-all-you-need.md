# Attention Is All You Need (Vaswani et al., 2017)

## Gist

Before this paper, sequence models read text one token at a time with RNNs,
which is slow and forgets distant context. The authors threw out recurrence
entirely and built the **Transformer** from one mechanism: attention, which
lets every token directly look at every other token. Result: better
translation quality with far less training time. Every model in this course
is a Transformer descendant.

## Key concepts

- **Attention**: each token scores how relevant every other token is, then
  takes a weighted mix of their meanings. "It" in "the animal didn't cross
  the street because it was too tired" attends to "animal".
- **Self-attention**: the sequence attending to itself, all positions at
  once — this is what makes training parallelizable.
- **Multi-head attention**: several attention mechanisms in parallel, each
  free to track a different relation (grammar, coreference, position).
- **Positional encoding**: since there is no reading order anymore, a
  position signal is added to each token so order information survives.
- **Encoder–decoder**: the original setup (translation); GPT-style models
  keep only the decoder half, which predicts the next token.

## Why it matters here

SmolLM, Qwen, TinyLlama — your SFT targets — are all decoder-only
Transformers. Understanding attention tells you what the model can and
cannot track, which is exactly what your Wordle prompts must compensate for.

## Links

- Paper: https://arxiv.org/abs/1706.03762
- Video: [Attention in transformers, step-by-step — 3Blue1Brown](https://www.youtube.com/watch?v=eMlx5fFNoYc)

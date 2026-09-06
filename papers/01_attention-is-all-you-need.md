# Attention Is All You Need (Vaswani et al., 2017)

## Gist

Before this paper, sequence models read text one token at a time with RNNs,
which is slow and forgets distant context. The authors threw out recurrence
entirely and built the **Transformer** from one mechanism: attention, which
lets every token directly look at every other token. Result: better
translation quality with far less training time. Every modern model is a
Transformer descendant.

## How it works

Each token is projected into three vectors: a **query** (what am I looking
for?), a **key** (what do I offer?), and a **value** (what do I contribute?).
Attention scores are dot products of queries against all keys, scaled by
√d and soft-maxed into weights; the output is the weighted mix of values.
**Multi-head** means running this 8–16 times in parallel with different
projections, then concatenating — each head free to track a different
relation. Since nothing now encodes order, **sinusoidal positional
encodings** are added to inputs. The encoder uses unmasked self-attention;
the decoder masks future positions and adds cross-attention to the encoder.
Because every position computes simultaneously, training parallelizes across
GPUs instead of crawling left to right.

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

## Why learn this

Attention is the primitive behind every model you will ever load. Once you
can hand-compute one head — queries, keys, softmax, mix — Transformers stop
being magic: architecture papers become parts lists, prompting becomes
context-shaping, and failures ("lost in the middle", position effects) turn
into predictable consequences instead of mysteries.

## Links

- Paper: https://arxiv.org/abs/1706.03762
- Video: [Attention in transformers, step-by-step — 3Blue1Brown](https://www.youtube.com/watch?v=eMlx5fFNoYc)

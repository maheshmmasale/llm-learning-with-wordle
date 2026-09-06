# Chain-of-Thought Prompting Elicits Reasoning (Wei et al., 2022)

## Gist

Add "let's think step by step" (or a few worked examples) and large models
suddenly solve math and logic tasks they flunked outright. Intermediate
tokens act as scratch space: each reasoning step is more computation spent
before committing to an answer. The gains appear with scale — small models
benefit less, which your milestone 3 will confirm firsthand.

## Key concepts

- **Intermediate tokens as compute**: generating steps buys serial
  computation. No steps = one forward pass per token of the answer; CoT =
  many passes of "thinking" first.
- **Few-shot CoT**: worked examples showing *how* to reason, not just final
  answers. Format of the scratchpad matters as much as its presence.
- **Zero-shot CoT**: the magic sentence "Let's think step by step" with no
  examples at all — weaker, but free.
- **Emergence**: CoT helps 100B+ models far more than small ones. Your 0.5B
  model may barely budge — that negative result is itself the lesson.
- **Faithfulness caveat**: the shown reasoning isn't guaranteed to be the
  real reasoning. Never treat CoT as an audit trail.

## Why it matters here

Your milestone-3 "structured reasoning" prompts are CoT applied to Wordle:
list greens, exclusions, multiplicities, then guess. The paper predicts your
small model will gain little — test that prediction, don't assume it.

## Links

- Paper: https://arxiv.org/abs/2201.11903
- Video: [Chain of Thought Prompting: Why Reasoning Out Loud Works — Eau Claire AI](https://www.youtube.com/watch?v=DLd3mhIAr04)

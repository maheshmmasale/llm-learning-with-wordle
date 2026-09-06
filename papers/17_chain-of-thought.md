# Chain-of-Thought Prompting Elicits Reasoning (Wei et al., 2022)

## Gist

Add "let's think step by step" (or a few worked examples) and large models
suddenly solve math and logic tasks they flunked outright. Intermediate
tokens act as scratch space: each reasoning step is more computation spent
before committing to an answer. The gains appear with scale — small models
benefit less, which is worth verifying rather than assuming.

## How it works

In **few-shot CoT**, prompt exemplars pair each question with a written
solution trace, not just the answer; the model continues the pattern,
generating its own trace before answering. **Zero-shot CoT** appends "Let's
think step by step" with no examples — weaker but free. Why does it help?
Each generated token is another full forward pass: a 50-token rationale is
50× the serial computation of blurting the answer, spent in a form the
model's next-token machinery can use. Ablations show language traces beat
equation-only traces, and gains concentrate on multi-step tasks (GSM8K math,
commonsense, symbolic manipulation) while single-step tasks barely move.

## Key concepts

- **Intermediate tokens as compute**: generating steps buys serial
  computation. No steps = one forward pass per token of the answer; CoT =
  many passes of "thinking" first.
- **Few-shot CoT**: worked examples showing *how* to reason, not just final
  answers. Format of the scratchpad matters as much as its presence.
- **Zero-shot CoT**: the magic sentence "Let's think step by step" with no
  examples at all — weaker, but free.
- **Emergence**: CoT helps 100B+ models far more than small ones.
- **Faithfulness caveat**: the shown reasoning isn't guaranteed to be the
  real reasoning. Never treat CoT as an audit trail.

## Why learn this

CoT teaches the compute-via-tokens mental model: inference spending is a
design variable, not a fixed cost. It also teaches technique
scale-dependence — a method's paper result on giant models says little about
your small one. "Reproduce the gain at your scale before building on it" is
a habit this paper rewards.

## Links

- Paper: https://arxiv.org/abs/2201.11903
- Video: [Chain of Thought Prompting: Why Reasoning Out Loud Works — Eau Claire AI](https://www.youtube.com/watch?v=DLd3mhIAr04)

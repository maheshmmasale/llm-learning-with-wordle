# Hints: Establish Model Baselines

> **Try without hints first.** A useful baseline is simple, reproducible, and honest about failure. Reveal hints only when you need them.

## Level 1 — Load once, evaluate many times

Choose a public causal language model in the project’s target size range and record its exact model identifier, revision, dtype, and decoding settings.

Load the tokenizer and model outside the per-game loop. Put the model in evaluation mode and use inference/no-gradient context. First verify that one fixed prompt produces output before launching a benchmark.

## Level 2 — A guess is not always one token

Do not assume a five-letter word corresponds to one tokenizer token. The model may emit:

- leading whitespace,
- multiple tokens for one word,
- punctuation or explanation,
- lowercase text,
- several candidate words.

Define a deterministic parser that extracts one proposed five-letter alphabetic word. Log both the raw generation and parsed action so parser failures are diagnosable. If comparing models, keep parser rules fixed.

## Level 3 — Decide invalid-word behavior in advance

The environment and benchmark must specify what happens when the model emits an invalid action. Reasonable choices include:

- consume the turn and return an invalid-action observation,
- retry once under a fixed repair prompt while counting the extra model call,
- constrain decoding to legal words.

These are different systems, so do not silently replace an invalid guess with a valid one. Report invalid-word rate and account for retries in inference compute. Include a simple non-model baseline such as random legal guessing or a fixed opening plus candidate filtering.

## Level 4 — Prompt a strong reference consistently

Treat the reference as a measured system, not an oracle with unspecified privileges. Give it the same visible history and six-turn limit, and document whether it receives the legal word list or candidate list.

A minimal reference prompt might be:

```text
You are playing standard five-letter Wordle.
Return exactly one legal five-letter English word and nothing else.

History:
1. CRANE -> ⬛ 🟨 ⬛ 🟩 ⬛
2. ...

Choose the next guess. Do not claim to know the hidden target.
```

Use deterministic or explicitly seeded decoding where supported. Save per-game traces, model-call counts, generated-token counts, latency, and failures. Evaluate all baselines on the same frozen target set; otherwise the percentages are not directly comparable.

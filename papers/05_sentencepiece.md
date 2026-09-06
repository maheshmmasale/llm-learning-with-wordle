# SentencePiece (Kudo & Richardson, 2018)

## Gist

Neural models can't have a vocabulary entry for every word, so text is split
into **subword pieces** ("unhappiness" → "un" + "happiness"). SentencePiece
trains that splitting directly from raw sentences — no pre-tokenization,
language-independent — and is fully reversible. It (and its cousin BPE) is
why models see fragments, not words.

## How it works

Feed raw sentences (no word splitting, so Chinese and code work too).
Spaces are escaped as ▁ so detokenization is lossless. Two training modes:
**BPE** starts from characters and merges the most frequent adjacent pairs
until the vocab budget fills; **unigram** starts from a huge candidate set
and prunes via EM, keeping pieces that maximize corpus likelihood, with
Viterbi segmentation at encode time. A bonus feature, **subword
regularization**, samples alternate segmentations during training so the
model never overfits to one splitting.

## Key concepts

- **Subword tokenization**: the compromise between whole words (huge vocab,
  unknown words break) and characters (long sequences, slow).
- **BPE / unigram**: two splitting algorithms — BPE merges frequent pairs
  bottom-up; unigram starts big and prunes. Both produce piece vocabularies.
- **Reversibility**: detokenizing pieces must restore the exact original
  text — SentencePiece guarantees this by treating space as a character.
- **Fertility**: how many pieces one word becomes. Short words can be 1–3
  tokens, which is why models fumble letter-level constraints.
- **Vocabulary size tradeoff**: bigger vocab = shorter sequences but a
  bigger embedding matrix; ~32k–128k is the usual range.

## Why learn this

Tokenization is the model's actual input — everything downstream inherits
its quirks. Fertility explains why letter games are hard, multilingual gaps,
and half your "model is stupid" moments. Anyone who debugs model behavior
without understanding tokens is debugging blind.

## Links

- Paper: https://arxiv.org/abs/1808.06226
- Video: [Let's build the GPT Tokenizer — Karpathy, BPE from scratch](https://www.youtube.com/watch?v=zduSFxRajkE)

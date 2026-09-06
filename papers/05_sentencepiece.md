# SentencePiece (Kudo & Richardson, 2018)

## Gist

Neural models can't have a vocabulary entry for every word, so text is split
into **subword pieces** ("unhappiness" → "un" + "happiness"). SentencePiece
trains that splitting directly from raw sentences — no pre-tokenization,
language-independent — and is fully reversible. It (and its cousin BPE) is
why your model sees fragments, not words.

## Key concepts

- **Subword tokenization**: the compromise between whole words (huge vocab,
  unknown words break) and characters (long sequences, slow).
- **BPE / unigram**: two splitting algorithms — BPE merges frequent pairs
  bottom-up; unigram starts big and prunes. Both produce piece vocabularies.
- **Reversibility**: detokenizing pieces must restore the exact original
  text — SentencePiece guarantees this by treating space as a character.
- **Fertility**: how many pieces one word becomes. A 5-letter Wordle answer
  may be 1–3 tokens, which is why models fumble letter-level constraints.
- **Vocabulary size tradeoff**: bigger vocab = shorter sequences but a
  bigger embedding matrix; ~32k–128k is the usual range.

## Why it matters here

Your model does not see "CRANE", it sees pieces like "CR" + "ANE". Any
prompt asking for positional letter reasoning fights the tokenizer — this
paper explains why five-letter guesses are oddly hard and why candidate
lists in prompts help so much.

## Links

- Paper: https://arxiv.org/abs/1808.06226
- Video: [Let's build the GPT Tokenizer — Karpathy, BPE from scratch](https://www.youtube.com/watch?v=zduSFxRajkE)

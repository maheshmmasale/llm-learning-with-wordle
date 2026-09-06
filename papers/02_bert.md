# BERT (Devlin et al., 2018)

## Gist

GPT-style models read left-to-right, so "bank" can't use the words after it.
BERT reads **both directions at once**: randomly mask 15% of tokens and train
the model to reconstruct them from full surrounding context. This
bidirectional pretraining plus a next-sentence task made BERT state of the
art on eleven language tasks at once, and started the pretrain-then-finetune
era.

## How it works

Text is WordPiece-tokenized with `[CLS]`/`[SEP]` markers; 15% of tokens are
chosen for masking (80% replaced with `[MASK]`, 10% with random tokens, 10%
left unchanged, so the model can't just pattern-match masks). Two losses
train jointly: **masked LM** (predict hidden tokens from both sides) and
**next-sentence prediction** (does sentence B follow A?). The 12- or
24-layer bidirectional encoder trains on BooksCorpus + Wikipedia, then each
downstream task needs only one new output layer finetuned briefly — the same
weights seed them all.

## Key concepts

- **Masked language modeling (MLM)**: hide tokens, predict them from both
  sides. The training signal is free — any text becomes a dataset.
- **Bidirectional context**: meaning flows left-to-right and right-to-left,
  unlike autoregressive models that only see the past.
- **Encoder**: BERT keeps the Transformer's understanding half and drops
  generation — great for classification, not for writing text.
- **Pretrain then finetune**: one expensive general training run, then cheap
  adaptation per task. LoRA is the modern version of step two.
- **[CLS] token**: a special position whose embedding summarizes the whole
  input for classification decisions.

## Why learn this

This paper teaches the transfer-learning paradigm that still runs the field:
general pretraining, cheap adaptation. MLM is also the cleanest example of
manufacturing supervision from raw text — once you see it, you start spotting
free training signals everywhere, which is the core skill behind all
synthetic-data work.

## Links

- Paper: https://arxiv.org/abs/1810.04805
- Video: [BERT Explained | Bidirectional Transformer Model in NLP](https://www.youtube.com/watch?v=kL-0UJSyh94)

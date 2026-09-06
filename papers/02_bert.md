# BERT (Devlin et al., 2018)

## Gist

GPT-style models read left-to-right, so "bank" can't use the words after it.
BERT reads **both directions at once**: randomly mask 15% of tokens and train
the model to reconstruct them from full surrounding context. This
bidirectional pretraining plus a next-sentence task made BERT state of the
art on eleven language tasks at once, and started the pretrain-then-finetune
era this course lives in.

## Key concepts

- **Masked language modeling (MLM)**: hide tokens, predict them from both
  sides. The training signal is free — any text becomes a dataset.
- **Bidirectional context**: meaning flows left-to-right and right-to-left,
  unlike autoregressive models that only see the past.
- **Encoder**: BERT keeps the Transformer's understanding half and drops
  generation — great for classification, not for writing guesses.
- **Pretrain then finetune**: one expensive general training run, then cheap
  adaptation per task. Your LoRA milestone is the modern version of step two.
- **[CLS] token**: a special position whose embedding summarizes the whole
  input for classification decisions.

## Why it matters here

You will finetune decoder models, not BERT — but BERT is why the field
believes small models plus the right training recipe beat bigger models
with the wrong one. MLM is also the cleanest example of getting supervision
for free, the trick your synthetic Wordle data reuses.

## Links

- Paper: https://arxiv.org/abs/1810.04805
- Video: [BERT Explained | Bidirectional Transformer Model in NLP](https://www.youtube.com/watch?v=kL-0UJSyh94)

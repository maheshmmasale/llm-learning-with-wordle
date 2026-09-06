# Datasheets for Datasets (Gebru et al., 2018)

## Gist

Every electronics part ships with a datasheet; ML datasets shipped with
nothing. This paper proposes a fixed questionnaire — motivation, composition,
collection, preprocessing, uses, distribution, maintenance — that every
dataset should answer before release. It turned "document your data" from
advice into a reviewable artifact and underlies modern data/model cards.

## Key concepts

- **Motivation**: why was this dataset built, by whom, funded by whom?
  Misaligned incentives here corrupt everything downstream.
- **Composition**: what's inside, what's missing, which populations are
  underrepresented — the section that catches bias before training does.
- **Collection & preprocessing**: how raw material became rows: sampling,
  filters, labelers, pay, consent. Your solver-teacher pipeline needs this.
- **Recommended uses (and non-uses)**: the authors demand explicit scope —
  "trained on 65 common words, not valid for rare-word claims" is this habit.
- **Distribution & maintenance**: versioning, updates, deprecation. A
  dataset is software with a lifecycle, not a file.

## Why it matters here

Milestone 5 requires a data card and leakage audit — that *is* a datasheet.
The companion video below covers the sibling Data Cards framework (Google
PAIR, FAccT 2022): same spirit, industry packaging. Read both, write one.

## Links

- Paper: https://arxiv.org/abs/1803.09010
- Video: [Data Cards: Purposeful and Transparent Documentation — ACM FAccT](https://www.youtube.com/watch?v=jcQ4A2EbFW8)

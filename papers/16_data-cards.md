# Datasheets for Datasets (Gebru et al., 2018)

## Gist

Every electronics part ships with a datasheet; ML datasets shipped with
nothing. This paper proposes a fixed questionnaire — motivation, composition,
collection, preprocessing, uses, distribution, maintenance — that every
dataset should answer before release. It turned "document your data" from
advice into a reviewable artifact and underlies modern data/model cards.

## How it works

57 questions across 7 lifecycle stages, each with a rationale for why the
answer matters. **Motivation** (purpose, creators, funding) exposes
incentive problems. **Composition** (instances, missing pieces, subpopulation
breakdown) surfaces bias before training does. **Collection** (sources,
sampling, consent, annotator pay) and **preprocessing** (cleaning, labels,
raw-data retention) make the pipeline auditable. **Uses** demands explicit
in-scope/out-of-scope tasks. **Distribution and maintenance** treat the
dataset as versioned software with updates and deprecation. Two fully worked
examples (Labeled Faces in the Wild, polarity data) show what good answers
look like.

## Key concepts

- **Motivation**: why was this dataset built, by whom, funded by whom?
  Misaligned incentives here corrupt everything downstream.
- **Composition**: what's inside, what's missing, which populations are
  underrepresented — the section that catches bias before training does.
- **Collection & preprocessing**: how raw material became rows: sampling,
  filters, labelers, pay, consent.
- **Recommended uses (and non-uses)**: explicit scope — "valid for common
  words, not for rare-word claims" is this habit.
- **Distribution & maintenance**: versioning, updates, deprecation. A
  dataset is software with a lifecycle, not a file.

## Why learn this

The questionnaire habit transfers to any data you touch: asking these
questions *before* collecting changes what you collect, which is enormously
cheaper than discovering bias after training. And "documentation as
engineering artifact" generalizes — model cards, eval reports, and incident
writeups all rhyme with it.

## Links

- Paper: https://arxiv.org/abs/1803.09010
- Video: [Data Cards: Purposeful and Transparent Documentation — ACM FAccT](https://www.youtube.com/watch?v=jcQ4A2EbFW8) (covers the sibling Data Cards framework — same spirit, industry packaging)

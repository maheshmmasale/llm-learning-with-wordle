# Problem 05 — Building a Supervised Dataset from an Entropy Solver

## Module context

Fine-tuning is only as good as its data: solver-only trajectories teach
openings, not state-dependent decisions. Treat dataset construction as an
experiment — define the teacher, diversify states, preserve provenance, and
prevent leakage.

- Theory: `theory/05_training_and_sft.md`
- Reference solution: `src/solutions/05_dataset/`
- Maintained library: `src/training/dataset.py`

## Objective

Ship a reproducible pipeline producing **≥100,000 validated unique
state→next-guess rows** labeled by an entropy solver, split into
leak-proof train/validation/test with a data card — no model training here.

## Requirements

1. CLI generator: seed, output dir, row count, solver config, split config;
   invocation + effective parameters saved in a manifest.
2. Label every row with the entropy solver; mark exact vs approximate with
   the approximation budget. Define both terms in metadata.
3. Cover early/middle/late states, candidate-count bands, and difficulty —
   no opening-position monoculture.
4. JSONL rows carry: schema version, state id, canonical history, candidates
   (or audit hash), label, score, ties, seed/provenance, split id.
5. Validate (legal guesses/feedback, consistent histories, recomputed sample
   scores), count rejections by reason, dedupe before splitting.
6. Split by grouping key (target/puzzle family), never by row; automated
   leakage audit must pass.
7. Provide a loader + verify command (schema, hashes, split exclusivity,
   minimum count, label sample).

## Done when

- ≥100k unique rows, all splits nonempty; rerun with same seed =
  identical hashes.
- Sabotage tests (bad histories, duplicates, cross-split groups) all caught.
- Coverage stats show real mid/late-game and difficulty spread.

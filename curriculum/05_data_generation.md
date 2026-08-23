# Module 5 — Generate a Supervised Wordle Dataset

## Why this module matters

Supervised fine-tuning is only as useful as its data. Complete games from one deterministic solver can produce a narrow set of familiar trajectories, allowing a model to imitate openings without learning state-dependent decisions. This module treats dataset construction as an experiment: define the teacher, sample diverse states, preserve provenance, prevent leakage, and measure the quality of labels.

## Learning objectives

By the end of this module, you should be able to:

- Convert Wordle states into supervised input-action examples.
- Use a strong solver to label actions with reproducible scoring rules.
- Generate 100K examples initially and scale toward 1M when justified.
- Sample diverse, difficult, and counterfactual states rather than only full games.
- Create train/validation/test splits that resist target and trajectory leakage.
- Validate legality, consistency, diversity, and label quality.
- Document and version a generated dataset.

## Data schema and teacher

A record should include a schema version, public history, canonical constraints, remaining-candidate count, optional candidate subset, teacher action, teacher score, alternative top actions, turn number, state source, solver version, and split identifier. Never include the hidden target in model-visible text. It may exist in protected metadata for auditing, but training code should deliberately drop it.

Use an entropy-based solver or another declared objective to label strong next guesses. For a guess `g`, partition remaining targets by possible feedback and compute expected information gain. Save ties or top-`k` actions when possible: several moves may be nearly equivalent, and forcing a single label can teach arbitrary preferences.

Recommended resources:

- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)
- [Apache Parquet](https://parquet.apache.org/docs/)
- [Data Cards for Datasets](https://arxiv.org/abs/1803.09010)
- [Dataset fingerprinting](https://huggingface.co/docs/datasets/about_cache)
- [3Blue1Brown Wordle information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)

## Sampling strategy

Combine several state sources:

- states visited by the teacher’s own games;
- states produced by random or weak policies;
- prefixes from LLM trajectories;
- counterfactual legal histories;
- states stratified by turn and remaining-candidate count;
- repeated-letter and rare-letter cases;
- states where entropy and immediate solve probability disagree;
- near-terminal states with two or more plausible answers.

Begin with roughly 100K examples so quality checks and baseline training are cheap. Scale to 250K, 500K, or 1M only after a data-scaling experiment shows value. Deduplicate exact states and measure near-duplicates.

Split by answer identity before trajectory generation, not by randomly shuffling state rows. Otherwise, states derived from the same hidden answer can appear in both training and test. Add a challenge split containing uncommon answers, repeated letters, unusual feedback patterns, and out-of-distribution candidate-set sizes.

## Suggested experiments

1. Teacher trajectories only versus mixed-policy and counterfactual states.
2. Single best action versus top-`k` acceptable actions.
3. Uniform state sampling versus balanced sampling across turns and difficulty.
4. Dataset sizes of 10K, 100K, 250K, and 1M.
5. Inputs with raw history versus canonical constraints versus both.
6. Labels optimized for entropy versus expected candidate count or solve probability.
7. Audit a random sample manually and compare independent solver implementations.

## Questions to answer

- What behavior is encoded by the teacher objective?
- Which important states are underrepresented in natural trajectories?
- Can answer identity or split membership be inferred through accidental metadata?
- How much label ambiguity exists among near-optimal guesses?
- Does the dataset reward legal constraint following, strategic exploration, or both?
- At what size do additional examples stop improving coverage or downstream quality?

## Deliverables

- A deterministic generator with seed, solver, word-list, and schema versions.
- A 100K-example initial dataset in JSONL or Parquet plus a small inspectable sample.
- Train, validation, test, and challenge manifests with leakage checks.
- A data card covering provenance, license, schema, generation method, limitations, and intended use.
- Quality reports for invalid records, duplicates, turn distribution, candidate-set sizes, letter patterns, and teacher-score margins.
- A scaling plan explaining whether generating up to 1M examples is likely to be useful.

**Exit criterion:** a reviewer can regenerate the dataset, verify that held-out answers are protected, and understand exactly which policy the labels teach.
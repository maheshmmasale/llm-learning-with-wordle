# Hints: Generate a Supervised Dataset

> **Try without hints first.** Decide what behavior the labels teach before generating a large dataset. Scale does not rescue a flawed target.

## Level 1 — “Optimal” is objective-dependent

The action that maximizes immediate information gain is not always the action that maximizes probability of solving within the remaining turns. A probe word may split candidates well but cannot be the answer; a likely answer may be better late in the game.

Name labels honestly: `entropy_greedy`, `expected_remaining`, `two_step_search`, or `teacher_action` rather than simply `optimal` unless you can prove optimality under a stated objective.

## Level 2 — Use feedback partitions and entropy

A proposed guess partitions remaining targets by the feedback pattern it would produce. If target probabilities are uniform, compute:

```text
p(pattern) = bucket_size / number_of_candidates
entropy = -sum(p * log2(p))
```

Alternatively minimize expected candidates remaining:

```text
sum(bucket_size^2) / number_of_candidates
```

Cache feedback values or integer-encode patterns; naïvely rescoring every `(state, guess, target)` triple can become the generation bottleneck.

## Level 3 — Sample diverse states, not only complete teacher games

Full trajectories from one strong policy create a narrow state distribution. Add states from:

- random legal guesses,
- weak and strong policies,
- different opening words,
- early, middle, and late turns,
- repeated-letter targets,
- rare words and large/small candidate sets,
- intentionally awkward but reachable histories.

Verify reachability and consistency. Track provenance and difficulty fields so you can stratify evaluation and ablate data sources later.

## Level 4 — Example JSONL schema

One record per state-action example:

```json
{"id":"train-000001","split_group":"target:cigar","history":[{"guess":"crane","feedback":[2,1,0,0,0]}],"turns_left":5,"constraints":{"pattern":"C____","required":["r"],"excluded":["a","n","e"]},"candidate_count":37,"candidate_sample":["cigar","curry"],"label":{"action":"cigar","policy":"expected_remaining_v1","score":1.82},"provenance":{"target_hash":"...","state_source":"mixed_policy","seed":17}}
```

Do **not** include the hidden target in the model-visible input. If you retain it for auditing, keep it in a protected metadata field excluded by the formatter. Split before or during generation by target/family—not by randomly shuffling individual states—so neighboring states from the same game cannot leak across train and test. Save generator version, vocabulary hashes, RNG seed, and label-policy configuration.

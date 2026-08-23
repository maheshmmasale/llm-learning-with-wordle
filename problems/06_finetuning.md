# Problem 06 — Supervised Fine-Tuning with LoRA

## Objective

Develop a reproducible supervised fine-tuning pipeline that teaches a pretrained language model to select strong next guesses from structured game states. Use the dataset produced by an entropy-based expert, preserve a strict **80/10/10 train/validation/test partition**, and train with Low-Rank Adaptation (LoRA) or a clearly justified parameter-efficient variant. The system must support fair evaluation of four policies: **Base**, **Prompted**, **SFT**, and **SFT+Search**.

The goal is not to maximize a single headline score through undocumented prompting or excessive test-time computation. The goal is to establish how much policy quality comes from the pretrained model, task instructions, supervised adaptation, and search. Your work must isolate these effects, provide a harder held-out test regime, and be reproducible on a fresh machine from configuration files and documented commands.

## Background

A supervised state-to-action dataset can be represented as text, structured tokens, or a hybrid serialization. Fine-tuning quality depends on seemingly minor choices: candidate ordering, history formatting, masking of prompt tokens, treatment of multiple optimal labels, truncation, and whether the model is asked to emit only a guess or an explanation plus a guess. LoRA reduces trainable parameter count by injecting low-rank updates into selected model projections, but its effectiveness depends on rank, scaling, dropout, target modules, learning rate, and sequence length.

Evaluation also requires care. Row-wise splitting can leak nearly identical game states. In addition, an ordinary IID test split may be too easy to expose meaningful differences among systems. This assignment therefore requires one deterministic group-aware 80/10/10 partition whose 10% test portion is deliberately harder according to predeclared, label-independent state characteristics. Difficulty must not be chosen after observing model outcomes. The SFT+Search policy may use the trained model inside a bounded inference procedure, but its compute must be measured separately from the direct SFT policy.

## Exact Requirements

1. Implement a training script that accepts model identifier and revision, dataset path and checksum, serialization template, split manifest, seed, LoRA configuration, optimization parameters, and output directory. It must support a dry-run mode on a tiny subset.
2. Preserve a deterministic, group-aware **80% train / 10% validation / 10% test** split by examples, allowing only minimal rounding. No canonical state family, puzzle universe, target group, or other declared leakage unit may cross splits.
3. Construct the test 10% to be harder than the training distribution using predeclared state-only criteria, for example larger action spaces, smaller expert margins, unusual feedback patterns, long histories, or held-out puzzle families. Report both aggregate test results and results by difficulty stratum. Do not move examples based on any trained model’s errors.
4. Use LoRA and save a complete adapter configuration including rank, alpha, dropout, bias policy, target modules, trainable-parameter count, precision, gradient checkpointing status, and base-model revision. Full fine-tuning is optional as an additional experiment, not a substitute.
5. Define the input and target format exactly. Ensure labels do not appear in prompts or auxiliary fields. If reasoning traces are generated, prove they contain no solver-only information unavailable at inference time.
6. Mask tokens correctly so that the declared objective is optimized. State whether loss is computed on answer tokens only or on a broader response and justify the choice.
7. Implement robust parsing of model output into legal actions. Invalid, ambiguous, and out-of-set outputs must be recorded as failures rather than silently repaired, except for a predeclared deterministic normalization layer.
8. Evaluate four systems under matched inputs: **Base** with minimal formatting and no task-specific exemplars; **Prompted** with a fixed task instruction and fixed few-shot examples selected without test access; **SFT** using the trained adapter and direct decoding; and **SFT+Search** using the same adapter with a documented, bounded search or candidate-selection procedure.
9. Keep decoding settings fixed where comparison requires it. For stochastic methods, evaluate multiple seeds and report uncertainty. Track all inference calls, generated tokens, candidate evaluations, and solver operations.
10. Select checkpoints and hyperparameters using validation data only. The test split may be evaluated for final reporting, not used for iterative model selection.
11. Save training curves, evaluation outputs, per-example predictions, adapter weights, machine-readable configurations, package/environment versions, random seeds, hardware description, run duration, and artifact checksums.
12. Provide one command to reproduce the primary training run and one command to reproduce the four-way evaluation from saved artifacts.

## Acceptance Criteria

- Split counts are within documented rounding of 80/10/10, and an automated leakage checker reports zero cross-split group collisions.
- The test split is demonstrably harder according to the predeclared criteria, with distributions reported before model training.
- The training script completes a smoke test, resumes from a checkpoint, and reproduces evaluation from a saved adapter without requiring hidden manual steps.
- LoRA configuration and base-model revision are sufficient to reconstruct the model exactly.
- Per-example evaluation records allow independent recomputation of all aggregate metrics.
- Base, Prompted, SFT, and SFT+Search are evaluated on exactly the same test examples and with clearly separated test-time compute accounting.
- At least three independent seeds are used for the main fine-tuning setting, or a documented resource constraint and a bootstrap confidence analysis is supplied.
- No test-set result is used to choose the prompt, checkpoint, search budget, or hyperparameters.

## Expected Experiments

Run a small hyperparameter study over at least two LoRA ranks and two learning rates, using validation performance and training stability for selection. Compare at least two input serializations, such as compact canonical state encoding versus a natural-language representation. Evaluate answer-only loss against response-level loss if both are feasible. Study the impact of class or state-difficulty reweighting. Compare greedy decoding with a small stochastic sample budget for the SFT model, then reserve more elaborate inference-time scaling for SFT+Search. Include ablations for removing history, removing the remaining-candidate representation, and training without difficult-state balancing. Report whether gains persist across easy, medium, and hard strata.

## What to Measure/Metrics

Primary policy metrics should include exact expert-action agreement, tie-aware agreement, legal-action rate, expert-score regret, top-k action recall, and end-to-end game win rate or solve rate under a fixed game protocol. Report average guesses to solve, failure rate, and worst-case behavior where relevant. Training metrics must include token-level loss, validation loss, learning-rate schedule, gradient norm, throughput, peak memory, trainable parameters, and wall-clock time. Inference metrics must include latency, generated tokens, forward passes, candidate evaluations, and any external solver/search operations per decision and per game. Provide mean, standard deviation or confidence intervals, and stratified metrics by difficulty and state depth.

## Questions to Answer

1. Which improvement comes from task prompting, and which requires changing model weights?
2. Does SFT learn the expert’s policy or merely exploit frequent actions and state templates?
3. How sensitive are conclusions to serialization, LoRA rank, and random seed?
4. What properties make the hard test split difficult, and are they representative of expected deployment states?
5. When SFT+Search outperforms SFT, how much additional compute does the gain require?
6. How are multiple expert-optimal actions scored during training and evaluation?
7. Which error classes remain dominant after fine-tuning: illegal outputs, poor ranking, long-context failures, or distribution shift?
8. What exact evidence demonstrates that the reported test results are uncontaminated by model selection?

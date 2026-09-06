# Problem 3: Systematic Prompting for Wordle Agents

## Module context

Prompting is the cheapest intervention and an essential control: find out how
much capability is already present before touching weights. Design prompt
families and compare them as ablations — producing plausible language is not
the same as tracking exact constraints.

- Hints: `hints/03_prompting.md`
- Theory: `theory/03_prompting_and_representation.md`
- Reference solution: `solutions/03_prompting/`
- Maintained library: `src/models/prompting.py`

## Objective

Design, implement, and evaluate at least five meaningfully different prompt strategies for a language-model Wordle agent. Use a fixed benchmark and controlled inference pipeline to estimate the win-rate delta attributable to prompting rather than answer selection, stochastic decoding, parser changes, or hidden target leakage. Prompts should elicit structured reasoning that is auditable and useful for diagnosis while ensuring that neither the target word nor evaluator-only candidate information enters the model context.

## Background

Prompting can change both the quality of a model’s guesses and its compliance with an interface. In Wordle, those effects are entangled. A prompt might improve constraint tracking but generate verbose text that is hard to parse; another might reduce invalid outputs without improving strategic play. An evaluation that changes prompt, parser, decoding temperature, retry policy, and benchmark answers simultaneously cannot identify why performance moved.

This assignment treats prompting as a controlled research variable. Use the deterministic environment and baseline harness from the earlier problems. Select one model configuration and hold model weights, tokenizer, decoding settings, parser, retry policy, word lists, answer order, and maximum guesses constant. The prompt is the intervention. At least five strategies must differ conceptually, not just by punctuation or synonyms. Examples of prompt families worth considering include a minimal instruction, explicit feedback-rule explanation, a constraint ledger, staged analysis followed by a final-answer field, candidate-comparison guidance, self-checking before submission, or compact few-shot demonstrations. These examples define a design space, not required implementations.

“Structured reasoning” means the prompt requests consistent intermediate fields or checks whose presence and correctness can be scored. It does not authorize revealing the hidden target, injecting the evaluator’s post-feedback candidate set, or presenting information unavailable to a human player. If internal reasoning should not be retained, design concise external state summaries or auditable constraint declarations rather than depending on unrestricted prose.

## Exact Requirements

1. Create at least five distinct prompt strategies plus the frozen baseline prompt from Problem 2. Give each strategy a name, hypothesis, exact template, and version identifier.
2. Keep all non-prompt variables fixed across strategies: model checkpoint, generation configuration, parser, invalid-output policy, game limit, vocabularies, answer schedule, and evaluation code revision.
3. Use one fixed benchmark set and order for all conditions. Predeclare a development subset, if needed, and keep it separate from the final evaluation subset. Do not revise prompts after inspecting final-set answer-level outcomes.
4. Every prompt must describe feedback symbols accurately, including the fact that repeated-letter feedback is count-limited. It may ask the model to reason from observations, but it must not include the hidden answer or evaluator-only knowledge.
5. Require a machine-identifiable final guess using the same parser contract in every condition. Prompt-specific formats may add structured fields, but the final guess extraction rule cannot be made more forgiving for one strategy.
6. At least three strategies must request structured reasoning. Define a schema such as known positions, excluded positions, minimum/maximum letter counts, eliminated letters, candidate rationale, consistency check, and final guess. The exact schema is a design decision to justify.
7. Validate prompt construction with automated leakage tests. Search rendered prompts and model-visible retry messages for the target and for any secret-state serialization. Include tests for answers that also appear in instructions or examples by coincidence.
8. Log the exact rendered prompt or a cryptographic digest plus recoverable template inputs, raw generation, parsed final guess, validity, feedback, and terminal status for each turn.
9. Compute per-strategy win rate and win-rate delta relative to baseline on paired answers. Report uncertainty intervals and avoid claiming superiority from raw point estimates alone.
10. Predefine tie-breaking and selection criteria for the “best” prompt. Include invalid-output behavior, average guesses, token cost, and reasoning consistency rather than optimizing only headline win rate.
11. Do not provide solutions to individual benchmark games in the assignment report. Transcripts may be analyzed internally, but examples in shared documentation should redact targets unless the game is explicitly over and disclosure is necessary.

## Acceptance Criteria

- Six total evaluated conditions exist: the baseline and at least five substantive prompt variants.
- Each condition runs on the identical fixed benchmark with identical inference and parsing settings.
- Prompt templates, hypotheses, configuration IDs, and benchmark identifiers are versioned and recoverable.
- Automated checks find no target leakage in any active-game prompt, retry prompt, or structured state field.
- At least three prompts produce scoreable structured reasoning, and schema-compliance rates are reported.
- Results include paired win-rate deltas from baseline, uncertainty intervals, average guesses, invalid rates, and token usage.
- Statistical and qualitative conclusions distinguish formatting improvements from better Wordle constraint reasoning.
- A rerun with the same seed is reproducible to the level supported by the inference backend, with deviations documented.

## Expected Experiments

Begin with a development-only calibration pass to ensure every template renders, fits the context window, and yields parser-compatible output. Do not use this pass to repeatedly optimize against final benchmark answers. Freeze templates before final evaluation. Run all conditions over the same answer schedule, preferably in an interleaved or otherwise bias-resistant order if the serving backend may drift.

For structured prompts, score whether declared constraints agree with the public game history. Check green-position retention, yellow-position exclusion, minimum and maximum letter counts, eliminated-letter reuse, and consistency between the reasoning fields and final guess. Compare strategy pairs answer by answer to identify wins unique to one prompt. Conduct ablations where scientifically justified—for example, removing a self-check field while preserving all other wording—but label these separately from the five primary strategies and correct for multiple exploratory comparisons.

Perform a leakage audit using synthetic sentinel answers and instrumentation that records every model-visible string. Include cases with repeated letters, because count summaries can accidentally encode more than the feedback permits if derived from the target rather than observations. Review samples of improved, regressed, invalid, and schema-noncompliant games without changing the frozen evaluation.

## What to Measure/Metrics

Primary metrics are win rate and paired absolute win-rate delta versus baseline. Report confidence intervals, paired discordant counts, and, where appropriate, a paired significance test. Secondary metrics include average accepted guesses among wins, loss-adjusted guesses per game, invalid-guess rate, duplicate-guess rate, parser-failure rate, and model turns. Measure prompt tokens, completion tokens, latency, and cost if applicable.

For structured reasoning, measure schema completion, constraint correctness by field, contradiction rate, final-guess consistency with stated constraints, and correction rate after feedback. Break out performance on repeated-letter answers and on games where model-declared count constraints are wrong. Report variability across deterministic reruns or seeded replicates and include failure counts rather than dropping malformed generations.

## Questions to Answer

1. Which prompt hypotheses are supported by paired win-rate improvements, and how uncertain are those estimates?
2. Do structured prompts improve game reasoning, merely improve output validity, or impose token costs without benefit?
3. Which structured fields best predict whether the next guess will be consistent with prior feedback?
4. How often does a model state correct constraints but choose a guess that violates them?
5. Are improvements stable on repeated-letter answers and across benchmark subsets?
6. What safeguards demonstrate that prompts contain only information derivable from public history?
7. Would the selected prompt remain preferable after considering win rate, guesses, invalid outputs, latency, and token cost together?

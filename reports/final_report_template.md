# Improving Reasoning Efficiency in Small Language Models: Training and Inference-Time Optimization for Wordle

> **Final research report template**  
> This document defines the expected evidence and argument for the final submission. Replace instructional text with project-specific prose; retain section headings so reports are comparable. Do not report a number without its evaluation split, denominator, uncertainty where applicable, and system configuration.

## Report metadata

Record the following on the first page:

- report title and repository URL;
- author and mentor/reviewer;
- submission date;
- repository commit hash used for final evaluation;
- model and tokenizer identifiers with revisions;
- dataset, target-list, allowed-guess-list, and split versions or hashes;
- total local compute (wall-clock, CPU-hours, peak memory) and hardware description;
- final-system configuration ID; and
- a one-sentence disclosure of any external APIs, black-box teachers, or solution materials used.

## Claim-and-evidence checklist

Before submission, verify that every major claim:

1. identifies the compared systems;
2. uses the same frozen target set or explains why it cannot;
3. reports sample size and uncertainty;
4. identifies training and inference compute;
5. names the relevant configuration and code revision;
6. distinguishes exploratory from final test results; and
7. is supported by a table, figure, trace analysis, or statistical test.

---

## Abstract

Write a self-contained summary of approximately 200–300 words. It should state:

- the capability question;
- the small model and strong reference system;
- the frozen evaluation setting;
- the major interventions tested;
- the best held-out result and reference gap;
- the inference-compute comparison;
- the total training/project budget consumed;
- the strongest causal or component-level finding; and
- the most important limitation.

A good abstract reports quantitative results rather than saying that performance “improved significantly.” It must make clear whether the final system met the within-five-percentage-point target and the operational definition of “substantially less inference compute.”

**Guiding questions**

- What exact problem was studied?
- What was the base-model win rate, final-system win rate, and reference win rate?
- What intervention contributed the largest verified gain?
- At what training and inference cost was that gain achieved?
- Which conclusion should a reader remember after one paragraph?

---

## 1. Problem definition

Define the project as a controlled investigation, not merely an implementation task.

### Required content

- Formalize the target vocabulary, allowed guesses, six-turn episode, feedback function, observable state, and agent action.
- State the primary research question and pre-declared final challenge.
- Define “within 5 percentage points” as an absolute win-rate gap.
- Give the operational threshold used for “substantially less inference compute.”
- State the local-only execution requirement and what local resources were measured (wall-clock, CPU-hours, peak RAM, tokens).
- Distinguish Wordle performance from claims about general reasoning.
- Identify what was fixed before optimization and what remained a design choice.

**Guiding questions**

- What makes a system valid for evaluation?
- What information is available to the policy, and how was hidden-target leakage prevented?
- Which decisions were made before seeing test results?
- What outcomes would support or refute the central hypothesis?
- Why is a negative result still informative?

---

## 2. Related work

Organize related work by idea rather than as an annotated list. Connect each source to a design decision or hypothesis in the project.

### Suggested subsections

1. Transformer language models and small-model training
2. Scaling laws and compute-efficient training
3. Supervised fine-tuning and synthetic/teacher-generated data
4. Chain-of-thought and structured reasoning
5. Self-consistency, verifiers, search, and inference-time scaling
6. Reinforcement learning or policy optimization, if used
7. Constraint satisfaction, entropy, and Wordle-solving strategies
8. Efficient inference and profiling

For every cluster, explain what was adopted, what was changed for this setting, and what remains incomparable.

**Guiding questions**

- Which prior method motivated each experimental factor?
- Does prior work optimize accuracy, reward, likelihood, or compute-adjusted capability?
- Which assumptions fail in a deterministic word game?
- Is the solver a baseline, a teacher, a tool, or all three in different experiments?
- What related result would make the current finding unsurprising?

### Citation practice

Use a consistent scholarly format. Cite original papers for research claims, official documentation for library behavior, and exact GitHub commits or release tags for reused code. Include access dates for changing web resources. Do not cite a secondary explainer in place of an available primary source.

---

## 3. Model and environment

### 3.1 Small language model

Document:

- model family, parameter count, architecture summary, context length, tokenizer, and license;
- base versus instruction-tuned status;
- exact model/tokenizer revision;
- numerical precision and quantization;
- device placement and generation implementation;
- reasons the model fits the 0.2B–0.5B scope; and
- any deviations from the original weights before task-specific training.

Explain why this model was chosen over at least two plausible alternatives. Selection criteria should include capability, licensing, vocabulary/tokenization, hardware fit, and expected training cost.

### 3.2 Wordle environment

Describe:

- sources and licenses for target and allowed-guess vocabularies;
- normalization rules;
- exact repeated-letter scoring algorithm;
- turn limit and termination;
- invalid/malformed output policy;
- deterministic seeding and replay;
- environment API and trace schema; and
- unit, property, and regression tests.

Include at least one worked repeated-letter example that demonstrates why naive set-based scoring is wrong.

### 3.3 State and action representations

For each representation used, report:

- exact serialized format;
- whether it is lossless;
- typical and maximum token count;
- how candidate sets or constraints are expressed;
- parsing and repair rules; and
- possible sources of bias or leakage.

### 3.4 System architecture

Provide a diagram showing all components in the final system: environment, prompt/state formatter, model calls, parser, candidate filter, ranker/verifier, search, caches, and evaluator. Label which components are learned, deterministic, frozen, or tuned.

**Guiding questions**

- Can an independent implementation reproduce the feedback exactly?
- Where can hidden information leak into the policy?
- What happens when the model returns commentary, multiple words, or an illegal word?
- Which component owns constraint tracking?
- What behavior is impossible to attribute to the model alone?

---

## 4. Evaluation methodology

### 4.1 Splits and benchmark construction

Report:

- train/validation/test construction;
- target counts and vocabulary hashes;
- whether splits were made before trajectory generation;
- overlap and contamination audits;
- difficulty-slice definitions;
- frozen test access policy; and
- any difference between development and final benchmarks.

A split summary should include:

| Split or slice | Number of targets | Number of states | Repeated-letter rate | Frequency/difficulty definition | Used for |
|---|---:|---:|---:|---|---|
| Training | | | | | |
| Validation | | | | | |
| Frozen test | | | | | |
| Hard/uncommon slice | | | | | |

### 4.2 Metrics

Define the primary win-rate metric mathematically. For every reported system, include:

- solved count, total count, percentage, and 95% confidence interval;
- mean/median guesses for solved games;
- solve-turn distribution;
- invalid and malformed output rates;
- constraint-violation rate;
- latency, model calls, input/output tokens, and cost per game; and
- approximate FLOPs only when the assumptions are documented.

Explain how confidence intervals were calculated and why the method is suitable. For system differences, prefer paired target-level bootstrap intervals or another justified paired method.

### 4.3 Protocol

Document:

- target order and seeds;
- generation parameters;
- retry/repair policy;
- timeout and failure behavior;
- batching and caching;
- hardware and software environment;
- reference-system access protocol; and
- rules for selecting checkpoints, prompts, and hyperparameters.

### 4.4 Fairness and validity

Discuss internal validity, construct validity, and external validity. Identify any mismatch in tools, context, retries, model access, or cost measurement between the small system and reference.

**Guiding questions**

- Are all systems evaluated on identical targets and rules?
- Was any configuration selected using test outcomes?
- How much sampling or seed variance remains?
- Are latency measurements synchronized and warmed up?
- Does the primary metric hide invalid outputs, excessive calls, or weak early-turn behavior?

---

## 5. Baseline results

Evaluate at least:

1. random/simple legal policy;
2. deterministic heuristic or solver;
3. unmodified small language model;
4. prompted small language model; and
5. strong reference system.

### Required table

| System | Win rate (95% CI) | Mean guesses, solved | Invalid rate | Calls/game | Tokens/game | Latency/game | Cost/game |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random/simple | | | | | | | |
| Deterministic heuristic | | | | | | | |
| Small base model | | | | | | | |
| Small prompted model | | | | | | | |
| Strong reference | | | | | | | |

Accompany aggregates with a cumulative solve-by-turn plot and at least one difficulty-sliced figure.

### Analysis requirements

- Quantify the original small-to-reference gap.
- Separate formatting/legality failures from strategic failures.
- Compare the deterministic baseline with the language-model baselines.
- Identify the largest baseline weakness that motivates the next experiment.
- State which baseline result was surprising and why.

**Guiding questions**

- Is the small model failing to understand the task, track state, retrieve words, or rank actions?
- Does a fixed first guess explain a large fraction of variance?
- How strong is a no-LLM solver?
- Is the chosen reference actually a strong and fair comparator?

---

## 6. Prompting experiments

### 6.1 Hypotheses and design

Describe the prompt factors evaluated, such as:

- raw game history versus explicit constraints;
- compact versus verbose state;
- candidate lists;
- direct answer versus structured reasoning;
- information-gain instructions;
- few-shot examples;
- constrained output schema; and
- decoding temperature or sampling method.

State the prompt-selection budget and validation-only selection procedure. Include exact prompts in an appendix or versioned configuration file.

### 6.2 Results

| Prompt ID | State representation | Reasoning instruction | Candidate list | Avg. input tokens | Win rate | Invalid rate | Cost/game |
|---|---|---|---|---:|---:|---:|---:|
| | | | | | | | |

Report uncertainty for selected comparisons and disclose the total number of prompt variants attempted.

### 6.3 Interpretation

Distinguish gains from:

- better formatting;
- fewer illegal actions;
- externalized constraint information;
- additional reasoning tokens;
- changed decoding; and
- genuinely improved action selection.

**Guiding questions**

- Does structured reasoning still help when token and call budgets are matched?
- Which prompt elements are redundant once a deterministic solver is present?
- Do gains persist on uncommon and repeated-letter targets?
- Does the model’s written rationale predict action correctness?

---

## 7. Search and solver experiments

### 7.1 Deterministic candidate filter

Specify the constraint representation, candidate-update algorithm, repeated-letter handling, complexity, and tests. Prove or empirically verify that the true target remains in the candidate set after every valid history.

### 7.2 Ranking and information gain

Define each scoring rule. If using entropy, state the partition over possible feedback patterns and the target prior. Clarify whether exploratory guesses outside the remaining target set are allowed.

### 7.3 Hybrid architectures

Compare relevant variants:

- LLM alone;
- solver alone;
- LLM given solver-derived constraints/candidates;
- LLM proposals filtered by solver;
- solver proposals reranked by LLM;
- model/verifier ensembles; and
- one-step or multi-step lookahead.

| System variant | Learned components | Deterministic components | Search budget | Win rate | Calls/game | Cost/game |
|---|---|---|---:|---:|---:|---:|
| | | | | | | |

### 7.4 Attribution

Use ablations to quantify what the solver contributes. Analyze cases fixed by exact constraints and cases that remain failures after filtering.

**Guiding questions**

- How much weakness was constraint tracking rather than language reasoning?
- Is the LLM adding value beyond a deterministic ranker?
- Does search improve strategic choice or just repair invalid output?
- Which component dominates latency at scale?
- Would a simpler non-neural policy achieve the same result?

---

## 8. Dataset generation

### 8.1 Teacher and generation policy

Describe the solver or teacher that labels actions, including objective, tie-breaking, stochasticity, search depth, priors, and version. Explain why its action is “strong” or “optimal” under that objective without overstating unproven optimality.

### 8.2 Sampling strategy

Document how states were sampled across:

- target words;
- game turns;
- candidate-set sizes;
- repeated-letter patterns;
- common and uncommon targets;
- teacher and off-policy trajectories; and
- naturally occurring versus deliberately difficult states.

### 8.3 Dataset schema and statistics

List every field, type, and semantic meaning. Include a data-flow diagram from target split through trajectory generation, filtering, serialization, and training loader.

| Statistic | Training | Validation | Test/analysis only |
|---|---:|---:|---:|
| Targets | | | |
| Trajectories | | | |
| States/examples | | | |
| Unique actions | | | |
| Repeated-letter states | | | |
| Median candidate-set size | | | |
| Invalid/filtered records | | | |

### 8.4 Quality and leakage audits

Report duplicate rates, target overlap, trajectory overlap, impossible states, label ties, teacher errors, vocabulary issues, and serialization round-trip tests. Explain whether model pretraining contamination is knowable and how claims are limited accordingly.

### 8.5 Data card and licensing

Summarize intended use, out-of-scope use, provenance, licenses, known biases, and privacy considerations. Word lists can carry licensing obligations even when individual words appear trivial.

**Guiding questions**

- Does the dataset represent the states encountered by the learned policy?
- How much label diversity exists for states with multiple equally strong actions?
- Does increasing data add coverage or mostly duplicates?
- Can train-state statistics accidentally encode the hidden target?
- What systematic teacher behavior will the student model inherit?

---

## 9. Supervised fine-tuning experiments

### 9.1 Objective and method

Describe:

- full fine-tuning or parameter-efficient method;
- trainable parameter count;
- input/target formatting and loss masking;
- optimizer, scheduler, learning rate, batch size, accumulation, epochs/steps;
- sequence length, packing, precision, clipping, and regularization;
- checkpoint and early-stopping policy;
- seed strategy; and
- hardware, duration, tokens, and cost.

### 9.2 Pilot selection

Explain the staged experiments used to choose the main run. Report unsuccessful pilot configurations and the evidence used to stop or continue them.

### 9.3 Learning curves and held-out results

Present train/validation loss, task-level validation metrics, and checkpoint selection. Task win rate matters more than loss alone.

| Model/checkpoint | Training examples | Trainable params | Training tokens | Cost | Validation win rate | Test win rate |
|---|---:|---:|---:|---:|---:|---:|
| Base | 0 | 0 | 0 | 0 | | |
| SFT variant(s) | | | | | | |

### 9.4 Data and representation ablations

Include at least one data-size or duration curve and one state/target representation comparison. When possible, vary teacher quality or difficult-state oversampling.

### 9.5 Behavioral interpretation

Analyze whether SFT changes legality, constraint adherence, ranking, calibration, and difficult-state behavior. Compare exact action imitation with downstream game performance.

**Guiding questions**

- Does lower validation loss predict higher win rate?
- Which skills improve before overall win rate moves?
- Is the model memorizing common targets or trajectories?
- Does SFT still help when a deterministic solver enforces legality?
- What is the marginal value of additional examples or training steps?

---

## 10. Inference-time scaling experiments

### 10.1 Methods

Define each method precisely: sample count, temperatures, beam width, candidate pool, verifier, search depth, rollout policy, stopping rule, cache behavior, and maximum token/call budget.

### 10.2 Compute ladder

Evaluate a pre-declared ladder of inference budgets. Include a no-extra-compute point and enough levels to show diminishing returns.

| Method | Budget level | Calls/game | Input tokens/game | Output tokens/game | Latency/game | Cost/game | Win rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| | | | | | | | |

Plot win rate against at least two resource axes, such as cost, latency, calls, or tokens. Mark the strong reference and matched-budget comparisons.

### 10.3 Marginal efficiency

Report absolute gain and gain per additional unit compute between adjacent budget levels. Explain where scaling saturates and why.

### 10.4 Selection effects

If a reranker or verifier chooses among samples, measure proposal recall separately from selection accuracy. A failed final choice can come from either stage.

**Guiding questions**

- Does more sampling improve candidate quality or only valid-output rate?
- Is the verifier better than the generator at ranking?
- At matched cost, should compute be spent on a larger model or more search?
- Which inference method has the best latency-constrained and cost-constrained operating point?
- Are gains robust across difficulty slices or concentrated in easy games?

---

## 11. Reinforcement learning experiments, if attempted

If RL was not attempted, keep this section and give an evidence-based explanation of why the expected value did not justify its budget. State which non-RL experiment received the saved compute.

### 11.1 Formulation

Document state, action, policy, reward, episode termination, discounting, reference policy, and optimization algorithm. Distinguish environment reward from shaped proxy rewards.

### 11.2 Training stability and budget

Report rollouts, updates, batch sizes, KL behavior, entropy, reward curves, collapse indicators, hardware, duration, and cost. Explain safety checks against invalid actions and data leakage.

### 11.3 Reward ablations

Compare sparse solve reward with any turn bonus, information-gain reward, legality reward, or other shaping. Measure whether optimizing the proxy harms actual held-out win rate.

| RL variant | Reward | Rollouts | Training cost | Validation reward | Validation win rate | Test win rate |
|---|---|---:|---:|---:|---:|---:|
| | | | | | | |

**Guiding questions**

- What capability should RL add beyond SFT and search?
- Is the reward dense enough for the available budget?
- Did policy optimization improve held-out games or exploit the reward?
- Could the same gain be obtained by better supervised data?
- Was RL a scientifically justified experiment or a résumé-driven addition?

---

## 12. Ablation studies

Present a cumulative system table and targeted one-factor ablations.

| Variant | Prompt | Solver | SFT | Search/verifier | Extra calls | Win rate | Δ from full | Cost/game |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Full system | | | | | | | | |
| Remove one component per row | | | | | | | | |

### Required interpretation

- Identify necessary, sufficient, redundant, and interacting components.
- Distinguish component removal from compute reduction.
- Repeat key comparisons at matched inference cost.
- Include uncertainty for differences, especially small ones.
- Discuss ablations that changed conclusions or contradicted intuition.

**Guiding questions**

- Does SFT add value when the solver is present?
- Does search add value after SFT?
- Is structured prompting still useful after fine-tuning?
- Are gains additive, overlapping, or synergistic?
- Which component would be removed first in a production simplification?

---

## 13. Compute and performance analysis

### 13.1 Budget ledger

Summarize all project compute, including unsuccessful and exploratory runs.

| Category | Wall-clock time | Peak RAM | CPU-hours | Useful outcome |
|---|---:|---:|---:|---|
| Environment | | | | |
| Baselines | | | | |
| Data generation | | | | |
| SFT pilots | | | | |
| Main SFT | | | | |
| Search/inference | | | | |
| Final evaluation | | | | |
| **Total** | | | | |

State whether the system runs entirely locally on consumer hardware without paid services. Include CPU fallback timing and memory usage. All models must be <1B params runnable in <16GB RAM.

### 13.2 Training efficiency

Report examples, tokens, effective batch, steps, throughput, peak memory, accelerator utilization if measured, duration, and cost. Explain bottlenecks and the effect of precision, quantization, packing, or gradient accumulation.

### 13.3 Inference efficiency

Report model calls, prompt/completion tokens, latency percentiles, throughput, memory, and cost per game. Separate model time from solver and orchestration time.

### 13.4 Capability per unit compute

Provide Pareto plots and identify dominated configurations. Compare:

- best absolute performance;
- best performance under a fixed cost per game;
- best latency-constrained system;
- small system versus strong reference at matched cost; and
- small system versus reference at each system’s best setting.

### 13.5 Counterfactual budgets and deployment

Explain the design under:

- **half the local time budget (e.g., 6 hours vs 12 hours)**;
- one-tenth the inference budget;
- ten times the research budget; and
- deployment at **one million games per day using local machines**.

For production scale, estimate the number of local machines required, daily model calls and tokens, throughput, memory and storage requirements, energy use, cache opportunities, reliability requirements, and the point at which a deterministic method is preferable.

**Guiding questions**

- Which experiments generated the most information per dollar?
- Where was budget spent without changing a decision?
- What is the cost of the final five percentage points of performance?
- Is the final design practical beyond the benchmark?

---

## 14. Generalization

Evaluate whether gains persist beyond common in-distribution games.

### Required slices

- held-out target words;
- uncommon or low-frequency words;
- repeated-letter targets;
- large and small candidate sets;
- late-game confusable candidate clusters;
- rare feedback patterns; and
- valid states unlike common training trajectories.

Where possible, include policy-distribution shift: compare teacher-trajectory states with states induced by the learned policy’s own mistakes.

| Slice | Targets/states | Base | Prompted | SFT | Final | Reference |
|---|---:|---:|---:|---:|---:|---:|
| Standard held-out | | | | | | |
| Uncommon | | | | | | |
| Repeated letters | | | | | | |
| Difficult/confusable | | | | | | |
| Off-policy states | | | | | | |

**Guiding questions**

- Does improvement come from a narrow subset of frequent targets?
- How does performance change with candidate-set size and game turn?
- Can the model recover after an unusual or weak earlier guess?
- Is exact target memorization plausible?
- Which generalization claim is supported, and which remains beyond the benchmark?

---

## 15. Failure analysis

Create a failure taxonomy before reviewing final-system traces, then label a representative or statistically meaningful sample.

### Suggested categories

- malformed or multi-word output;
- out-of-vocabulary guess;
- violation of green/yellow/gray constraints;
- repeated-letter multiplicity error;
- legal but dominated/low-information guess;
- unnecessary repeated information;
- poor exploration/exploitation trade-off;
- endgame confusion among similar candidates;
- search proposal failure;
- verifier/reranker selection failure;
- tool/parser/integration failure;
- latency, timeout, or resource failure; and
- benchmark or annotation anomaly.

| Failure category | Count | Share of failures | Baseline prevalence | Final prevalence | Representative trace IDs |
|---|---:|---:|---:|---:|---|
| | | | | | |

Include several complete traces selected by a declared procedure, not only entertaining examples. For each, show observable state, system proposals/scores, chosen action, feedback, and a concise diagnosis. Never expose hidden targets to the policy; post hoc analysis may show them if clearly separated from model-visible input.

**Guiding questions**

- Which errors were eliminated by each intervention?
- What is now the dominant bottleneck?
- Which failures are model errors, tool errors, or interface errors?
- Does the model’s explanation match the actual cause of failure?
- What experiment would discriminate between two plausible diagnoses?

---

## 16. Conclusions

Answer the central research question directly. This section should synthesize evidence rather than repeat the results section.

State:

- whether the final system met the five-percentage-point target;
- whether it met the declared lower-inference-compute criterion;
- which interventions produced robust gains;
- what the model learned versus what the tool supplied;
- the strongest evidence for generalization;
- the total project cost;
- the most important negative result; and
- the limits of the claims.

Separate **observed findings** from **interpretations**. Use calibrated language: “on the frozen Wordle benchmark” rather than “the model learned reasoning” unless broader evidence exists.

**Guiding questions**

- What did this study establish with high confidence?
- Which claim depends on an assumption or imperfect comparison?
- If only one figure could remain, which one supports the central conclusion?
- What changed in the student’s understanding of small-model capability?

---

## 17. Future work

Prioritize a small number of experiments by expected information value, not novelty alone.

For each proposed direction, state:

- unresolved question;
- proposed intervention or experiment;
- control and evaluation metric;
- expected outcome under competing hypotheses;
- estimated compute/data cost; and
- reason it was not completed in the current project.

Potential directions include stronger data curricula, active state generation, distillation from search, learned value functions, calibrated verifiers, alternative small models, cross-game transfer, formal optimality comparisons, latency-aware policy training, and deployment optimization.

Address two mandatory counterfactuals:

1. **With 10× the compute:** what would be scaled, and what evidence suggests that scaling it is worthwhile?
2. **At one million games per day:** what architecture, batching, caching, model compression, monitoring, and fallback strategy would be required?

**Guiding questions**

- Which next experiment would most likely change the conclusion?
- Which direction merely increases complexity without resolving uncertainty?
- Can a proposed improvement be tested first with a cheap pilot?
- What evidence would justify moving beyond Wordle to a broader task?

---

## 18. Reproducibility statement

Provide exact commands for:

- installing dependencies;
- downloading or verifying word lists and split manifests;
- running tests;
- generating the dataset;
- executing one small SFT smoke run;
- evaluating a named checkpoint/configuration;
- reproducing every headline table and figure; and
- locating raw per-game traces and the compute ledger.

Also report:

- operating system and Python version;
- GPU/accelerator model, count, driver, and relevant library versions;
- known nondeterministic operations;
- random seeds;
- immutable model and dataset revisions;
- environment variables required by name, never secret values; and
- artifacts that cannot be redistributed and how another researcher can substitute them.

Include a clean-environment reproduction result from a second machine or fresh container when feasible.

---

## 19. Ethical, licensing, and scope considerations

Discuss:

- licenses and acceptable-use terms for models, word lists, datasets, code, and APIs;
- whether black-box outputs may be used for training under provider terms;
- handling of credentials and paid services;
- environmental/resource implications of experimentation;
- risk of overstating narrow benchmark performance as general reasoning; and
- disclosure of external assistance and reused code.

No personal or sensitive data should be required for this project.

---

## References

Use one consistent citation style. Every in-text citation must appear here, and every listed reference should be cited in the report. Include persistent identifiers such as DOI, arXiv ID, official documentation URL, repository URL plus commit/tag, and access date where appropriate.

---

## Appendices

### Appendix A — Complete configurations

Include or link immutable configurations for every reported system, including prompts, decoding settings, solver options, model revisions, and budget limits.

### Appendix B — Additional results

Provide full seed-level and slice-level tables, confidence intervals, statistical tests, learning curves, and negative results that are too detailed for the main text.

### Appendix C — Prompt and output schemas

Show exact prompts and parsers. Clearly distinguish text visible to the model from evaluator-only metadata.

### Appendix D — Dataset card and split manifests

Include schema, generation process, quality checks, hashes, licenses, and immutable artifact locations.

### Appendix E — Compute ledger

Provide the complete run-level ledger, including failed and exploratory runs.

### Appendix F — Representative traces

Include the declared sample of wins and failures with trace identifiers. Mark post hoc annotations and hidden targets so they cannot be confused with model-visible context.

### Appendix G — Research log and deviations

Summarize pre-registered hypotheses, decision gates, changes to the protocol, and reasons for deviations. Identify which changes occurred before versus after test access.

---

## Final submission checklist

- [ ] The frozen test set was not used for prompt, checkpoint, or hyperparameter selection.
- [ ] Target and trajectory leakage audits are documented.
- [ ] All headline systems use the same environment rules and targets.
- [ ] Win rates include counts, denominators, and 95% confidence intervals.
- [ ] Key differences use paired analyses where appropriate.
- [ ] Training and inference compute are reported for every major system.
- [ ] System runs entirely locally without paid cloud/API calls, with local resource usage documented.
- [ ] The reference protocol and lower-compute criterion are explicit.
- [ ] Ablations isolate the claimed sources of improvement.
- [ ] Negative and null results that affected decisions are included.
- [ ] Generalization and failure analyses go beyond aggregate win rate.
- [ ] Exact code, configurations, revisions, seeds, and commands are provided.
- [ ] Model, data, code, API, and word-list licenses were checked.
- [ ] The conclusion states limitations and avoids broad unsupported reasoning claims.
- [ ] `solutions/` material used, if any, is disclosed according to mentor policy.

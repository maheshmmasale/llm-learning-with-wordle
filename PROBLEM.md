# Problem Definition

## Formal title

**Improving Reasoning Efficiency in Small Language Models: A Controlled Study of Training, Search, and Inference-Time Scaling on Wordle**

## 1. Context

This project is designed as a self-paced research project for a computer engineering student preparing for machine-learning engineering or research roles at a frontier AI laboratory. The student is expected to have introductory exposure to Python, PyTorch, deep learning, transformer language models, and model training, but no Wordle-specific knowledge is assumed.

The project must demonstrate more than the ability to call a pretrained model or fine-tune on a convenient dataset. The student is expected to show that they can:

- formulate a capability question precisely;
- build a trustworthy, reproducible benchmark;
- establish meaningful baselines before optimizing;
- train or adapt a language model;
- design controlled experiments and ablations;
- combine learned models with deterministic tools and search;
- reason about generalization, leakage, and failure modes;
- quantify training and inference compute;
- make decisions under fixed local hardware and runtime constraints; and
- produce a defensible research artifact.

Wordle is the domain, not the intellectual endpoint. The intended learning loop is:

```text
problem formulation → benchmark → baseline → hypothesis → experiment
→ measurement → failure analysis → iteration → ablation → conclusion
```

## 2. Core research question

The project is **not** framed as “build an LLM that plays Wordle.” The central question is:

> **Can training, structured state representations, deterministic tools, search, and inference-time compute improve the reasoning and decision-making of a 0.2B–0.5B parameter language model on Wordle enough to approach a much stronger reference system?**

A complete answer must identify not only whether performance improved, but **why**. In particular:

- Which gains come from the learned model?
- Which gains come from exact constraint tracking?
- Which gains come from additional inference compute?
- Does supervised training produce behavior that generalizes to held-out targets and difficult states?
- Is the final system efficient relative to the reference, or does it recover quality only by spending comparable compute through repeated calls and search?

## 3. Final challenge

Starting from a publicly available language model with approximately **200M–500M parameters**, build and evaluate a Wordle-playing system that:

1. achieves a held-out win rate **within 5 percentage points** of a documented strong reference system;
2. uses **substantially less inference compute** than that reference under the comparison protocol;
3. runs entirely locally on consumer hardware (CPU or a single consumer GPU) without requiring paid cloud compute or API calls;
4. never exposes the hidden target word to the model or decision policy;
5. uses frozen, leakage-audited train/validation/test splits;
6. reports uncertainty, secondary metrics, resource use, and failure analysis; and
7. is reproducible from committed code, configurations, dependency versions, and documented model/data revisions.

The 5-percentage-point threshold is measured as an absolute difference. If the reference wins 92% of games, the target is at least 87% on the same held-out benchmark. The exact reference, prompt and inference settings, target set, allowed-guess list, inference limit, and compute-accounting method must be frozen after the baseline phase and before final-system optimization.

“Substantially less inference compute” must be operationalized before the final comparison. At minimum, report model calls, input/output tokens, wall-clock time, CPU-hours, and peak memory per game. When architecture details are available, report approximate FLOPs. A defensible default target is **at most one-quarter of the reference system’s measured inference compute per game**, while also presenting matched-compute comparisons. Use measured tokens, calls, latency, memory, and optional GPU-hours; disclose measurement limitations and avoid claiming exact hardware efficiency when the evidence does not support it.

The challenge is intentionally method-agnostic. The student must determine whether the strongest approach is prompting, better data, supervised fine-tuning, a deterministic constraint solver, candidate reranking, a verifier, search, inference-time scaling, optional reinforcement learning, or a justified combination.

Failure to reach the numerical target is not automatically a failed project. A careful, reproducible account of why the target was missed can demonstrate stronger research ability than an unsupported headline result.

## 4. Formal environment

### 4.1 Vocabulary and hidden target

Let:

- \(A\) be the set of allowed five-letter guesses;
- \(T \subseteq A\) be the set of valid target words;
- \(w^* \in T\) be the hidden target;
- \(g_t \in A\) be the guess on turn \(t\), with \(t \in \{1,\ldots,6\}\).

A benchmark episode samples or selects \(w^*\) from a frozen evaluation target set. The agent observes only the public game history. The target must never appear in the prompt, tool output available to the agent, hidden metadata, or any feature derived in a target-specific way.

### 4.2 Feedback

After a guess, the environment returns a five-position feedback vector:

\[
f(g_t,w^*) \in \{\text{green},\text{yellow},\text{gray}\}^5.
\]

- **Green:** the letter is correct at that position.
- **Yellow:** the letter occurs in the target but not at that position, subject to multiplicity.
- **Gray:** no unmatched occurrence of that letter remains in the target.

Repeated letters are scored using official Wordle-style multiplicity: greens are assigned first, then remaining unmatched target letters are consumed by yellows. A correct implementation must not mark both copies of a repeated guessed letter yellow when the target contains only one unmatched copy.

### 4.3 State and action

The observable state before turn \(t\) is:

\[
s_t = ((g_1,f_1),\ldots,(g_{t-1},f_{t-1})), A,
\]

or a lossless structured representation of that history. The agent outputs one next guess. Depending on the declared protocol, malformed or out-of-vocabulary output either consumes a turn or is counted and repaired by a fixed parser. This policy must be established before comparison; silent, system-specific retries are prohibited.

An episode terminates when:

- \(g_t=w^*\), producing a win on turn \(t\); or
- the turn budget is exhausted, producing a loss. The budget defaults to one
  turn per letter (5 turns for 5 letters, 9 for 9) and is overridable per run.

### 4.4 Determinism and reproducibility

For fixed code, vocabulary versions, target order, agent configuration, model revision, generation seed, and hardware-determinism settings, the harness must reproduce the same environment transitions. Stochastic model policies may vary across platforms; all available seeds and generation parameters must still be captured.

The environment, evaluator, and split construction must be tested independently of any model.

## 5. Why Wordle is a useful controlled environment

### 5.1 Compact, observable state

Each game has a short history and a known action space. State can be rendered as raw colored feedback, symbolic constraints, candidate words, or another lossless format. Representation choices can therefore be isolated and compared.

### 5.2 Exact transition and feedback rules

The environment is deterministic. A guess and target produce one correct feedback vector, including well-defined repeated-letter behavior. This makes environment tests and replay straightforward.

### 5.3 Objective outcomes

Every episode ends in a solve turn or failure at the turn budget. The primary metric requires no subjective annotator. Secondary errors—invalid words, malformed output, contradictions, and constraint violations—can also be counted automatically.

### 5.4 Cheap repeated trials

The benchmark can run thousands of episodes, enabling confidence intervals, paired comparisons, difficulty slices, and ablations without the cost of evaluating broad natural-language tasks. Deterministic solvers can generate large synthetic datasets primarily on CPU.

### 5.5 Multiple capability components

Strong play involves exact constraint handling, lexical knowledge, planning, uncertainty reduction, and action selection. These can be assigned to a model, a tool, or a hybrid architecture, making the domain suitable for component-level analysis.

### 5.6 Legible failures

A poor action can often be categorized: illegal word, formatting failure, use of an eliminated letter, repeated information, low information gain, weak endgame discrimination, or inconsistency with feedback. This supports mechanistic error taxonomies rather than score-only reporting.

### 5.7 Known limitations

Wordle is a narrow, synthetic task. Success does not establish broad reasoning ability, real-world planning, factuality, or safe deployment. A deterministic solver may dominate the game without a language model. These are features for controlled study but limits on external claims. The final report must not generalize beyond the evidence.

## 6. Experimental progression

The expected progression is cumulative but not prescriptive:

```text
small base model
    ↓
prompting and structured state
    ↓
external constraint solver / ranking / search
    ↓
solver-generated training data
    ↓
supervised fine-tuning
    ↓
inference-time scaling
    ↓
optional RL or policy optimization
    ↓
best system + ablations
```

The student may change course when evidence supports doing so. Every major experiment should begin with a written hypothesis, success criterion, estimated local runtime and memory use, and stopping rule.

### 6.1 Required baselines

At minimum, benchmark:

1. **Random/simple policy:** a transparent lower bound, such as uniform legal guesses or a fixed opening plus random consistent candidate.
2. **Deterministic heuristic:** candidate filtering with a documented ranking rule.
3. **Unmodified small model:** direct next-guess generation without task-specific training.
4. **Prompted small model:** the strongest validation-selected prompt under a declared prompt search budget.
5. **Strong reference:** a stronger model or established high-performing system used as a black-box comparator under a fixed protocol.

These baselines establish the initial gap:

```text
small base model → prompted model → hybrid/trained systems → strong reference
```

### 6.2 Prompting

Compare several pre-specified representations and instructions, not a single hand-tuned prompt. Potential factors include raw history, explicit green/yellow/gray constraints, remaining candidates, scratch space, information-gain instructions, few-shot examples, and constrained output formatting.

Prompt experiments must report token count, invalid-output handling, and the number of prompt variants tried. Choosing the best prompt on the test set is prohibited.

### 6.3 Model versus external reasoning

Build a deterministic component that can reconstruct the exact set of targets consistent with game history. Compare at least:

- LLM alone;
- deterministic solver alone;
- LLM with exact candidate filtering;
- LLM candidate generation followed by deterministic validation or ranking; and
- search/reranking variants that use additional inference compute.

The key analytical question is whether the model fails because it cannot track constraints, lacks lexical/action knowledge, or ranks legal candidates poorly.

### 6.4 Supervised data generation

Use a documented teacher or solver to generate state-to-action examples. The initial target is at least **100,000 diverse states**, with expansion justified by coverage and learning curves rather than volume alone.

The dataset must include:

- game history or an equivalent state representation;
- valid next-action target(s) and how they were selected;
- source target split and trajectory metadata for auditing;
- repeated-letter and difficult-state coverage;
- teacher/solver version and configuration; and
- a data card describing construction, filters, limitations, and licenses.

Do not randomly split individual states from the same target or trajectory across train and test. Split by hidden target before generating trajectories, or otherwise prove that target and trajectory leakage are prevented.

### 6.5 Supervised fine-tuning

Fine-tune the selected small model on training states. Pilot on subsets before committing to a full run. Preserve configurations and curves, and compare against base and prompted versions using the frozen evaluation protocol.

Required investigations include at least one data-size or training-duration curve, one representation comparison, and checks that gains persist on held-out targets and difficult states. Parameter-efficient fine-tuning is allowed and may be preferable under the budget.

### 6.6 Inference-time scaling

Measure whether more inference computation improves the small model. Candidate methods include:

- multiple samples and self-consistency;
- candidate reranking;
- constrained decoding;
- verifier-guided selection;
- beam or limited-depth search;
- Monte Carlo-style rollout estimates; and
- multiple model calls with fixed roles.

The output must include performance-versus-compute curves, not only the best point. Report diminishing returns and compare against a larger locally runnable model at matched compute.

### 6.7 Optional reinforcement learning

Reinforcement learning is a stretch goal, not a core requirement. It should be attempted only after a strong SFT + solver/search baseline exists and the expected information gain justifies its budget.

A minimal reward may be \(+1\) for solving and \(0\) otherwise. Shaped rewards may incorporate solve turn or information gain, but their consequences must be ablated. Policy optimization must use training targets only; evaluation targets remain frozen and inaccessible.

## 7. Research questions

The final report must answer, with evidence, as many of the following as the implemented scope permits:

### Capability and failure

- Why does the unmodified base model fail?
- How much performance is lost to formatting and invalid actions?
- Does the model apply repeated-letter constraints correctly?
- Does it choose merely valid words or strategically useful actions?

### Representation and prompting

- Which state representation is most reliable and token-efficient?
- Does explicit reasoning improve action quality after controlling for extra tokens and calls?
- Are prompt gains robust across seeds and difficulty slices?

### Tools and search

- How much does exact candidate filtering help?
- Which errors remain after constraint tracking is externalized?
- Does search improve planning, or simply provide more chances to sample a valid word?
- At equal inference compute, is a small model plus search better than a larger direct model?

### Training data and SFT

- What does the student model learn from solver-generated trajectories?
- How do data quantity, diversity, teacher policy, and state representation affect results?
- Does the model generalize to held-out target words and rare constraint patterns?
- Are improvements from action imitation, constraint learning, lexical memorization, or output-format regularity?

### Scaling and compute

- What is the marginal win-rate gain from additional samples, tokens, search depth, or model calls?
- Where do returns diminish?
- What would the best design be under half the budget?
- What bottlenecks would dominate at one million games per day?

### Scientific validity

- Which ablations support the claimed source of improvement?
- How sensitive are conclusions to the target list, first guess, decoding parameters, and random seed?
- What negative or null results changed the project direction?
- Which claims are specific to Wordle, and which may transfer to other constrained decision tasks?

## 8. Data splitting and generalization

A naive 80/10/10 split is acceptable only if it is performed by hidden target before trajectory generation and documented with immutable word-list hashes. A stronger evaluation includes:

- a standard held-out target split;
- an uncommon-word or low-frequency slice;
- a repeated-letter slice;
- states with small but confusable candidate sets;
- states unlike common training trajectories;
- cases where one-step greedy information gain is weak; and
- counterfactual or adversarially generated constraint states that remain valid.

The test set is a scarce resource. Use training data for fitting and validation data for prompts, hyperparameters, checkpoint selection, and system design. Run the complete frozen test evaluation only at pre-declared milestones.

## 9. Evaluation methodology

### 9.1 Primary metric

The primary metric is:

\[
\text{WinRate} = \frac{\#\{\text{targets solved in at most 6 turns}\}}{\#\{\text{evaluated targets}\}}.
\]

Report the raw count, denominator, percentage, and 95% confidence interval. Use paired target-level comparisons when two systems play the same target set.

### 9.2 Secondary metrics

Report, as applicable:

- mean and median guesses among solved games;
- solve distribution for turns 1 through 6 and failures;
- cumulative win rate after each turn;
- invalid-word, malformed-output, and constraint-violation rates;
- performance by difficulty, frequency, repeated-letter status, and candidate-set size;
- first-guess behavior and sensitivity;
- model calls and input/output tokens per game;
- approximate inference FLOPs when defensible;
- end-to-end and model-only latency;
- local runtime per game and estimated throughput; and
- training wall-clock time, CPU-hours, tokens, optional local GPU-hours, and peak memory.

### 9.3 Statistical practice

- Preserve per-target outcomes rather than only aggregates.
- Use fixed target ordering and paired tests or paired bootstrap intervals for system differences.
- Include variability across relevant generation or training seeds.
- Separate exploratory runs from confirmatory final evaluation.
- Do not claim superiority from overlapping noisy estimates without an appropriate paired analysis.

### 9.4 Reference-system fairness

The reference system must receive the same observable game state and must not receive the hidden target. Document its model/version, prompt, tools, decoding settings, retries, rate limits, and measurement method. If the reference uses a deterministic solver or search, disclose that fact and compare against both the full system and any available components.

## 10. Compute constraint — Local Execution

The complete project must run locally on the student's laptop or another consumer machine. Paid cloud accelerators, hosted model APIs, paid inference services, and remote data-generation services are not permitted. Every model used by the student system must contain fewer than **1 billion parameters** and must be runnable with less than **16 GB of system RAM**. A single consumer GPU may be used when available, but every required workflow must also provide a documented CPU fallback.

Maintain an append-only local-compute ledger containing:

- date and experiment ID;
- CPU model, logical/physical core count, and number of cores used;
- GPU model and VRAM, when a local GPU is used;
- wall-clock duration and CPU-hours;
- peak system RAM and peak GPU memory, when applicable;
- training and inference token counts, model calls, and generated examples;
- purpose and associated configuration; and
- whether the run contributed to a reported result.

Before each material run, write:

1. hypothesis;
2. smallest sufficient experiment;
3. estimated wall-clock time and peak memory;
4. success/failure criterion; and
5. stopping rule.

Measure efficiency in elapsed time, CPU-hours, memory, tokens, model calls, and optional local GPU-hours—not dollars. Prefer quantization, parameter-efficient training, small pilot datasets, caching, and early stopping where they preserve the experimental question. Reproducibility on the student's laptop is a hard requirement: document operating system, hardware, thread limits, dependency versions, model revision, quantization format, random seeds, and the exact commands for both the primary path and CPU fallback.

## 11. Required ablations

The exact matrix depends on the final system, but the final submission must isolate major sources of gain. At minimum, include comparisons that remove or vary:

- structured prompting;
- external candidate filtering;
- solver/search ranking;
- supervised fine-tuning;
- training-data size or quality;
- number of generated candidates/model calls; and
- inference search depth or verifier use.

Where possible, compare components both independently and cumulatively. Match inference budgets when attributing gains.

## 12. Required artifacts

A complete submission includes:

1. tested Wordle environment and immutable vocabulary/split manifests;
2. reproducible benchmark harness with per-game traces;
3. baseline results and statistical summaries;
4. prompt configurations and prompt-selection record;
5. deterministic solver/search implementation and tests;
6. generated-dataset code, versioned metadata, leakage audit, and data card;
7. SFT configuration, logs, checkpoint or adapter location, and model/system card;
8. inference-scaling configurations and compute/performance curves;
9. optional RL implementation and ablations, if attempted;
10. experiment registry with commit hashes, seeds, hardware, wall-clock time, CPU/GPU-hours, memory, and outcomes;
11. final system and one-command evaluation instructions;
12. final research report using `reports/final_report_template.md`; and
13. the completed autograde scorecard (`python -m src.evaluation.autograde`).

Large model weights and datasets should be stored through an appropriate artifact or model repository, not committed directly to Git. Include immutable identifiers and access instructions.

## 13. Assessment: the machine is the grader

No human evaluates this project. `python -m src.evaluation.autograde`
scores every milestone out of 100 using fixed seeds and the shipped word
lists. Tiers, points, and rules live in `grading_rubric.md`. Better systems
score higher; the same command grades everyone identically.

## 14. Success criteria

A successful project leaves a reviewer able to answer:

- What was the initial capability gap?
- Which interventions closed it, by how much, and with what local compute and memory use?
- Are the comparisons reproducible and fair?
- Does the system generalize beyond training targets and common trajectories?
- Which behavior belongs to the model versus the deterministic solver or search procedure?
- What failed, and what evidence motivated each change of direction?
- How would the design change under one-tenth, one-half, or ten times the compute?
- What would be required to serve one million games per day?
- Which conclusions are robust, and which remain speculative?

If those answers are supported by code, data, controlled experiments, and transparent limitations, the project has met its broader objective: demonstrating the habits required for serious ML engineering and research.

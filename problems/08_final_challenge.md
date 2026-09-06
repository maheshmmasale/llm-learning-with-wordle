# Problem 08 — Final Challenge: A Local End-to-End Guessing System

## Module context

Integrate everything under fixed budgets with a comparison against targets you write down before running.
A credible negative result with rigorous ablations beats a high score from
leakage or undocumented tuning.

- Hints: `hints/08_final.md`
- Theory: `theory/01_ablations.md`, `theory/06_evaluation_and_statistics.md`
- Reference solution: `solutions/08_final/`
- Report checklist: `reports/final_report_template.md`

## Objective

Design, train, and evaluate a complete hidden-target guessing system that runs **entirely on local consumer hardware**. The submitted workflow must not require cloud compute, hosted inference, or paid APIs. It must integrate data generation, supervised learning, inference-time decision making, and rigorous evaluation within the following resource ceiling:

- fewer than **16 GB of system RAM**;
- no more than **8 CPU cores**;
- models with fewer than **1 billion parameters**;
- an optional single consumer GPU, with a fully documented CPU fallback; and
- less than **5 seconds per game on CPU** for the final inference path.

The quality target is to finish **within five percentage points of a strong reference system’s win rate** while using **at least 4× less inference compute**. Define “strong reference,” “win rate,” and the primary compute unit before the final test evaluation. Compute comparisons must use local, auditable measures such as wall-clock time, CPU-hours, tokens, model calls, forward passes, and search operations—not monetary cost.

This is an end-to-end engineering and research challenge. A valid submission is not a collection of disconnected notebook results. It is a reproducible local system with explicit interfaces, resource controls, tests, ablations, and a final report that allows a reviewer to verify the quality–compute claim on a consumer machine.

## Background

A strong reference may achieve high win rate by enumerating legal actions, applying exact entropy calculations, or running broad lookahead. A resource-efficient student system may instead distill expert behavior into a smaller model, invoke search only on uncertain states, cache deterministic computations, quantize local weights, or combine a learned proposal policy with a narrow symbolic verifier. Success depends on total-system design rather than any single component.

Comparing systems requires a frozen test set, identical game rules, and honest accounting. A reference that receives target information is invalid; a student system that shifts expensive work into unrecorded preprocessing is also invalid. Inference compute must be measured per game and per decision, including model tokens, model calls, candidate scoring, and symbolic search. Development compute must be tracked separately from final inference compute so that an efficient deployed system is not confused with an efficient research process.

A GPU may accelerate development, but it is never a required dependency. The repository must provide a CPU path for data generation, training or parameter-efficient adaptation, inference, and evaluation. If full local CPU training is impractical, reduce model size, quantize, use adapters, reduce the dataset, or use solver-generated policies rather than moving the workload to a remote service.

## Exact Requirements

1. Submit an end-to-end executable pipeline covering dataset preparation, local training or adapter fitting, validation-based model selection, inference, game evaluation, local-compute reporting, and report generation.
2. Enforce the hard local ceiling: fewer than 16 GB RAM, at most 8 CPU cores, and models below 1B parameters. A single consumer GPU is optional, but every required stage must have a documented CPU fallback.
3. Make the final student inference path complete one game in under 5 seconds on CPU using the declared benchmark machine and core limit. Report median and p95 latency across the frozen test suite.
4. Use no paid cloud compute, hosted model inference, paid APIs, or remote labeling services. Downloading public model weights, tokenizers, packages, and static datasets is allowed; execution after setup must be local.
5. Maintain a cumulative local-compute ledger. Record every material run with timestamp, experiment ID, purpose, hardware, cores used, wall-clock duration, CPU-hours, optional GPU-hours, peak RAM, peak VRAM when applicable, tokens, model calls, and whether the run contributed to the final system. Include failed and exploratory runs.
6. Freeze the rules, legal action universe, data partitions, target prior, evaluation protocol, strong reference configuration, hardware protocol, and compute units before the final evaluation.
7. Define a strong reference policy using an exact or high-compute local entropy/search procedure. Demonstrate its strength against simpler baselines on validation data. The reference must obey the game’s information constraints and run locally under the same RAM and core ceiling.
8. Define the primary quality target as a student win rate no more than **5.0 percentage points below** the reference on the frozen test suite. Use the paired difference in win proportions, report uncertainty, and avoid claiming success if the confidence interval is inconclusive.
9. Define “substantially less inference compute” as a primary compute unit declared upfront, with the student system required to use no more than one-quarter of the reference compute. Prefer hardware-independent counts such as model calls, decoded tokens, forward passes, candidate evaluations, or search nodes; also report wall-clock latency. Report neural and symbolic components independently.
10. The student system may use supervised fine-tuning, LoRA, prompting, sampling, reranking, quantization, caching, adaptive compute, or search, but all choices must be selected using training and validation data only.
11. Enforce inference limits programmatically. Every decision must emit a trace containing model calls, tokens, candidate evaluations, entropy computations, expanded nodes, cache activity, latency, memory use, and the reason for stopping.
12. Evaluate the final student and reference systems on identical held-out games with paired seeds and identical stopping rules. Choose a sample size justified by power analysis or confidence-width analysis.
13. Include at least five ablations that isolate major system components. Required categories are: learned adaptation versus no adaptation; search or reranking versus direct decoding; adaptive versus fixed inference allocation; dataset balancing or hard-state coverage; and one architecture- or representation-level choice.
14. Include robustness tests on at least two controlled distribution shifts, such as altered target frequencies, larger candidate sets, noiseless but unusual histories, or held-out puzzle families. These are secondary and must not replace the frozen primary test.
15. Package all configurations, seeds, environment information, model and adapter identifiers, source revision, data checksums, per-game outputs, plotting scripts, and CPU fallback commands. Local model files may be referenced by immutable checksum and a reproducible download procedure if redistribution is restricted.
16. Produce a polished final report in Markdown, HTML, or PDF. It must contain an executive summary, system diagram, methods, local-compute ledger, hardware protocol, experimental protocol, primary results, compute–performance frontier, ablations, error analysis, limitations, and reproducibility instructions.
17. Do not alter the final system after inspecting frozen-test outcomes. If a rerun is required because of infrastructure failure, document the reason and preserve the failed trace.

## Acceptance Criteria

- The complete required workflow runs locally with no paid services or model API calls.
- Every model has fewer than 1B parameters, and the measured peak system memory stays below 16 GB.
- The configured run uses at most 8 CPU cores. Any GPU-accelerated path is optional and has a tested, documented CPU fallback.
- The final student system completes a game in under 5 seconds on CPU on the declared benchmark machine; median and p95 game latency are reported.
- The primary student system is within 5.0 percentage points of the strong reference’s win rate on the frozen paired test, with statistical uncertainty reported and interpreted conservatively.
- The student uses at least 4× less inference compute than the reference under the declared primary compute unit, supported by raw counts and wall-clock measurements.
- All final comparisons use identical games, seeds, rules, hardware limits, and success criteria.
- The five required ablation categories are complete and reveal the marginal contribution of each major component.
- The local-compute ledger reconciles with machine logs within a documented tolerance and includes unsuccessful experiments.
- A clean-environment smoke test reproduces a small CPU-only run, and the full evaluation can be regenerated from saved predictions without rerunning training.
- The final report contains no unsupported performance claims and links every major table or figure to machine-readable source data.

## Expected Experiments

Begin with short local pilots that estimate learning curves, peak memory, and runtime before larger configurations enter the main sweep. Compare a compact prompted baseline, direct SFT or adapter tuning, SFT with candidate reranking, and an adaptive SFT-plus-search system. Run every required comparison first through the CPU smoke-test path.

Sweep at least three inference limits expressed in model calls, decoded tokens, candidate evaluations, or search nodes, and place both student and reference configurations on a compute–win-rate plot. Evaluate uncertainty-triggered search, where easy states use direct decoding and difficult states receive additional proposals or lookahead. Test whether expert-data volume can be reduced through diversity sampling, curriculum design, or hard-example mining. Compare quantized and unquantized local inference when both fit the hardware ceiling, recording quality, latency, and memory effects.

Run required ablations one factor at a time around the final configuration while acknowledging interaction effects. Repeat critical ablations under a fixed hardware-independent compute unit so caching or implementation changes do not distort attribution. Perform paired error analysis on games where the reference wins and the student loses, separating proposal failure, reranking failure, illegal output, search exhaustion, repeated-letter mistakes, and distribution shift.

## What to Measure/Metrics

Report primary win rate, paired win-rate gap to reference, confidence interval, average guesses, unsolved fraction, and performance by difficulty stratum. Measure expert-action agreement, tie-aware agreement, reference-score regret, legal-output rate, and calibration of model confidence or uncertainty.

For every final system, report:

- model parameter count, weight precision, and local storage size;
- input and output tokens;
- model calls and forward passes;
- candidate proposals and unique candidates;
- entropy evaluations, search nodes, and rollouts;
- wall-clock time per decision and per game;
- median and p95 CPU latency;
- CPU-hours for dataset generation, training, ablations, and evaluation;
- optional local GPU-hours;
- peak system RAM and peak GPU memory when applicable;
- CPU/GPU model, operating system, core/thread settings, and relevant library versions; and
- student-to-reference compute ratio under the declared primary unit.

Also report win-rate loss per 2× compute reduction and the location of diminishing returns. Robustness results should include absolute performance, change from IID performance, and paired gap to the reference under each shift. Do not translate local use into monetary estimates; the purpose of the ledger is reproducibility and resource accountability on consumer hardware.

## Questions to Answer

1. What system design choice contributes most to closing the gap with the strong reference?
2. Which stage consumes the most local wall-clock time, CPU-hours, or memory, and is that allocation justified by measured gains?
3. Is the student genuinely compute-efficient, or has work been shifted from inference into labeling, training, preprocessing, or caching?
4. On which state types does the remaining five-point gap concentrate?
5. Does adaptive search spend computation on the states that benefit most from it?
6. Which ablation most weakens win rate, and which supposedly important component can be removed with little effect?
7. How stable is the claim across hardware-independent units, CPU implementations, quantization choices, and confidence-interval methods?
8. What changes are needed to run the system on a slower laptop, with fewer cores, or under a tighter memory ceiling?
9. If the target is missed, is the dominant limitation data coverage, model capacity, action proposal, value estimation, search, or the 5-second CPU latency limit?
10. Can an independent reviewer reproduce the local-compute ledger, metrics, and final figures without undocumented services, remote execution, or manual intervention?

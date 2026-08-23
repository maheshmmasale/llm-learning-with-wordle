# Problem 08 — Final Challenge: A Budgeted End-to-End Guessing System

## Objective

Design, train, and evaluate a complete hidden-target guessing system under a fixed total compute budget of **less than USD 300**. The system must integrate data generation, supervised learning, inference-time decision making, and rigorous evaluation. Its target is to finish **within five percentage points of a strong reference system’s win rate** while using **substantially less inference compute**. You must define “strong reference,” “win rate,” and “substantially less” before the final test evaluation and defend those definitions quantitatively.

This is an end-to-end engineering and research challenge. A valid submission is not a collection of disconnected notebook results. It is a reproducible system with explicit interfaces, budget controls, tests, ablations, and a final report artifact that allows a reviewer to verify the quality–cost claim. The budget includes all compute consumed for the submitted development path, including dataset labeling, pilot training, hyperparameter sweeps, final training, search calibration, and evaluation. Free credits do not make compute free: charge resources at documented public or institutional rates.

## Background

A high-compute reference can achieve strong play by enumerating legal actions, applying exact entropy calculations, running broad lookahead, or using a larger model with many sampled candidates. A resource-efficient system may instead distill expert behavior into a smaller model, invoke search only on uncertain states, cache deterministic computations, or combine a learned proposal policy with a narrow symbolic verifier. Success depends on total-system design rather than any single component.

Comparing systems requires a frozen test set, identical game rules, and honest accounting. A reference that secretly uses target information is invalid; a student system that shifts expensive work into uncounted preprocessing is also invalid. Inference compute must be measured per game and per decision, including model tokens, candidate scoring, and symbolic search. Development compute must be tracked separately from final inference compute so that a cheap deployed system is not confused with a cheap research process.

## Exact Requirements

1. Submit an end-to-end executable pipeline covering dataset preparation, training or adapter fitting, validation-based model selection, inference, game evaluation, budget reporting, and report generation.
2. Maintain a cumulative compute ledger with a hard ceiling of **USD 300.00**. Record every material run with timestamp, purpose, hardware type, duration, quantity, pricing source, calculated cost, and whether it contributed to the final system. Include failed and exploratory runs.
3. Freeze the rules, legal action universe, data partitions, target prior, evaluation protocol, strong reference configuration, and budget conversion rates before the final evaluation.
4. Define a strong reference policy using an exact or high-budget entropy/search procedure. Demonstrate its strength against simpler baselines on validation data. The reference must obey the game’s information constraints.
5. Define the primary quality target as a student win rate no more than **5.0 percentage points below** the reference on the frozen test suite. For example, the relevant quantity is the paired difference in win proportions, not a relative five-percent decrease. Include uncertainty and avoid claiming success if the confidence interval is inconclusive.
6. Define “substantially less inference compute” as a preregistered ratio of the primary compute unit, with a required reduction of at least 4× unless a stricter course-wide definition is provided. Report neural and symbolic compute components independently.
7. The student system may use supervised fine-tuning, LoRA, prompting, sampling, reranking, caching, adaptive compute, or search, but all choices must be selected using training and validation data only.
8. Enforce inference budgets programmatically. Every decision must emit a trace containing model calls, tokens, candidate evaluations, entropy computations, expanded nodes, cache activity, latency, and the reason for stopping.
9. Evaluate the final student and reference on identical held-out games with paired seeds and identical stopping rules. Choose a sample size justified by power analysis or confidence-width analysis.
10. Include at least five ablations that isolate major system components. Required categories are: learned adaptation versus no adaptation; search or reranking versus direct decoding; adaptive versus fixed inference budget; dataset balancing or hard-state coverage; and one architecture- or representation-level choice.
11. Include robustness tests on at least two controlled distribution shifts, such as altered target frequencies, larger candidate sets, noiseless but unusual histories, or held-out puzzle families. These are secondary and must not replace the frozen primary test.
12. Package all configurations, seeds, environment information, model and adapter identifiers, source revision, data checksums, per-game outputs, and plotting scripts. Large weights may be referenced by immutable checksum and storage location if redistribution is restricted.
13. Produce a polished **final report artifact** in Markdown, HTML, or PDF. It must contain an executive summary, system diagram, methods, compute ledger, experimental protocol, primary results, Pareto comparison, ablations, error analysis, limitations, and reproducibility instructions.
14. Do not alter the final system after inspecting frozen-test outcomes. If a rerun is required because of infrastructure failure, document the reason and preserve the failed trace.

## Acceptance Criteria

- The recorded total development and evaluation compute cost is below USD 300.00 using the declared pricing methodology.
- The primary student system is within 5.0 percentage points of the strong reference’s win rate on the frozen paired test, with statistical uncertainty reported and interpreted conservatively.
- The student uses at least 4× less inference compute than the reference under the preregistered primary compute unit, and the reduction is supported by raw operation counts and latency/cost measurements.
- All final comparisons use identical games, seeds, rules, and success criteria.
- The five required ablation categories are complete and reveal the marginal contribution of each major component.
- The compute ledger reconciles with machine logs within a documented tolerance and includes unsuccessful experiments.
- A clean-environment smoke test can reproduce a small run, and the full evaluation can be regenerated from saved predictions without rerunning training.
- The final report artifact contains no unsupported performance claims and links every major table or figure to machine-readable source data.

## Expected Experiments

Begin with low-cost pilots that estimate learning curves and prevent expensive configurations from entering the main sweep. Compare a compact prompted baseline, direct SFT, SFT with candidate reranking, and an adaptive SFT-plus-search system. Sweep at least three inference budgets and place both student and reference configurations on a compute–win-rate plot. Evaluate uncertainty-triggered search, where easy states use direct decoding and difficult states receive additional proposals or lookahead. Test whether expert-data volume can be reduced through diversity sampling, curriculum design, or hard-example mining. Run required ablations one factor at a time around the final configuration, while acknowledging interaction effects. Perform paired error analysis on games where the reference wins and the student loses, separating proposal failure, reranking failure, illegal output, search-budget exhaustion, and distribution shift.

## What to Measure/Metrics

Report primary win rate, paired win-rate gap to reference, confidence interval, average guesses, unsolved fraction, and performance by difficulty stratum. Measure expert-action agreement, tie-aware agreement, reference-score regret, legal-output rate, and calibration of model confidence or uncertainty. Inference compute reporting must include tokens, forward passes, candidate proposals, unique candidates, entropy evaluations, search nodes, rollouts, median and p95 latency, peak memory, estimated energy where available, and dollar cost per game. Report student-to-reference compute ratio and win-rate loss per 2× compute reduction. Development accounting must include dataset generation, training, hyperparameter selection, ablations, and final evaluation. Robustness results should include absolute performance, change from IID performance, and paired gap to the reference under each shift.

## Questions to Answer

1. What system design choice contributes most to closing the gap with the strong reference?
2. Which component consumes the largest share of the USD 300 budget, and was that allocation justified by measured gains?
3. Is the student genuinely computation-efficient, or has expense been shifted from inference into labeling, training, or caching?
4. On which state types does the remaining five-point gap concentrate?
5. Does adaptive search spend computation on the states that benefit most from it?
6. Which ablation most weakens win rate, and which supposedly important component can be removed with little effect?
7. How stable is the claim under alternate compute units, hardware prices, and confidence-interval methods?
8. What evidence would be required to deploy the system under a tighter budget or a larger game universe?
9. If the target is missed, is the dominant limitation data coverage, model capacity, action proposal, value estimation, or search?
10. Can an independent reviewer reproduce the budget, metrics, and final figures without access to undocumented services or manual intervention?

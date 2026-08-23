# Grading Rubric

This rubric evaluates the **quality of the research process and engineering evidence**, not only the final Wordle win rate. Grade each area against the repository, experiment logs, final report, and oral/demo presentation.

## Scoring method

For each area, select the performance band that best matches the evidence and assign a score within that band:

- **Excellent:** 90–100% of the area's weight
- **Good:** 70–89% of the area's weight
- **Needs Work:** 0–69% of the area's weight

Partial scores are encouraged when work falls between descriptions. The weights sum to 100%.

| Area | Weight | Excellent | Good | Needs Work |
|---|---:|---|---|---|
| **ML fundamentals** | **10%** | Explains tokenization, autoregressive modeling, attention, decoding, fine-tuning, and overfitting accurately; connects each concept to observed Wordle behavior and makes technically sound design choices. | Understands the main concepts and uses them appropriately, with only minor gaps or weak connections to results. | Explanations contain material errors, are mostly copied/descriptive, or do not justify modeling choices. |
| **Experimental design** | **15%** | States testable hypotheses; changes one factor at a time where possible; controls randomness and leakage; uses fixed splits, seeds, and compute accounting; reports uncertainty and pre-registers primary comparisons. | Experiments answer useful questions and use reasonable controls, but some confounds, missing seeds, or post-hoc choices remain. | Experiments are ad hoc, incomparable, leakage-prone, or lack clear hypotheses and controls. |
| **Engineering quality** | **15%** | Code is modular, typed or well-documented, tested on critical logic, configurable, reproducible from a clean checkout, and robust to invalid outputs; commands and dependencies are pinned and clear. | Code works and is reasonably organized; most runs are reproducible, though tests, interfaces, error handling, or setup details are incomplete. | Code is fragile or monolithic, relies on manual edits/hidden state, lacks tests, or cannot reproduce reported results. |
| **Baseline and evaluation quality** | **10%** | Implements meaningful random/heuristic, base-model, prompted-model, and strong-reference baselines under a common protocol; validates Wordle feedback (including repeated letters); reports primary, secondary, and compute metrics with confidence intervals. | Includes multiple baselines and a mostly consistent evaluator, but omits some validation, metrics, uncertainty, or fairness checks. | Baselines are missing or weak; evaluation differs across systems, exposes targets, contains rule errors, or reports only cherry-picked examples. |
| **Model improvement** | **15%** | Produces a clear, reproducible improvement over strong baselines; attributes gains to specific data/training choices; monitors validation behavior; documents hyperparameters, costs, and negative results. | Achieves a credible improvement and documents the main training setup, but attribution, tuning discipline, or cost reporting is limited. | Improvement is absent, unsupported, evaluated on seen data, or impossible to distinguish from leakage/search/tool effects. |
| **Search and inference-time reasoning** | **10%** | Cleanly separates model, deterministic constraints, candidate generation, ranking, and search; compares inference strategies across a compute frontier and explains when/why added compute helps. | Implements at least one useful solver/search or reranking method and measures its effect, but decomposition or compute analysis is incomplete. | Search is missing, incorrectly implemented, unfairly compared, or treated as an unexplained performance trick. |
| **Research insight** | **15%** | Draws precise conclusions supported by evidence; distinguishes memorization, reasoning, constraint tracking, and tool use; explains failures and proposes high-value follow-ups that follow from results. | Conclusions are mostly supported and include useful observations, but remain descriptive or overgeneralize in places. | Claims exceed evidence, contradict results, ignore confounds, or reduce the work to a leaderboard score. |
| **Ablations and failure analysis** | **5%** | Runs targeted ablations on data, prompts, solver access, search budget, and/or model components; categorizes failures with representative cases and quantifies category frequency. | Includes some useful ablations or error examples, but coverage or quantification is limited. | Provides no controlled ablations, only anecdotes, or no analysis of why the system fails. |
| **Documentation and presentation** | **5%** | README, experiment records, model/data cards, plots, and final report tell a coherent story; limitations and ethics are explicit; another student can reproduce the key result and demo. | Documentation covers setup, approach, and results but has gaps, stale commands, or weak narrative/visualization. | Documentation is incomplete, misleading, difficult to follow, or does not support reproduction. |

## Required evidence checklist

Before grading, confirm that the submission includes:

- [ ] A frozen held-out test target list and a documented train/validation/test policy.
- [ ] Exact commands or scripts for at least one baseline and the best system.
- [ ] A machine-readable result artifact containing per-game outcomes.
- [ ] Training and inference compute/cost estimates.
- [ ] At least three independent runs for central comparisons, or a written justification when this is infeasible.
- [ ] At least one negative result and one qualitative failure analysis.
- [ ] A final report that distinguishes model-only, model-plus-solver, and model-plus-search performance.

## Overall evaluation questions

The student should be prepared to answer these with direct evidence:

1. Why did the unmodified base model fail, and which failure modes were most common?
2. Is the system actually learning a transferable policy, memorizing trajectories or vocabulary, or outsourcing the task to deterministic code?
3. Why does search help—or fail to help—at particular game states?
4. Why does supervised fine-tuning help, and what did the model learn from generated data?
5. How does performance change on uncommon words, repeated-letter words, and out-of-distribution states?
6. How much does additional inference compute improve performance, and where are the diminishing returns?
7. How much of the improvement comes from training versus prompting, candidate filtering, reranking, or the external solver?
8. What happens when the total training or inference compute budget is halved?
9. Why does the best approach outperform each baseline under the same evaluation protocol?
10. Which conclusion is most strongly supported, and which conclusion remains uncertain?
11. What would you try with 10× the compute, and what evidence makes that experiment worth running?
12. How would the system and evaluation change for deployment at one million games per day?

## Suggested final grade interpretation

| Score | Interpretation |
|---:|---|
| **90–100** | Research-portfolio quality: rigorous, reproducible, insightful, and clearly communicated. |
| **80–89** | Strong project: technically credible with a few gaps in rigor, analysis, or polish. |
| **70–79** | Competent project: core system works, but evidence or research depth is uneven. |
| **60–69** | Partial completion: useful implementation work, but major evaluation or reproducibility weaknesses. |
| **Below 60** | Insufficient evidence that the research question was answered reliably. |

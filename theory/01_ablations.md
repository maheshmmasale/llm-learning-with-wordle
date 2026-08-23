# Ablations: Finding What Actually Works

## What Is an Ablation?

An ablation is a controlled experiment in which one part of a system is removed, replaced, or varied while the rest is kept fixed. Its purpose is not merely to find a higher score. It is to test a causal claim: **did this component cause the improvement?**

Suppose a Wordle system improves from 48% to 72% win rate after you add structured prompts, candidate filtering, and self-consistency. A before-and-after comparison cannot tell you which change mattered. Perhaps filtering produced almost all of the gain and self-consistency only increased runtime. Ablations separate those explanations.

## Main Types

- **Component removal:** Start from the full system and remove one component. Example: disable the external valid-word filter.
- **Replacement:** Swap one design for another. Example: replace a structured constraint table with raw guess/feedback history.
- **Scaling:** Vary a quantity. Example: evaluate 1, 2, 4, and 8 sampled candidate guesses per turn.

A good ablation changes one factor at a time. Use the same model checkpoint, held-out target words, prompt budget, word lists, random seeds, and evaluation code. When comparing systems with different inference procedures, report both equal-compute and natural-compute results. Otherwise, a method may appear better only because it sampled eight times more tokens.

## Required Wordle Ablations

The final project should examine at least these factors:

1. raw history versus structured prompting;
2. no external filtering versus valid-word and constraint filtering;
3. direct model choice versus deterministic solver/search assistance;
4. base model versus supervised fine-tuning (SFT);
5. SFT dataset size, such as 1k, 10k, and 100k states;
6. candidate count per turn;
7. inference depth, such as direct decoding, reranking, and multi-step search.

For example, if the full hybrid system uses a structured prompt, a filtered candidate list, four LLM proposals, and an entropy-based reranker, remove only the reranker first. Feed the same four proposals to a fixed fallback selector. The difference estimates the reranker's contribution more cleanly than comparing the full hybrid against a raw language model.

## Interactions and Non-Additive Gains

Component gains are not always additive. Structured constraints may help only when candidate filtering is enabled. SFT may teach the model to consume a candidate list, so removing that list after training causes a larger drop than it would for the base model. This is an **interaction effect**.

Use a small factorial design when interactions are plausible. For two components A and B, evaluate neither, A only, B only, and A+B. If A adds 5 points, B adds 4, but A+B adds 18, the pair is synergistic. If A+B adds only 6, their benefits overlap.

## Example Table

| System | Win rate | Avg guesses | Invalid % | Time/game | Δ from full |
|---|---:|---:|---:|---:|---:|
| Full system | 78% | 4.2 | 0.1% | 3.8 s | 0 pp |
| − structured prompt | 70% | 4.6 | 1.8% | 3.7 s | −8 pp |
| − candidate filter | 55% | 5.1 | 7.4% | 3.1 s | −23 pp |
| − reranker | 74% | 4.4 | 0.1% | 2.2 s | −4 pp |

“Δ from full” is the ablated result minus the full-system result. Candidate filtering has the largest measured contribution here. The reranker gives only four percentage points but costs 1.6 seconds per game, so its value depends on the latency goal and confidence intervals.

## Negative Results and Pitfalls

A zero or negative gain is useful evidence. It may mean the component is unnecessary, poorly implemented, redundant with another component, underpowered at the current sample size, or helpful only on a difficult slice. Inspect confidence intervals and failure cases before concluding “no effect.”

Common mistakes include changing multiple settings at once, comparing unmatched compute, using different target sets, leaking answers into prompts, tuning on the test set, and reporting only the best seed after post-hoc selection. Freeze evaluation targets and seeds before running the study. Record every configuration, including failures. A rigorous negative result is more valuable than an unexplained high score.

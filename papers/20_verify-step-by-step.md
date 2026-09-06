# Let's Verify Step by Step (Lightman et al., 2023)

## Gist

To judge reasoning, grade the **final answer** (outcome supervision) or
**each step** (process supervision)? OpenAI trained both kinds of reward
models on math and found process supervision wins decisively (78% on MATH)
— and exposed why: outcome-supervised models "regularly use incorrect
reasoning to reach the correct final answer." Right answers, wrong reasons.

## How it works

Labelers grade 800k individual reasoning steps (the released **PRM800K**
dataset), not just solutions. A **process reward model** trains on step
labels; an **outcome reward model** trains on final correctness only. At
test time both are used the same way: sample N candidate solutions
(best-of-N) and let the reward model pick. The PRM picks better — and the
gap widens as N grows, because outcome supervision can't distinguish a sound
proof from a lucky guess once both end at the right number. Follow-up
analysis shows ORM-selected solutions contain measurably more invalid steps.

## Key concepts

- **Outcome supervision (ORM)**: one label per solution — correct or not.
  Cheap, but rewards lucky guesses and hallucinated chains.
- **Process supervision (PRM)**: a label per reasoning step, from the
  800k-label PRM800K dataset the paper released. Expensive, honest.
- **Credit assignment**: which step deserves blame? PRMs localize errors;
  ORMs smear one label over the whole chain.
- **Best-of-N with a verifier**: sample many solutions, let the reward
  model pick — the inference-time pattern behind all reranking.
- **Alignment tax note**: process supervision was *more* interpretable and
  safer while performing better — a rare free lunch, worth remembering.

## Why learn this

"Judge the process, not just the outcome" generalizes far beyond math:
code review, essay grading, eval design, even managing people. The paper
also teaches the deepest testing lesson there is — a passing test suite
(ORM) can hide broken reasoning, so audit the steps (PRM), not just the
green checkmarks.

## Links

- Paper: https://arxiv.org/abs/2305.20050
- Video: [Reward Models Explained: What Actually Trains Reasoning](https://www.youtube.com/watch?v=xrt7NMDuURc)

# Tree of Thoughts (Yao et al., 2023)

## Gist

Chain-of-thought is one line of thinking with no backtracking. Tree of
Thoughts generalizes it to a **search tree**: generate several candidate
"thoughts", have the model *evaluate* them, keep the promising ones (BFS)
or dive deep (DFS), backtrack on dead ends. On Game-of-24 puzzles: 4% (CoT)
→ 74% (ToT). Deliberate search over thoughts beats longer single thoughts.

## How it works

Define the thought granularity (a word, a line, a puzzle move). **Generate**:
sample k candidate next thoughts from the current state. **Evaluate**: score
each as sure/maybe/impossible — by LLM vote or a deterministic checker.
**Search**: BFS keeps the top-b states per level; DFS pursues one line until
the evaluator vetoes, then backtracks. The paper's demos (Game of 24,
crosswords, creative writing) all share one property CoT lacks: intermediate
states are *checkable*, so bad branches die early instead of compounding.
Cost is explicit: states visited × (generate + evaluate) calls.

## Key concepts

- **Thought as state**: a partial solution is a tree node; children extend
  it by one step.
- **Generator**: proposes candidate next thoughts — any LLM policy in this
  role.
- **Evaluator**: scores states ("sure / maybe / impossible") — can be the
  LLM itself voting, or a deterministic checker.
- **BFS vs DFS**: breadth keeps the best b states per level; depth commits
  and backtracks. Different compute/quality tradeoffs to ablate.
- **Deliberate vs greedy**: CoT never revisits a bad step; ToT's whole win
  is noticing and abandoning them.

## Why learn this

ToT is search literacy for the LLM age: generator, evaluator, and search
strategy as separable components you can upgrade independently. That
decomposition — propose deterministically-checkable steps, kill bad branches
early — is the design pattern behind agents, verifiers, and every
"LLM + tools" system you'll build.

## Links

- Paper: https://arxiv.org/abs/2305.10601
- Video: [Chain-of-Thought Is Not Enough — Tree of Thoughts paper walkthrough](https://www.youtube.com/watch?v=nz054BhDIzI)

# Tree of Thoughts (Yao et al., 2023)

## Gist

Chain-of-thought is one line of thinking with no backtracking. Tree of
Thoughts generalizes it to a **search tree**: generate several candidate
"thoughts", have the model *evaluate* them, keep the promising ones (BFS)
or dive deep (DFS), backtrack on dead ends. On Game-of-24 puzzles: 4% (CoT)
→ 74% (ToT). Deliberate search over thoughts beats longer single thoughts.

## Key concepts

- **Thought as state**: a partial solution (a Wordle guess sequence so far)
  is a tree node; children extend it by one step.
- **Generator**: proposes candidate next thoughts — your LLM policy in this
  role.
- **Evaluator**: scores states ("sure / maybe / impossible") — can be the
  LLM itself voting, or a deterministic checker like your solver.
- **BFS vs DFS**: breadth keeps the best b states per level; depth commits
  and backtracks. Different compute/quality tradeoffs to ablate.
- **Deliberate vs greedy**: CoT never revisits a bad step; ToT's whole win
  is noticing and abandoning them.

## Why it matters here

This is the intellectual parent of your hybrid architecture: model proposes,
deterministic code disposes. Your milestone-4 solver already plays evaluator
for single guesses; ToT asks what happens when the search runs multi-turn.

## Links

- Paper: https://arxiv.org/abs/2305.10601
- Video: [Chain-of-Thought Is Not Enough — Tree of Thoughts paper walkthrough](https://www.youtube.com/watch?v=nz054BhDIzI)

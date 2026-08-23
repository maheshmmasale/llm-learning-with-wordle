# Search, Solvers, and Inference-Time Scaling

## Deterministic Candidate Filtering

After each Wordle guess, the colored feedback defines constraints on the hidden word. A deterministic solver can maintain the set of answer words that would produce exactly the observed feedback. The safest implementation does not hand-code a collection of green/yellow/gray rules. Instead, it reuses the official feedback function:

```text
keep candidate c if feedback(guess, c) == observed_feedback
```

This method naturally handles repeated letters. If the guess is `SHEEP`, a gray second `E` does not necessarily mean that no `E` exists; it may establish an upper count. Replaying the same feedback algorithm avoids many subtle bugs.

Filtering gives a belief state: a set of targets still possible. A basic solver can guess from that set. A stronger solver chooses a word that will divide the set efficiently.

## Entropy and Information Gain

For a possible guess, simulate its feedback against every remaining target. This partitions candidates into feedback buckets. If most targets produce the same pattern, the guess reveals little. If targets spread across many balanced buckets, it reveals more.

The entropy of the pattern distribution is:

`H = -Σ p(pattern) log2 p(pattern)`

Higher entropy means more expected information. Another useful objective minimizes expected remaining candidates: `Σ p(pattern) × bucket_size(pattern)`. These objectives are related but not identical. During the final turns, probability of solving immediately may matter more than pure information gain.

A guess need not be a possible answer to be informative. For example, when several candidates differ only in two letters, a “probe” word can test many alternatives at once. Compare hard mode, where guesses must honor known constraints, with unrestricted information-seeking.

## Hybrid LLM–Solver Systems

The deterministic solver is good at legality and exhaustive calculation; the LLM may provide learned priors, semantic frequency judgments, or candidate proposals. Useful hybrids include:

- the solver filters all legal candidates and the LLM ranks a short list;
- the LLM proposes guesses and a verifier rejects inconsistent or invalid ones;
- the solver computes entropy and the LLM chooses among near-tied options;
- the LLM predicts a score that is combined with information gain.

Always define fallback behavior. If every LLM proposal is invalid, select the best deterministic candidate. Track how often the fallback fires, because a high win rate may actually belong to the solver rather than the model.

## Inference-Time Scaling

Inference-time scaling spends more computation on each decision without changing model weights.

**Self-consistency** samples several model outputs and chooses the most frequent valid guess or the candidate with the best verifier score. It can reduce random errors, but correlated samples add little value.

**Beam search** keeps several promising partial output sequences. It is useful when the model must generate structured text, but ordinary token-level beam search does not directly optimize Wordle information gain. A game-level beam instead explores several possible guesses and feedback branches.

**Monte Carlo Tree Search (MCTS)** alternates selection, expansion, simulation, and value backup. In Wordle, a node represents candidate-set state, an action is a guess, and chance branches correspond to possible feedback patterns. Exact exhaustive search may be feasible when the set is small; MCTS is more relevant when action branching is large or the value function uses an LLM.

## Local Search Engineering

Search can become expensive even when the model is small. Evaluating every allowed guess against every remaining target is approximately `O(G × C)` feedback calls per turn. Cache feedback patterns, represent patterns as small integers, vectorize filtering, and restrict the candidate guess pool when needed. Measure solver time separately from LLM time.

Compare direct decoding, multiple proposals, deterministic reranking, and deeper search at matched local time or model-call budgets. Plot win rate against seconds per game. More search is worthwhile only when its gain justifies the latency and complexity. A simple entropy solver may outperform an elaborate LLM tree search; that is an important scientific result, not a failure of the project.

# Problem 4: Deterministic Constraint Solver and Hybrid LLM Agent

## Module context

A model may know useful word statistics while failing at exact bookkeeping.
Separate the two: the solver owns feasibility, the model ranks or selects.
This decomposition also tells you what the model actually contributes.

- Theory: `theory/04_search_and_solver.md`
- Reference solution: `src/solutions/04_solver/`
- Maintained library: `src/search/` (tested by `tests/test_search.py`)

## Objective

Build an exact candidate filter plus three compared agents — LLM alone,
solver alone, solver-filters-then-LLM-ranks — on one fixed benchmark. Find
out whether the model adds anything once feasibility is guaranteed.

## Requirements

1. Filter returns exactly the answers consistent with history, where
   consistency = rescoring each prior guess against the candidate reproduces
   the recorded feedback. Handle repeated letters via count bounds (a black
   copy must not delete a letter that is green/yellow elsewhere).
2. Deterministic ordering; contradictory histories return empty, never a
   fabricated fallback.
3. Solver-only policy with documented ranking and tie-break; LLM-alone uses
   the frozen prompt with no candidate information.
4. Hybrid: solver filters, LLM ranks among presented candidates; fixed
   declared fallback for out-of-set choices; reproducible presentation when
   the set exceeds prompt limits.
5. Log candidate-set size before/after every turn; targets never enter
   model-visible data.
6. Differential-test the filter against brute-force rescoring, emphasizing
   doubled/tripled letters, singleton and empty sets.

## Done when

- Filter matches the rescore oracle on every tested history.
- All three agents run paired on identical answers, budgets, and scoring.
- Answer to: does LLM ranking beat deterministic ranking, and where?

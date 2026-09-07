# Problem 2: Establish a Small-Language-Model Wordle Baseline

## Module context

Without baselines, an apparent improvement may come from an easier test set,
a lucky first guess, answer leakage, or extra inference calls. Build the
comparison ladder — random, heuristic, base model, prompted model, strong
reference — before trying to improve anything.

- Theory: `theory/01_ablations.md`, `theory/06_evaluation_and_statistics.md`
- Reference solution: `src/solutions/02_baseline/`
- Maintained library: `src/evaluation/` (run it now:
  `python -m src.evaluation.benchmark --policy solver --limit 50`)

## Objective

Wire a 0.2–0.5B pretrained model to the environment through one frozen
prompt and a deterministic parser, and measure it on a fixed benchmark next
to a strong reference. Establish an honest floor — no prompt tuning here.

## Requirements

1. Load a named 0.2–0.5B checkpoint; pin model id, revision, dtype, and
   hardware. Reference: `src/models/model.py`.
2. Freeze one baseline prompt (task, B/Y/G rules, `GUESS:` contract) and one
   parser (`src/models/prompting.py`); never repair failures silently —
   invalid outputs count against the model.
3. Never let the target into prompts, logs the model sees, or retry messages.
4. Benchmark on a fixed seeded answer set; record per-turn raw text, parsed
   guess, validity, feedback, and terminal status.
5. Run a strong reference under identical rules, schedule, parser policy,
   and attempt budget.

## Done when

- Two identical runs produce identical transcripts, or backend noise is
  quantified.
- Win rate, avg guesses, and invalid-guess rate reported with denominators;
  failures retained, never dropped.
- A transcript sample audited for target leakage.

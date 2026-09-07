# Problem 06 — Supervised Fine-Tuning with LoRA

## Module context

Test whether a 0.2B–0.5B model can internalize Wordle behavior from
solver-generated data — and distinguish imitation from memorization with
held-out and challenge splits. Start with LoRA; it is cheap and iterable.

- Theory: `theory/05_training_and_sft.md`, `theory/02_local_llms.md`
- Reference solution: `src/solutions/06_finetuning/`
- Maintained library: `src/training/sft.py` (needs `requirements-ml.txt`)

## Objective

Finetune with LoRA on the milestone-5 data under a group-aware 80/10/10
split with a deliberately hard test 10%, and evaluate Base vs Prompted vs
SFT vs SFT+Search on identical examples with separated compute accounting.

## Requirements

1. Training script takes model, data + checksum, template, split manifest,
   seed, LoRA config (rank/alpha/dropout/targets), optimizer settings, and
   output dir; supports dry-run on a tiny subset.
2. Deterministic group-aware 80/10/10; no leakage unit crosses splits; test
   10% built harder by predeclared state-only criteria (never by model
   errors).
3. Exact input/target format; labels absent from prompts; loss masking
   stated and justified (answer-tokens-only vs full response).
4. Invalid/ambiguous outputs recorded as failures; checkpoints picked on
   validation only — test is for final reporting.
5. Save curves, per-example predictions, adapter + base revision, env
   versions, seeds, hardware, and checksums; one command reproduces training,
   one reproduces the four-way eval.

## Done when

- Split counts match 80/10/10; leakage checker reports zero collisions.
- Smoke-train, resume, and eval-from-adapter all work headless.
- Four systems compared on the same test examples; ≥3 seeds or bootstrap
  uncertainty; no test-driven model selection.

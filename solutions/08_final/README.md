# 08 — Final integrated system

`system.py` connects the complete pipeline:

1. Load the base model and the LoRA adapter trained in solution 06.
2. Reconstruct the exact answer posterior from Wordle feedback.
3. Collect model proposals through stochastic sampling, beam search, and optional best-first search from solution 07.
4. Add a symbolic entropy shortlist so malformed model output cannot stall the solver.
5. Rerank every proposal using model likelihood, entropy, and self-consistency votes.
6. Run either a reproducible simulation or an interactive game.

The prompt schema matches solution 05, reducing train/serve skew.

## Simulated game

```bash
python solutions/08_final/system.py \
  --model Qwen/Qwen2.5-0.5B \
  --adapter checkpoints/wordle-lora \
  --answers data/answers.txt --allowed data/allowed.txt \
  --target crane --samples 24 --search-nodes 128
```

## Interactive game

```bash
python solutions/08_final/system.py \
  --model Qwen/Qwen2.5-0.5B \
  --adapter checkpoints/wordle-lora \
  --answers data/answers.txt --allowed data/allowed.txt
```

After each guess, enter five characters: `G` for correct position, `Y` for present elsewhere, and `B` for absent. Diagnostics show the model score, verifier reward, exact entropy, votes, and final combined score for the top candidates.

`--reward-weight` controls how strongly symbolic verification overrides language-model likelihood. `--search-nodes 0` (the default) skips best-first search for lower latency. For benchmark reporting, run a fixed answer list and record solve rate, average turns, wall time, and tokens generated under the same inference budget.

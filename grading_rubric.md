# Grading: one eval, zero humans

```bash
python -m src.evaluation.autograde --model <hf-id-or-path> --games 100000
```

Your finetuned LLM plays N Wordle games through the harness. Grade:

- **Solved vs unsolved (80 pts):** `80 * solved / games`.
- **Solve speed (20 pts):** `20 * min(1, 5 / avg_seconds_per_solve)`.

Nothing else counts — not docs, style, tests, or effort. Same seed,
same schedule, same command for everyone. No `--model`: SKIP.

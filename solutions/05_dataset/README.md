# 05 — Entropy-based dataset generation

`generate.py` creates Wordle state/action trajectories labeled by an exact entropy oracle. It implements duplicate-letter feedback correctly, filters the answer posterior after every observation, scores each legal guess by expected information gain, and writes JSONL suitable for supervised fine-tuning.

## Input

Prepare lowercase word lists with one word per line:

- `answers.txt`: possible hidden answers.
- `allowed.txt` (optional): all legal guesses. Answers are always added to this set.

## Generate

```bash
python solutions/05_dataset/generate.py \
  --answers data/answers.txt \
  --allowed data/allowed.txt \
  --output data/wordle_train.jsonl \
  --episodes 10000 --seed 7
```

Each row includes `state`, oracle `action`, `entropy_bits`, and ready-to-train `prompt` / `completion` fields. The hidden answer is omitted by default to prevent accidental leakage; use `--include-answer` only for debugging.

For large vocabularies the exact oracle is CPU-heavy: its cost is roughly `turns × allowed guesses × remaining answers`. A practical first run uses the answer list as the allowed list. The fixed seed makes target sampling reproducible.

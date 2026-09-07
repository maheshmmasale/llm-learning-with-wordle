# 02 — Small-LM baseline

This baseline loads a causal language model through Hugging Face Transformers,
asks for one Wordle guess at a time, and reports win rate, mean attempts, and
invalid model outputs over a fixed answer list.

```bash
pip install torch transformers accelerate
python baseline.py words.txt --limit 100
```

The default is `HuggingFaceTB/SmolLM-360M-Instruct`. To use Qwen instead:

```bash
python baseline.py words.txt --model Qwen/Qwen2-0.5B-Instruct
```

Use `--guesses allowed.txt` when guesses may come from a larger dictionary.
Generation is greedy (`do_sample=False`) and each answer is evaluated exactly
once, making comparisons reproducible. If the model emits no valid dictionary
word (or repeats one), the evaluator records an invalid output and uses the
first unused allowed guess so the episode can continue.

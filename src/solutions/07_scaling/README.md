# 07 — Inference-time scaling

`inference.py` provides four complementary ways to spend more inference compute:

- **Self-consistency:** sample multiple continuations, normalize their answers, and plurality-vote; likelihood breaks ties.
- **Candidate reranking:** combine mean conditional log-probability with a caller-provided verifier/reward.
- **Beam/diverse-beam decoding:** retain several high-likelihood continuations.
- **Best-first search:** expand a global token-hypothesis priority queue under an explicit node budget.

## CLI examples

```bash
python solutions/07_scaling/inference.py \
  --model Qwen/Qwen2.5-0.5B --adapter checkpoints/wordle-lora \
  --prompt "History: crane:BBYBB. Guess:" \
  --method self-consistency --samples 32 --max-new-tokens 8

python solutions/07_scaling/inference.py \
  --model Qwen/Qwen2.5-0.5B --prompt "Guess:" --method rerank \
  --candidate slate --candidate stale --candidate least
```

## Library use

```python
from inference import ScaledDecoder

decoder = ScaledDecoder.from_pretrained(BASE_MODEL, ADAPTER_DIR)
ranked = decoder.rerank(prompt, candidates, reward_fn=my_verifier, reward_weight=0.5)
```

Use self-consistency when outputs have a stable extractable answer, reranking when a reliable symbolic verifier exists, beam search for a cheap likelihood baseline, and best-first search when an explicit expansion budget matters. The external reward should be on a scale comparable to mean token log-probability, or adjusted with `reward_weight`.

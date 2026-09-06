# Training LMs to Follow Instructions with Human Feedback / InstructGPT (Ouyang et al., 2022)

## Gist

Pretrained models complete text; users want instructions followed. The fix
is three stages: supervised finetuning on human demonstrations, train a
**reward model** on human preference rankings, then optimize the policy
against it with PPO. A 1.3B InstructGPT beat the 175B base GPT-3 in human
preference. Alignment, not size, made assistants useful.

## Key concepts

- **SFT on demonstrations**: step one — imitate human-written ideal answers
  so outputs are in the right format.
- **Reward model (RM)**: trained on ranked pairs (A better than B) to score
  any response. Human taste, compressed into a scalar.
- **PPO against the RM**: step three — reinforcement learning that pushes
  the policy toward high-reward outputs, with a KL penalty stopping it from
  drifting into gibberish the RM accidentally likes.
- **KL penalty**: the leash — stay close to the SFT model while improving.
  Without it, RL exploits reward-model blind spots ("reward hacking").
- **Labeler agreement**: human preferences are noisy; the paper measures
  annotator disagreement honestly instead of hiding it.

## Why it matters here

Your SFT milestone skips RLHF (too costly), but the paper defines what your
finetuned model is missing: it imitates solver moves (step one) without ever
learning human-like preferences. Know which step you skipped and what it costs.

## Links

- Paper: https://arxiv.org/abs/2203.02155
- Video: [Fine-tuning LLMs on Human Feedback, RLHF + DPO — Shaw Talebi](https://www.youtube.com/watch?v=bbVoDXoPrPM)

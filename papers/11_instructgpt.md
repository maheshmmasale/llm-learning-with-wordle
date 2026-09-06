# Training LMs to Follow Instructions with Human Feedback / InstructGPT (Ouyang et al., 2022)

## Gist

Pretrained models complete text; users want instructions followed. The fix
is three stages: supervised finetuning on human demonstrations, train a
**reward model** on human preference rankings, then optimize the policy
against it with PPO. A 1.3B InstructGPT beat the 175B base GPT-3 in human
preference. Alignment, not size, made assistants useful.

## How it works

**Step 1 (SFT):** finetune GPT-3 on human-written ideal responses so outputs
are in the right format. **Step 2 (RM):** show labelers pairs of model
outputs, collect which-is-better rankings, and train a reward model to
predict human preference (pairwise ranking loss). **Step 3 (PPO):** sample
prompts, generate responses, score them with the RM, and RL-update the
policy — with a **KL penalty** per token anchoring it to the SFT model so it
can't drift into high-reward gibberish. Evaluation is human win-rate against
baselines plus targeted probes (toxicity, truthfulness, bias), with labeler
disagreement reported rather than hidden.

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

## Why learn this

InstructGPT is the reference design for turning a raw model into a useful
one — and a catalog of failure modes (reward hacking, sycophancy, noisy
labels) that recur in every alignment effort since. Even if you never run
RLHF, its three-stage anatomy (demonstrate → model preferences → optimize
with a leash) is the template all lighter methods are compressing.

## Links

- Paper: https://arxiv.org/abs/2203.02155
- Video: [Fine-tuning LLMs on Human Feedback, RLHF + DPO — Shaw Talebi](https://www.youtube.com/watch?v=bbVoDXoPrPM)

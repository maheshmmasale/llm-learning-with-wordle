# Training and Supervised Fine-Tuning

## What SFT Learns

Supervised fine-tuning (SFT) trains a pretrained language model to predict desired outputs for supplied inputs. For this project, an input might contain a structured Wordle state and a shortlist of candidates; the target output is a strong next guess. The usual objective is token-level cross-entropy: maximize the probability assigned to the teacher's answer tokens.

Pretraining gives the model language and word knowledge. SFT teaches the task interface: how to read constraints, respect the requested format, and imitate a policy. It does not guarantee that the model has learned a general Wordle algorithm. Evaluation must distinguish generalization from memorization.

## Generating Teacher Data

A deterministic solver can create training pairs cheaply and locally. Sample an answer, play one or more legal histories, compute the surviving candidates, and ask an entropy or expected-size solver for a strong next move. Store the full state, teacher action, and metadata such as turn number, candidate count, and difficulty.

A dataset around 100,000 states provides broad coverage without requiring 100,000 distinct answer words. Each target generates multiple states, and randomized legal prefixes create different constraints. However, more rows are not automatically better. Near-duplicate openings can dominate the dataset. Deduplicate exact states, balance turns and difficulty, and include repeated-letter cases.

A data-size ablation—such as 1k, 10k, and 100k examples—shows whether gains are data-limited. Keep validation and test targets held out before generation so their states do not leak into training.

## Full Fine-Tuning Versus LoRA

Full fine-tuning updates every model parameter and usually requires optimizer states plus gradients for all weights. Even a 0.3B model can exceed comfortable laptop memory during training.

LoRA, or Low-Rank Adaptation, freezes base weights and learns small low-rank matrices inside selected layers. This dramatically reduces trainable parameters and optimizer memory. It is often the practical local choice. Quantized LoRA can reduce base-weight memory further, though kernel support and numerical stability vary by machine.

Compare methods fairly: record trainable parameter count, peak RAM, wall-clock time, examples processed, and validation performance. “Parameter efficient” does not always mean faster if an implementation uses slow dequantization or unsupported operations.

## Local Training Tactics

Use short prompts and short targets. Batch sequences of similar lengths to reduce padding. If a full batch does not fit, use **gradient accumulation**: process several microbatches, accumulate gradients, then perform one optimizer step. The effective batch size is microbatch size × accumulation steps.

Use mixed precision when supported by the local accelerator. On CPU, FP32 or BF16 support may be more stable than FP16; test the actual hardware. Gradient checkpointing trades extra computation for lower activation memory. Freeze most layers or use LoRA, save adapters rather than full checkpoints, and evaluate periodically rather than after every small step.

Begin with a tiny overfit test: train on perhaps 32 examples until the loss drops and outputs match targets. This catches broken labels, token masking, and serialization before a long run. Then train a small real split and inspect learning curves before scaling to the full local dataset.

## Generalization and Memorization

Split by hidden target word, not by individual state, because states from the same target are strongly related. Keep the official held-out benchmark untouched during model selection. Test paraphrased prompt formats, unseen candidate lists, rare letters, repeated letters, and late-game states.

Signs of memorization include excellent training accuracy but weak held-out win rate, copying a familiar answer despite contradictory feedback, or large degradation when candidate order changes. Randomize candidate order during training if order should not carry meaning. Compare against the frozen base model and a deterministic solver.

The goal is not merely a lower training loss. It is a locally trained model that makes valid, useful decisions on unseen games, with documented memory use, runtime, and a reproducible training configuration.

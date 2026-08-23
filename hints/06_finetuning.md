# Hints: Supervised Fine-Tuning

> **Try without hints first.** First prove the data pipeline can overfit a tiny batch; then train a real run. Most early failures are formatting or masking bugs.

## Level 1 — Split to test reasoning, not memorization

A random split of state rows may place nearly identical states—or trajectories for the same target—in training and test. Group splits by target word at minimum. Consider a harder test slice with repeated letters, uncommon answers, unusual constraint patterns, and candidate-set sizes absent from common training states.

Freeze the split manifest and benchmark targets before tuning hyperparameters.

## Level 2 — Treat LoRA rank as a hypothesis

Parameter-efficient tuning can make iteration cheaper, but a larger LoRA rank is not automatically better. Start with a modest rank (for example 8 or 16), specify which modules receive adapters, and record trainable parameter count.

Compare at least one rank or target-module ablation if budget permits. Monitor training and validation loss plus task-level Wordle metrics; token loss alone may not predict legal-action quality.

## Level 3 — Format training exactly like inference

Serialize each state with the same instruction and constraint encoding used during evaluation. The target completion should be easy to parse, for example:

```text
### Instruction
Choose the next legal Wordle guess from the state. Output only one word.

### State
Turns left: 4
CRANE -> 0 1 0 2 0
...

### Response
RAILS
```

Mask prompt tokens from the loss if the objective is completion-only. Confirm the EOS token, padding side, truncation, and label mask using a decoded batch. Ensure truncation never removes the answer.

## Level 4 — Minimal training-loop sketch

```python
model.train()
optimizer.zero_grad(set_to_none=True)

for step, batch in enumerate(loader):
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        out = model(**batch)           # labels contain -100 on prompt/pad tokens
        loss = out.loss / grad_accum
    loss.backward()

    if (step + 1) % grad_accum == 0:
        torch.nn.utils.clip_grad_norm_(trainable_params, 1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)
```

Before a full run:

1. inspect tokenized examples and loss masks,
2. overfit 16–64 examples,
3. decode generations from that tiny set,
4. run a short validation benchmark,
5. only then launch the budgeted experiment.

Save adapter/model checkpoints, tokenizer files, config, dataset hash, package versions, seed, and evaluation command. Never select the final model using the test set.

# Module 3 — Prompting and Structured Reasoning

## Why this module matters

Prompting is the cheapest intervention and an essential control. Before modifying weights, determine how much capability is already present but inaccessible through a weak interface. Wordle also exposes an important distinction: producing plausible language is not the same as tracking exact constraints. This module asks you to design prompt families, not to celebrate a single lucky prompt.

## Learning objectives

By the end of this module, you should be able to:

- Translate Wordle state into concise, unambiguous model context.
- Distinguish zero-shot, few-shot, structured-reasoning, and tool-assisted prompts.
- Inject exact constraints without leaking the hidden answer.
- Request information-gain reasoning and valid machine-readable output.
- Benchmark prompts across fixed targets, seeds, and decoding settings.
- Analyze instruction compliance, constraint errors, and token overhead.

## Prompt families

Start with a minimal prompt: rules, public history, and “return one five-letter guess.” Then add one factor at a time:

- **Canonical state:** greens by position, yellow letters with excluded positions, gray letters, turn number, and prior guesses.
- **Remaining candidates:** provide the count, a truncated list, or the full list when it fits. Treat these as distinct conditions.
- **Structured reasoning:** ask the model to list constraints, propose candidates, compare them, and emit a final answer in a strict field.
- **Information-gain instruction:** ask it to choose a guess that partitions remaining answers well, even if the guess is not itself a likely answer.
- **Few-shot demonstrations:** show legal state-to-guess examples chosen only from training data.
- **Chain-of-thought variants:** compare private scratchpad-style reasoning, concise rationale, and answer-only prompting. Do not assume longer reasoning is better.

Relevant reading:

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [Hugging Face chat templates](https://huggingface.co/docs/transformers/chat_templating)
- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs)

## Experimental design

Create a prompt registry with IDs and immutable templates. Every run must log the rendered prompt, tokenizer length, model revision, generation parameters, parser result, and final action. Use the same benchmark from Module 2. Avoid tuning on test answers: develop on a validation split and run the test set only after selecting prompt variants.

Use a factorial design where practical. For example, cross three state representations with two reasoning styles and two temperatures. This reveals interactions and prevents attributing an improvement to the wrong component. Compare answer quality against token cost and latency; a verbose prompt that gains one point while using ten times more tokens may not be efficient.

## Suggested experiments

1. Minimal history versus canonical derived constraints.
2. Constraints only versus constraints plus candidate list.
3. Answer-only versus “analyze then answer.”
4. Generic strategy instruction versus explicit entropy/information-gain instruction.
5. Zero-shot versus two or four carefully selected demonstrations.
6. Free-form text versus JSON or tagged final-answer output.
7. Greedy decoding versus temperatures such as 0.2, 0.7, and 1.0.
8. Prompt robustness: reorder fields, alter harmless wording, or remove one constraint type.

Report solve rate, invalid words, consistency violations, parsing failures, mean prompt/completion tokens, calls, and latency. Inspect trajectories, not merely aggregate scores.

## Questions to answer

- Which state representation reduces constraint violations most?
- Does explicit reasoning improve the final guess, or only produce plausible explanations?
- When does exposing candidate lists help, and when does it overwhelm the small model?
- Does information-gain language cause better partitions in measurable terms?
- How sensitive are results to wording and decoding seed?
- Is any gain explained by extra information or extra compute rather than prompting quality?

## Deliverables

- A versioned prompt registry with at least six meaningfully different templates.
- A renderer and strict output parser with recovery behavior documented.
- A benchmark matrix comparing prompt, decoding, and state-representation variants.
- Plots of win rate and constraint-error rate versus generated tokens or latency.
- At least ten annotated failure trajectories.
- A short recommendation naming the selected prompt baseline and why it is the fairest input to later training and search experiments.

**Exit criterion:** you can state which prompt components causally appear useful, how stable the gains are, and what those gains cost.
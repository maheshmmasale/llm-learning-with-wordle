# Prompting and State Representation

## The Prompt Is an Interface

A language model does not directly observe a Wordle board. It receives tokens. The representation you choose determines which facts are easy to recover, which mistakes are likely, and how much context must be processed. Prompt engineering is therefore not cosmetic wording; it is interface design between the deterministic game state and a probabilistic model.

The simplest representation is raw history:

```text
Guess: CRANE -> ⬛🟨⬛🟩⬛
Guess: SPLIT -> ⬛⬛🟨⬛⬛
Choose the next guess.
```

This is compact and human-readable, but the model must infer constraints, including repeated-letter rules, every turn. A structured representation performs that computation outside the model:

```text
Fixed: position 4 = N
Present: R not in position 2; L not in position 3
Absent: C, A, E, S, P, I, T
Minimum counts: R=1, L=1, N=1
Candidates: [BLOND, GROWN, ...]
```

The second prompt uses more explicit semantics and reduces reasoning load, but only if the constraint extractor is correct.

## Three Useful State Representations

1. **Raw history:** Keep guesses and feedback exactly as played. It preserves all evidence and is easy to log, but small models may misread symbols or double letters.
2. **Structured constraints:** Encode fixed positions, forbidden positions, absent letters, and lower/upper letter counts. It is reliable and token-efficient once the candidate set is large.
3. **Candidate list:** Supply words already consistent with feedback. This converts constraint solving into ranking. It can be extremely effective, but long candidate lists consume context and may encourage copying or formatting errors.

A hybrid prompt can include compact constraints plus the top 20 candidates selected by a deterministic heuristic.

## Prompt Factors to Test

A prompt has independent factors: instruction wording, state representation, candidate-list size, requested output format, examples, reasoning request, and decoding settings. Change one at a time. For example, compare “Return one valid five-letter lowercase word” with a verbose role-playing instruction while keeping the state identical.

Token efficiency matters locally. Longer prompts increase prompt-processing time and key-value-cache memory. Repeating the entire dictionary is usually worse than filtering candidates in Python and passing a short ranked list. Measure prompt tokens, output tokens, latency, invalid-word rate, and win rate.

## Reasoning Versus Direct Answers

Asking for step-by-step reasoning can help a model check constraints, but it also generates more tokens and may create confident yet inconsistent explanations. For a small model, a rigid checklist can be more reliable than open-ended chain-of-thought:

```text
Check: five letters; valid dictionary word; matches greens; honors yellows; avoids grays.
Output JSON only: {"guess":"_____"}
```

You can also keep reasoning in deterministic code and ask the model only to score or choose among candidates. This reduces inference cost and makes decisions auditable.

## Why Prompting Can Hurt

Small models have limited instruction-following ability and context capacity. Extra examples may distract them. Unicode square symbols may tokenize inefficiently. A huge candidate list may cause position errors. Contradictory natural-language and machine-generated constraints can make the model ignore both. A model trained mostly on prose may also wrap an answer in commentary despite a strict output request.

Use a parser with validation and a defined fallback. If the response is `"I choose CRANE"`, extract carefully or reject it; never send an unchecked string to the game. Track formatting failures separately from strategic failures. If JSON causes more malformed outputs than plain text, simpler formatting is better.

The best prompt is not the one that sounds most intelligent. It is the smallest, clearest representation that produces valid, strategically useful guesses with low local latency. Evaluate it across held-out targets, repeated-letter cases, early-game uncertainty, and late-game near-collisions rather than relying on a few attractive transcripts.

# Hints: Prompting and Structured Reasoning

> **Try without hints first.** Write a hypothesis for each prompt change before testing it. A longer prompt is not automatically a better prompt.

## Level 1 — Ask what information the model needs

The raw history is sufficient in principle, but not necessarily easy for a small model to use. Consider which derived facts could reduce bookkeeping burden:

- fixed letters and positions,
- letters known to exist but forbidden in certain positions,
- excluded letters,
- turns remaining,
- legal or remaining candidates.

Change one information component at a time so you can attribute improvements.

## Level 2 — Encode constraints unambiguously

Choose a consistent representation for green, yellow, and gray evidence. Avoid ambiguous prose such as “A is yellow,” which omits the position where `A` cannot occur.

For example:

```text
GREEN:  _ _ A _ E
YELLOW: R not at positions {1, 4}
GRAY:   T, O, N
TURNS LEFT: 3
```

Repeated-letter evidence complicates gray letters: one gray copy does not always mean that letter is absent if another copy was green or yellow. Prefer deriving the summary from the exact feedback history with tested code.

## Level 3 — Compare answer-only and reasoning prompts

Test structured reasoning as an experimental condition rather than assuming chain-of-thought helps. Possible conditions:

1. answer only,
2. concise constraint checklist,
3. generate several candidates then choose,
4. reason privately/structurally and emit one machine-readable action.

Score only the final parsed guess, but measure extra generated tokens and latency. Long free-form reasoning may increase cost or introduce contradictions. A compact scratchpad with a fixed schema can be more reliable for a small model.

## Level 4 — Example of a strong structured prompt

```text
SYSTEM
You are a Wordle decision policy. Obey all observed constraints.
Do not guess the hidden word directly from unavailable information.

RULES
- The answer is a legal five-letter word.
- Green = correct letter and position.
- Yellow = present, wrong position.
- Gray = no remaining unmatched copy of that letter.
- You have at most six total guesses.

STATE
Turns left: 3
History:
  CRANE -> 0 1 0 2 0
  BUILT -> 0 0 1 0 0
Derived constraints:
  pattern: _ _ _ N _
  required letters: R, I
  forbidden positions: R:{2}, I:{3}
  excluded letters: C, A, E, B, U, L, T

TASK
1. Check the constraints.
2. Consider up to three informative legal candidates.
3. Select one next guess.
4. End with exactly: FINAL: WORD
```

Keep the template versioned. Compare prompts over the same game seeds with confidence intervals. If candidate lists are supplied, label that condition separately from LLM-only prompting because it grants deterministic solver assistance.

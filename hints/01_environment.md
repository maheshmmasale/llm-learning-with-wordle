# Hints: Build the Wordle Environment

> **Try without hints first.** Open one level only after you have written down what is blocking you. Each level reveals more of the design.

## Level 1 — Separate deterministic information

Wordle feedback is not a modeling problem. Given a target and a guess, the result is completely deterministic.

Start by defining the smallest pure function you can test:

```text
feedback(target, guess) -> five position-level labels
```

Keep this function independent from the six-turn game loop. Test it before building an environment class.

## Level 2 — Handle repeated letters correctly

A tempting one-pass implementation—“green if equal, otherwise yellow if the letter occurs anywhere in the target”—is wrong for duplicate letters.

Use two passes:

1. Mark exact-position matches as green and consume those target letters.
2. For each remaining guess letter, mark it yellow only if an unconsumed copy remains; otherwise mark it gray.

Useful edge cases include a target with one copy and a guess with two copies, a target with two copies, and a letter appearing once green plus once elsewhere in the guess.

## Level 3 — Make state explicit

Represent the game state as data rather than reconstructing it from printed prompts. A dataclass can hold:

- hidden target (environment-private),
- prior guesses,
- prior feedback patterns,
- maximum turns,
- terminal status.

Expose only an observation that the policy is allowed to see. Consider immutable tuples for history so evaluation code cannot accidentally mutate past state.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Observation:
    guesses: tuple[str, ...]
    patterns: tuple[tuple[int, ...], ...]
    turns_left: int
```

Choose and document one stable encoding, such as `0=gray`, `1=yellow`, `2=green`.

## Level 4 — Reference implementation sketch

The core evaluator can look like this:

```python
GRAY, YELLOW, GREEN = 0, 1, 2

def score_guess(target: str, guess: str) -> tuple[int, ...]:
    if len(target) != 5 or len(guess) != 5:
        raise ValueError("target and guess must be five letters")

    result = [GRAY] * 5
    remaining = {}

    # Exact matches consume their positions first.
    for i, (t, g) in enumerate(zip(target, guess)):
        if t == g:
            result[i] = GREEN
        else:
            remaining[t] = remaining.get(t, 0) + 1

    # Only unconsumed copies can become yellow.
    for i, g in enumerate(guess):
        if result[i] == GREEN:
            continue
        if remaining.get(g, 0) > 0:
            result[i] = YELLOW
            remaining[g] -= 1

    return tuple(result)
```

Build `reset(target)` and `step(guess)` around this pure function. `step` should validate the guess, append to history, and return `(observation, reward, terminated, info)` or another interface you document clearly. Add unit tests before simulation tests; repeated-letter bugs can corrupt every later experiment while remaining hard to notice.

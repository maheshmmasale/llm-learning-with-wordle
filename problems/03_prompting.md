# Problem 3: Systematic Prompting for Wordle Agents

## Module context

Prompting is the cheapest intervention and an essential control: find out how
much capability is already present before touching weights. Design prompt
families and compare them as ablations — producing plausible language is not
the same as tracking exact constraints.

- Theory: `theory/03_prompting_and_representation.md`
- Reference solution: `src/solutions/03_prompting/`
- Maintained library: `src/models/prompting.py`

## Objective

Design ≥5 conceptually distinct prompt strategies and measure each one's
paired win-rate delta over the frozen baseline — same model, parser,
decoding, benchmark, and budget. The prompt is the only intervention.

## Requirements

1. Name, hypothesize, template, and version each strategy (minimal, rules
   explanation, constraint ledger, staged analysis, few-shot, self-check…).
2. ≥3 strategies request scoreable structured reasoning (positions,
   exclusions, letter counts, consistency check, final guess).
3. Same `GUESS:` extraction rule in every condition; no per-strategy repair.
4. Automated leakage tests over every rendered prompt and retry message,
   including answers that coincidentally appear in examples.
5. Log template version, raw output, parsed guess, and terminal status per
   turn; report paired deltas with uncertainty, plus invalid rates and token
   cost. Pick the winner on all of those, not headline win rate alone.

## Done when

- Baseline + 5 variants run on the identical benchmark; templates frozen
  before final evaluation.
- No leakage found; schema-compliance rates reported for structured prompts.
- Conclusions separate formatting gains from real constraint reasoning.

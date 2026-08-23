# 03 — Prompt strategies

`prompts.py` contains six prompts ordered from a minimal baseline to explicit,
duplicate-aware constraint reasoning:

1. `simple`
2. `explain_feedback`
3. `dictionary_only`
4. `evidence_first`
5. `constraint_check`
6. `structured_reasoning`

```python
from prompts import build_prompt

prompt = build_prompt("constraint_check", [("crane", "BYGBB")], length=5)
```

All strategies accept `(history, length)`. The first five request a bare word;
the final strategy requests a single JSON object, making its stronger output
contract easy to parse in an experiment. Reasoning is requested internally so
the benchmark does not depend on free-form chain-of-thought text.

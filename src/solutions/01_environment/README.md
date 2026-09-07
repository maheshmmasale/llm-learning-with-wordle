# 01 — Deterministic Wordle environment

`wordle.py` implements a dependency-free evaluation environment. Feedback uses
`G` (green), `Y` (yellow), and `B` (gray). It performs a green pass before a
yellow pass, so repeated letters cannot consume the same answer letter twice.

```python
from wordle import WordleEnv

env = WordleEnv(["cigar", "rebut", "sissy"], seed=7)
obs = env.reset(answer="cigar")
result = env.step("rebut")
print(result.feedback, result.terminated)
```

Run the tests from this directory:

```bash
python -m pytest -q
```

Passing an explicit answer to `reset` makes benchmark episodes fully
reproducible; otherwise the environment uses its own seeded RNG.

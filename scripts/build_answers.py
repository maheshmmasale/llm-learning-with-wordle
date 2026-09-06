"""Rebuild data/answers*.txt from word frequency ranks.

Answers are the most frequent English words per length that also appear in
the BSD-dictionary guesses lists, so every answer is a legal guess::

    pip install wordfreq
    python scripts/build_answers.py --per-length 2200

Requires network on first run (wordfreq downloads its data once).
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {5: "answers.txt", 6: "answers6.txt", 7: "answers7.txt",
         8: "answers8.txt", 9: "answers9.txt"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-length", type=int, default=2200)
    parser.add_argument("--top-n", type=int, default=150000)
    args = parser.parse_args()

    import sys

    sys.path.insert(0, str(ROOT))

    from wordfreq import top_n_list

    from src.environment.vocab import load_words
    rank: dict[int, list[str]] = defaultdict(list)
    seen: set[str] = set()
    for word in top_n_list("en", args.top_n):
        word = word.strip().lower()
        if re.fullmatch(r"[a-z]{5,9}", word) and word not in seen:
            seen.add(word)
            rank[len(word)].append(word)

    for length, name in NAMES.items():
        guesses = set(load_words(ROOT / "data" / f"guesses{length}.txt"
                                 if length > 5 else "data/guesses.txt"))
        top = [w for w in rank[length] if w in guesses][: args.per_length]
        path = ROOT / "data" / name
        path.write_text(
            f"# Answer list: {len(top)} words, top frequency-ranked English words\n"
            "# (wordfreq SUBTLEX-based) present in the BSD dictionary guesses list.\n"
            "# Most common first. Regenerate: scripts/build_answers.py\n"
            + "\n".join(top) + "\n",
            encoding="utf-8",
        )
        print(f"{name}: {len(top)}")


if __name__ == "__main__":
    main()

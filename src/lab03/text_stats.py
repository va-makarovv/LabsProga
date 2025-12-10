
"""
echo 'Привет, мир! Привет!!!' | python src/lab03/text_stats.py
"""
from __future__ import annotations

import sys
from typing import List

from src.lab03.text import normalize, tokenize, count_freq, top_n  # type: ignore


def main(argv: List[str]) -> int:
    data = sys.stdin.read()

    norm = normalize(data)
    tokens = tokenize(norm)
    freq = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")

    for w, c in top_n(freq, 5):
        print(f"{w}:{c}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
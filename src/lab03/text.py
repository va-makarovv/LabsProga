# src/lib/text.py
from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Dict, List, Tuple

wordRe = re.compile(r"\b\w+(?:-\w+)*\b", re.UNICODE) # \w и дефисы

spaceRe = re.compile(r"\s+") #сливаем пробелы м в один


def specials2Space(text: str) -> str:
    'заменяем спецсимволы на пробел'
    chars = []
    append = chars.append
    for ch in text:
        cat = unicodedata.category(ch)
        if cat in {"Cc", "Cf"}:
            append(" ")
        else:
            append(ch)
    return "".join(chars)


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")

    text = specials2Space(text)
    text = spaceRe.sub(" ", text).strip()

    if casefold:
        text = text.casefold()

    return text


def tokenize(text: str) -> List[str]:
    return wordRe.findall(text)


def count_freq(tokens: List[str]) -> Dict[str, int]:
    'считаем частоты'
    return dict(Counter(tokens))


def top_n(freq: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    'возвращаем по убыванию частоты или алфавиту'
    # Сортируем: сначала по -count, затем по слову
    items = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return items[:n]

# #normalize
# print(normalize("ПрИвЕт\nМИр\t"))
# print(normalize("ёжик, Ёлка"))
# print(normalize("Hello\r\nWorld"))
# print(normalize("  двойные   пробелы  "))
# print()
#
# #tokenize (normalized)
# print(tokenize(normalize("привет мир")))
# print(tokenize(normalize("hello.txt,world!!!")))
# print(tokenize(normalize("по-настоящему круто")))
# print(tokenize(normalize("2025 год")))
# print(tokenize(normalize("emoji 😀 не слово")))
# print()
#
# #count_freq + top_n
# tokens1 = ["a", "b", "a", "c", "b", "a"]
# freq1 = count_freq(tokens1)
# print(freq1)
# print(top_n(freq1, n=2))
#
# tokens2 = ["bb", "aa", "bb", "aa", "cc"]
# freq2 = count_freq(tokens2)
# print(freq2)
# print(top_n(freq2, n=2))
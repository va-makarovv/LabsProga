# Лабораторная работа 7

## Задание А - test_text.py

```python
import pytest

from src.lib.text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
    ],
)
def test_normalize_basic(source: str, expected: str) -> None:
    assert normalize(source) == expected


def test_normalize_yo2e_flag() -> None:
    """проверка замены ё/Ё на е/Е."""
    text = "ёжик ёлка"
    assert normalize(text) == "ежик елка"
    assert normalize(text, yo2e=True) == "ежик елка"
    assert normalize(text, yo2e=False) == "ёжик ёлка"


@pytest.mark.parametrize(
    "source, expected_tokens",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello.txt,world!!!", ["hello", "txt", "world"]),
        ("по-настоящему круто", ["по-настоящему", "круто"]),
        ("2025 год", ["2025", "год"]),
        ("emoji 😀 не слово", ["emoji", "не", "слово"]),
        ("", []),
    ],
)
def test_tokenize_basic(source: str, expected_tokens: list[str]) -> None:
    """Тест токенизации (после normalize)"""
    tokens = tokenize(normalize(source))
    assert tokens == expected_tokens


def test_count_freq_and_top_n() -> None:
    """count_freq + top_n """
    tokens = ["a", "b", "a", "c", "b", "a"]
    freq = count_freq(tokens)

    # частоты 
    assert freq == {"a": 3, "b": 2, "c": 1}

    # top_n с n=2
    top2 = top_n(freq, n=2)
    assert top2 == [("a", 3), ("b", 2)]

    # пустой словарь - пустой список
    assert top_n({}, n=5) == []


def test_top_n_tie_breaker() -> None:
    """
    сортировка по алфавиту
    """
    tokens = ["bb", "aa", "bb", "aa", "cc"]
    freq = count_freq(tokens)

    
    # сортировка по убыванию частоты, потом по слову
    top2 = top_n(freq, n=2)
    assert top2 == [("aa", 2), ("bb", 2)]

    # если n больше числа уникальных слов то возвращаем все
    top_all = top_n(freq, n=10)
    assert top_all == [("aa", 2), ("bb", 2), ("cc", 1)]
```

## Задание B - test_json_csv

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from src.lab05.json_csv import json_to_csv, csv_to_json


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _read_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def test_json_to_csv_basic(tmp_path: Path) -> None:
    """JSON в CSV."""
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"

    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    json_to_csv(str(src), str(dst))

    assert dst.exists()

    rows = _read_csv(dst)
    assert len(rows) == 2

    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == "30"
    assert rows[1]["name"] == "Bob"
    assert rows[1]["age"] == "25"


def test_json_to_csv_invalid_structure_raises(tmp_path: Path) -> None:
    """JSON - ValueError."""
    # В модуле ожидается list[dict], не объект
    src = tmp_path / "data.json"
    dst = tmp_path / "data.csv"

    src.write_text(json.dumps({"name": "Alice"}, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_json_to_csv_empty_list_raises(tmp_path: Path) -> None:
    """Пустой список в JSON → ValueError."""
    src = tmp_path / "empty.json"
    dst = tmp_path / "out.csv"

    src.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


@pytest.mark.parametrize(
    "src_name, dst_name",
    [
        ("data.txt", "out.csv"),  # неверный формат у input файла
        ("data.json", "out.txt"),  # неверный формат у output файла
    ],
)
def test_json_to_csv_wrong_suffix_raises(
    tmp_path: Path, src_name: str, dst_name: str
) -> None:
    src = tmp_path / src_name
    dst = tmp_path / dst_name

    # проверяем формат
    src.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_basic(tmp_path: Path) -> None:
    """CSV → JSON"""
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"

    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age"])
        writer.writerow(["Alice", "30"])
        writer.writerow(["Bob", "25"])

    csv_to_json(str(src), str(dst))

    assert dst.exists()

    rows = _read_json(dst)
    assert isinstance(rows, list)
    assert rows == [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]


def test_csv_to_json_empty_raises(tmp_path: Path) -> None:
    """Пустой CSV → ValueError"""
    src = tmp_path / "empty.csv"
    dst = tmp_path / "empty.json"

    src.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "src_name, dst_name",
    [
        ("data.txt", "out.json"),  
        ("data.csv", "out.txt"),
    ],
)
def test_csv_to_json_wrong_suffix_raises(
    tmp_path: Path, src_name: str, dst_name: str
) -> None:
    src = tmp_path / src_name
    dst = tmp_path / dst_name

    # неверный формат
    src.write_text("name,age\nAlice,30\n", encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_json_csv_roundtrip(tmp_path: Path) -> None:
    """JSON → CSV → JSON"""
    original = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    json_src = tmp_path / "original.json"
    csv_tmp = tmp_path / "tmp.csv"
    json_back = tmp_path / "back.json"

    json_src.write_text(
        json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    json_to_csv(str(json_src), str(csv_tmp))
    csv_to_json(str(csv_tmp), str(json_back))

    result = _read_json(json_back)

    def _normalize_values(items: list[dict]) -> list[dict[str, str]]:
        return [
            {k: ("" if v is None else str(v)) for k, v in row.items()} for row in items
        ]

    assert _normalize_values(original) == result

```

## Результат работы


![](/images/lab07/tests.png)

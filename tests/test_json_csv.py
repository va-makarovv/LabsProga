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
    """Базовый сценарий: JSON (list[dict]) → CSV."""
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

    # числа становятся строками
    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == "30"
    assert rows[1]["name"] == "Bob"
    assert rows[1]["age"] == "25"


def test_json_to_csv_invalid_structure_raises(tmp_path: Path) -> None:
    """Неподдерживаемая структура JSON → ValueError."""
    # В модуле ожидается list[dict], а не объект
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
        ("data.txt", "out.csv"),   # неверное расширение у исходного файла
        ("data.json", "out.txt"),  # неверное расширение у целевого файла
    ],
)
def test_json_to_csv_wrong_suffix_raises(
    tmp_path: Path, src_name: str, dst_name: str
) -> None:
    src = tmp_path / src_name
    dst = tmp_path / dst_name

    # содержимое не важно, сначала проверяются расширения
    src.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_basic(tmp_path: Path) -> None:
    """Базовый сценарий: CSV → JSON (list[dict])."""
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
    """Пустой CSV → ValueError."""
    src = tmp_path / "empty.csv"
    dst = tmp_path / "empty.json"

    src.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "src_name, dst_name",
    [
        ("data.txt", "out.json"),  # неверное расширение у исходного файла
        ("data.csv", "out.txt"),   # неверное расширение у целевого файла
    ],
)
def test_csv_to_json_wrong_suffix_raises(
    tmp_path: Path, src_name: str, dst_name: str
) -> None:
    src = tmp_path / src_name
    dst = tmp_path / dst_name

    # корректный CSV, но расширения не те
    src.write_text("name,age\nAlice,30\n", encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_json_csv_roundtrip(tmp_path: Path) -> None:
    """
    Сквозной сценарий: JSON → CSV → JSON.

    В json_to_csv / csv_to_json все значения в итоге становятся строками,
    поэтому для сравнения приводим исходный список к тому же формату.
    """
    original = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25, "city": "Paris"},
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
            {k: ("" if v is None else str(v)) for k, v in row.items()}
            for row in items
        ]

    assert _normalize_values(original) == result
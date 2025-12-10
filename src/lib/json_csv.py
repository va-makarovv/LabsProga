from __future__ import annotations

import csv
import json
from pathlib import Path


def _check_suffix(path: Path, expected: str) -> None:

    if path.suffix.lower() != expected:
        raise ValueError("Неверный тип файла")


def _ensure_parent_dir(path: Path) -> None:
    parent = path.parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def json_to_csv(json_path: str, csv_path: str) -> None:

    src = Path(json_path)
    dst = Path(csv_path)

    _check_suffix(src, ".json")
    _check_suffix(dst, ".csv")

    with src.open(encoding="utf-8") as jf:
        try:
            data = json.load(jf)
        except json.JSONDecodeError:
            raise ValueError("Пустой JSON или неподдерживаемая структура")

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    first_keys = list(data[0].keys())
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    extra_keys = sorted(k for k in all_keys if k not in first_keys)
    fieldnames = first_keys + extra_keys

    def _stringify(value):
        if value is None:
            return ""
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    _ensure_parent_dir(dst)
    with dst.open("w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            row = {key: _stringify(item.get(key, "")) for key in fieldnames}
            writer.writerow(row)


def csv_to_json(csv_path: str, json_path: str) -> None:

    src = Path(csv_path)
    dst = Path(json_path)

    _check_suffix(src, ".csv")
    _check_suffix(dst, ".json")

    with src.open(encoding="utf-8") as f:
        sample = f.read(2048)
        if not sample.strip():
            raise ValueError("Пустой CSV или отсутствует заголовок")
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.get_dialect("excel")
        try:
            has_header = csv.Sniffer().has_header(sample)
        except csv.Error:
            has_header = True
        f.seek(0)
        reader = csv.DictReader(f, dialect=dialect)

        if (
            not has_header
            or not reader.fieldnames
            or any(h is None or h == "" for h in reader.fieldnames)
        ):
            raise ValueError("Пустой CSV или отсутствует заголовок")
        rows = []
        for row in reader:

            if row is None:
                continue
            if all((v is None or str(v) == "") for v in row.values()):
                continue
            rows.append({k: ("" if v is None else str(v)) for k, v in row.items()})

    if not rows:
        raise ValueError("Пустой CSV или отсутствует заголовок")

    _ensure_parent_dir(dst)
    with dst.open("w", encoding="utf-8") as jf:
        json.dump(rows, jf, ensure_ascii=False, indent=2)

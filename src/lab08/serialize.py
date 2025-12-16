from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .models import Student


PathLike = Union[str, Path]


def students_to_json(students: list[Student], path: PathLike) -> None:
    """Сохраняет список студентов в JSON-файл."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    data = [s.to_dict() for s in students]
    p.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def students_from_json(path: PathLike) -> list[Student]:
    """Читает JSON-массив и возвращает список Student (с валидацией)."""
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("JSON root must be a list of students")

    students: list[Student] = []
    for i, item in enumerate(raw):
        try:
            students.append(Student.from_dict(item))
        except Exception as e:
            raise ValueError(f"Invalid student at index {i}: {e}") from e

    return students
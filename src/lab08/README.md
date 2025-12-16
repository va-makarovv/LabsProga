# Лабораторная работа 8

## models.py

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass(slots=True)
class Student:
    fio: str
    birthdate: str  # YYYY-MM-DD
    group: str
    gpa: float

    _birthdate_date: date = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # fio/group 
        if not isinstance(self.fio, str) or not self.fio.strip():
            raise ValueError("fio must be a non-empty string")
        if not isinstance(self.group, str) or not self.group.strip():
            raise ValueError("group must be a non-empty string")

        # gpa: 0..5
        try:
            self.gpa = float(self.gpa)
        except (TypeError, ValueError) as e:
            raise ValueError("gpa must be a number") from e
        if not (0.0 <= self.gpa <= 5.0):
            raise ValueError("gpa must be between 0 and 5")

        # birthdate: YYYY-MM-DD
        if not isinstance(self.birthdate, str):
            raise ValueError("birthdate must be a string in YYYY-MM-DD format")
        try:
            self._birthdate_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("birthdate must match format YYYY-MM-DD") from e

        if self._birthdate_date > date.today():
            raise ValueError("birthdate cannot be in the future")

    def age(self) -> int:
        today = date.today()
        b = self._birthdate_date
        years = today.year - b.year
        if (today.month, today.day) < (b.month, b.day):
            years -= 1
        return years

    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Student:
        if not isinstance(d, dict):
            raise ValueError("student item must be a dict")

        missing = [k for k in ("fio", "birthdate", "group", "gpa") if k not in d]
        if missing:
            raise ValueError(f"missing fields: {', '.join(missing)}")

        return cls(
            fio=d["fio"],
            birthdate=d["birthdate"],
            group=d["group"],
            gpa=d["gpa"],
        )

    def __str__(self) -> str:
        return f"{self.fio} | {self.group} | GPA: {self.gpa:.2f} | Age: {self.age()}"
```

## serialize.py

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .models import Student


PathLike = Union[str, Path]


def students_to_json(students: list[Student], path: PathLike) -> None:
    """список в JSON"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    data = [s.to_dict() for s in students]
    p.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def students_from_json(path: PathLike) -> list[Student]:
    """читает JSON и возвращает список"""
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
```

## Результат работы


![](/images/lab08/img.png)

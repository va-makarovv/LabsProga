from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.lab08.models import Student


class StorageFormatError(ValueError):
    """Ошибки формата CSV-хранилища (заголовок/колонки/битые строки)."""


class Group:
    """
    CSV-хранилище студентов (CRUD).

    Формат CSV (обязательный заголовок):
        fio,birthdate,group,gpa
    """

    FIELDS = ("fio", "birthdate", "group", "gpa")

    def __init__(self, storage_path: str | Path):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    # -------------------------
    # internal helpers
    # -------------------------
    def _ensure_storage_exists(self) -> None:
        """Создаёт файл с заголовком при отсутствии. Проверяет заголовок при наличии."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self._write_header_only()
            return

        text = self.path.read_text(encoding="utf-8")
        if not text.strip():
            self._write_header_only()
            return

        first_line = text.splitlines()[0].strip()
        expected = ",".join(self.FIELDS)
        if first_line != expected:
            raise StorageFormatError(
                f"Некорректный заголовок CSV.\n"
                f"Ожидается: {expected}\n"
                f"Фактически: {first_line}"
            )

    def _write_header_only(self) -> None:
        with self.path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.FIELDS))
            writer.writeheader()

    def _read_all_rows(self) -> list[dict[str, str]]:
        """Читает все строки CSV как dict (все значения строками)."""
        self._ensure_storage_exists()

        with self.path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != list(self.FIELDS):
                raise StorageFormatError(
                    f"Некорректные поля в CSV: {reader.fieldnames}. Ожидаются: {list(self.FIELDS)}"
                )

            rows: list[dict[str, str]] = []
            for i, row in enumerate(reader, start=2):  # 1 — заголовок
                if row is None:
                    continue
                if any(k is None for k in row.keys()):
                    raise StorageFormatError(f"Битая строка CSV на линии {i}: {row}")

                normalized = {k: (row.get(k) or "").strip() for k in self.FIELDS}
                rows.append(normalized)

            return rows

    def _write_all_rows(self, rows: list[dict[str, Any]]) -> None:
        """Перезаписывает файл (заголовок + rows)."""
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.FIELDS))
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k, "") for k in self.FIELDS})
        tmp_path.replace(self.path)

    def _student_from_row(self, row: dict[str, str]) -> Student:
        """
        Валидация строки: должна конвертироваться в Student.
        Важно: birthdate у вашего Student — СТРОКА YYYY-MM-DD.
        """
        fio = row["fio"]
        birthdate = row["birthdate"]
        group = row["group"]

        gpa_raw = row["gpa"]
        try:
            gpa: Any = float(gpa_raw.replace(",", ".")) if gpa_raw != "" else gpa_raw
        except Exception:
            gpa = gpa_raw

        return Student(fio=fio, birthdate=birthdate, group=group, gpa=gpa)

    def _row_from_student(self, student: Student) -> dict[str, str]:
        """Student -> dict для CSV + валидация через Student."""
        d = student.to_dict()

        fio = str(d.get("fio", "")).strip()
        birthdate = str(d.get("birthdate", "")).strip()  # строка YYYY-MM-DD
        group = str(d.get("group", "")).strip()
        gpa_val = d.get("gpa", "")

        try:
            gpa_str = str(float(gpa_val))
        except Exception:
            gpa_str = str(gpa_val)

        row = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa_str}

        # финальная валидация: строка должна собраться в Student
        _ = self._student_from_row(row)
        return row

    # -------------------------
    # CRUD
    # -------------------------
    def list(self) -> list[Student]:
        """Вернуть всех студентов списком Student."""
        return [self._student_from_row(r) for r in self._read_all_rows()]

    def add(self, student: Student) -> None:
        """Добавить нового студента в CSV (append)."""
        self._ensure_storage_exists()
        row = self._row_from_student(student)

        with self.path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.FIELDS))
            writer.writerow(row)

    def find(self, substr: str) -> list[Student]:
        """Найти студентов по подстроке в fio (без учёта регистра)."""
        needle = (substr or "").casefold()
        if not needle:
            return []

        result: list[Student] = []
        for r in self._read_all_rows():
            if needle in r["fio"].casefold():
                result.append(self._student_from_row(r))
        return result

    def remove(self, fio: str) -> int:
        """Удалить запись(и) с данным fio. Возвращает количество удалённых."""
        target = (fio or "").strip()
        if not target:
            return 0

        rows = self._read_all_rows()
        kept = [r for r in rows if r["fio"] != target]
        removed = len(rows) - len(kept)

        if removed:
            self._write_all_rows(kept)

        return removed

    def update(self, fio: str, **fields: Any) -> int:
        """
        Обновить поля существующего студента(ов) по fio.
        Разрешённые поля: fio, birthdate, group, gpa.
        Возвращает количество обновлённых записей.
        """
        target = (fio or "").strip()
        if not target:
            return 0

        allowed = set(self.FIELDS)
        bad = set(fields.keys()) - allowed
        if bad:
            raise ValueError(
                f"Недопустимые поля для update: {sorted(bad)}. Разрешены: {list(self.FIELDS)}"
            )

        rows = self._read_all_rows()
        updated = 0

        for r in rows:
            if r["fio"] != target:
                continue

            for k, v in fields.items():
                if k == "gpa":
                    r[k] = "" if v is None else str(float(v))
                else:
                    r[k] = "" if v is None else str(v).strip()

            # валидация после изменения
            _ = self._student_from_row(r)
            updated += 1

        if updated:
            self._write_all_rows(rows)

        return updated

    # -------------------------
    # ★ (опционально) статистика
    # -------------------------
    def stats(self) -> dict[str, Any]:
        """
        Возвращает статистику как в README:
        count, min_gpa, max_gpa, avg_gpa, groups, top_5_students
        """
        students = self.list()

        gpas: list[float] = []
        groups_count: dict[str, int] = {}

        for s in students:
            groups_count[s.group] = groups_count.get(s.group, 0) + 1
            try:
                gpas.append(float(s.gpa))
            except Exception:
                pass

        top = sorted(
            [{"fio": s.fio, "gpa": float(s.gpa)} for s in students if _can_float(s.gpa)],
            key=lambda x: x["gpa"],
            reverse=True,
        )[:5]

        return {
            "count": len(students),
            "min_gpa": min(gpas) if gpas else None,
            "max_gpa": max(gpas) if gpas else None,
            "avg_gpa": (sum(gpas) / len(gpas)) if gpas else None,
            "groups": groups_count,
            "top_5_students": top,
        }


def _can_float(x: Any) -> bool:
    try:
        float(x)
        return True
    except Exception:
        return False
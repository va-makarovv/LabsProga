from __future__ import annotations

import json
from pathlib import Path

from src.lab08.models import Student
from src.lab09 import Group


def fmt_student(s: Student) -> str:
    # Печатаем похоже на скриншоты: Student: ..., Group: ..., GPA: ..., Age: ...
    fio = getattr(s, "fio", "")
    group = getattr(s, "group", "")
    gpa = getattr(s, "gpa", "")
    age = getattr(s, "age", None)  # если в вашей модели есть property age

    base = f"Student: {fio}, Group: {group}, GPA: {gpa}"
    return base + (f", Age: {age}" if age is not None else "")


def print_list(title: str, students: list[Student]) -> None:
    print(title)
    for i, s in enumerate(students, start=1):
        print(f"   {i}. {fmt_student(s)}")
    print()


def export_to_json(students: list[Student], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = [s.to_dict() for s in students]

    # Чтобы было как на скриншоте (unicode-escape), оставляем ensure_ascii=True
    out_path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    storage = Path("data/lab09/students_mock.csv")
    group = Group(storage)

    print("=== Демонстрация CRUD-операций с группой студентов ===\n")

    # 1) READ
    students = group.list()
    print_list("1. Просмотр всех студентов (READ):", students)

    # 2) CREATE
    print("2. Добавление нового студента (CREATE):")
    new_student = Student(
        "Беляев Тимофей Романович",
        "2003-09-09",
        "БИВТ-21-1",
        4.7,
    )
    group.add(new_student)
    print(f"   Добавлен: {fmt_student(new_student)}\n")

    # 3) READ after create
    students = group.list()
    print_list("3. Список студентов после добавления:", students)

    # 4) SEARCH (READ)
    print("4. Поиск студентов по подстроке 'Дарья' (READ):")
    found = group.find("Дарья")
    for i, s in enumerate(found, start=1):
        print(f"   {i}. {fmt_student(s)}")
    print()

    # 5) UPDATE
    print("5. Обновление информации о студенте (UPDATE):")
    updated = group.update("Зайцев Кирилл Андреевич", gpa=4.3)
    if updated:
        print("   Успешно обновлены данные Зайцева К.А.\n")
    else:
        print("   Не найден студент для обновления.\n")

    # 6) READ after update
    students = group.list()
    print_list("6. Список студентов после обновления:", students)

    # 7) DELETE
    print("7. Удаление студента (DELETE):")
    removed = group.remove("Громов Никита Павлович")
    print(f"   Удалено {removed} студент(ов)\n")

    # 8) FINAL READ
    students = group.list()
    print_list("8. Финальный список студентов:", students)

    # 9) STATS
    print("=== Statistics ===")
    st = group.stats()
    print(f"Всего студентов: {st['count']}")
    print(f"Минимальный GPA: {st['min_gpa']}")
    print(f"Максимальный GPA: {st['max_gpa']}")
    print(f"Средний GPA: {st['avg_gpa']}")
    print("Студентов по группам:")
    for k, v in st["groups"].items():
        print(f"  {k}: {v}")
    print()

    # 10) EXPORT JSON
    out_json = Path("data/lab09/students_export.json")
    export_to_json(students, out_json)
    print("10. Экспорт данных в JSON:")
    print(f"   Данные экспортированы в {out_json.as_posix()}\n")


if __name__ == "__main__":
    main()
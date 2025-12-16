from __future__ import annotations

from pathlib import Path

from pathlib import Path

from src.lab08.models import Student
from src.lab08.serialize import students_from_json, students_to_json

def main() -> None:
    print("=== Testing Examples for lab08 ===")

    # 1) Student - dict - Student
    print("\n--- Test: model serialize/restore ---")
    s = Student(
        fio="Belova Marina Sergeevna",
        birthdate="2000-12-09",
        group="SE-13",
        gpa=4.25,
    )
    print("Student:", s)
    d = s.to_dict()
    print("Serialized:", d)
    s2 = Student.from_dict(d)
    print("Restored:", s2)

    # 2) запись JSON
    print("\n--- Test: students_to_json ---")
    out_file = Path("data/lab08/test_examples_output.json")
    students_to_json([s, s2], out_file)
    print(f"Output file created: {out_file}")
    print(out_file.read_text(encoding="utf-8"))

    # 3) чтение JSON
    print("\n--- Test: students_from_json ---")
    in_file = Path("data/lab08/students_input.json")
    students = students_from_json(in_file)
    print(f"Loaded {len(students)} students from {in_file}")
    for st in students:
        print(" ", st)

    # 4) прочитать -> добавить -> сохранить
    print("\n--- Test: combined ---")
    combined = students + [
        Student(
            fio="Sokolov Ilya Vladimirovich",
            birthdate="2002-03-21",
            group="SE-14",
            gpa=4.95,
        )
    ]
    combined_out = Path("data/lab08/combined_output.json")
    students_to_json(combined, combined_out)
    print(f"Saved {len(combined)} students to {combined_out}")

    print("\n=== All examples completed ===")


if __name__ == "__main__":
    main()
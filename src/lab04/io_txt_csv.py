from __future__ import annotations
import csv
from pathlib import Path
from tabnanny import check
from typing import Iterable, Sequence


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    p = Path(path)
    return p.read_text(encoding=encoding)


def write_csv(
    rows: Iterable[Sequence],
    path: str | Path,
    header: tuple[str, ...] | None = None,
) -> None:

    rows = list(rows)

    if rows:
        expected_len = len(rows[0])
        for i, r in enumerate(rows):
            if len(r) != expected_len:
                raise ValueError(
                    f"длина rows[{i}] = {len(r)}," f"expected {expected_len}."
                )
        if header is not None and len(header) != expected_len:
            raise ValueError(
                f"Длина header ({len(header)}) должна совпадать с длиной строк ({expected_len})."
            )

    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)


txt = read_text("../../data/input1.txt")
print(f"прочитано {len(txt)} символов")

checkpath = "check.csv"
write_csv([("word", "count"), ("test", 3)], checkpath)
print(f"записано {checkpath}")

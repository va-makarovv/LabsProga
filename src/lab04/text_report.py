from __future__ import annotations

import sys
import argparse
from pathlib import Path

# python3 src/lab04/text_report.py --in data/input.txt --encoding cp1251

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # корень
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.lab04.io_txt_csv import read_text, write_csv
from src.lab03 import normalize, tokenize, count_freq, top_n



HEADER = ("word", "count")

def newPath(p: str | Path) -> Path:
    "подправляем работу с путём"
    p = Path(p)
    return p if p.is_absolute() else (BASE_DIR / p)

def betterParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", default="data/input1.txt")
    parser.add_argument("--out", dest="out_path", default="data/report.csv")
    parser.add_argument("--encoding", dest="encoding", default="utf-8")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = betterParser().parse_args(argv)

    in_path  = newPath(args.in_path)
    out_path = newPath(args.out_path)

    try:
        text = read_text(in_path, encoding=args.encoding)
    except FileNotFoundError:
        print(f"файл не найден: {in_path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("Ошибка декода. Укажите кодировку, examp: --encoding cp1251", file=sys.stderr)
        return 1

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    rows = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))

    try:
        write_csv(rows, out_path, header=HEADER)
    except FileNotFoundError:
        print(f"Не найдена папка для записи: {out_path.parent}\n",file=sys.stderr)
        return 1

    # 5) Краткое резюме в консоль
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")
    for w, c in top_n(freq, 5):
        print(f"{w}:{c}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
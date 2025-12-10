"""

python -m src.lab06.cli_text stats --input data/samples/text.txt
python -m src.lab06.cli_text stats --input data/samples/text.txt --top 10
python -m src.lab06.cli_text cat --input data/samples/text.txt
python -m src.lab06.cli_text cat --input data/samples/text.txt -n
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from src.lab03 import normalize, tokenize, count_freq, top_n


def cmd_stats(args: argparse.Namespace) -> int:

    input_path = Path(args.input)

    try:
        raw = input_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Ошибка: файл '{input_path}' не найден")
    except OSError as exc:
        raise SystemExit(f"Ошибка при чтении файла '{input_path}': {exc}")

    norm = normalize(raw)
    tokens: List[str] = tokenize(norm)
    freq = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")

    top_n_value = args.top
    print(f"Топ-{top_n_value}:")

    for word, count in top_n(freq, n=top_n_value):
        print(f"{word}:{count}")

    return 0


def cmd_cat(args: argparse.Namespace) -> int:

    input_path = Path(args.input)

    try:
        with input_path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                line = line.rstrip("\n")
                if args.n:

                    print(f"{idx:6}  {line}")
                else:
                    print(line)
    except FileNotFoundError:
        raise SystemExit(f"Ошибка: файл '{input_path}' не найден")
    except OSError as exc:
        raise SystemExit(f"Ошибка при чтении файла '{input_path}': {exc}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI-утилиты для работы с текстом (ЛР6, на основе lab03)."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="команды",
        help="доступные подкоманды",
    )

    # ---- stats ----
    p_stats = subparsers.add_parser(
        "stats",
        help="анализ частот слов в текстовом файле",
    )
    p_stats.add_argument(
        "--input",
        required=True,
        help="путь к входному .txt файлу",
    )
    p_stats.add_argument(
        "--top",
        type=int,
        default=5,
        help="сколько наиболее частых слов вывести (по умолчанию 5)",
    )
    p_stats.set_defaults(func=cmd_stats)

    # ---- cat ----
    p_cat = subparsers.add_parser(
        "cat",
        help="вывод содержимого файла построчно",
    )
    p_cat.add_argument(
        "--input",
        required=True,
        help="путь к входному файлу",
    )
    p_cat.add_argument(
        "-n",
        action="store_true",
        help="нумеровать строки вывода",
    )
    p_cat.set_defaults(func=cmd_cat)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)

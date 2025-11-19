"""

    python -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
    python -m src.lab06.cli_convert csv2json --in data/samples/people.csv --out data/out/people.json
    python -m src.lab06.cli_convert csv2xlsx --in data/samples/people.csv --out data/out/people.xlsx
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def ensure_input_file(path_str: str) -> Path:

    path = Path(path_str)
    if not path.is_file():
        raise SystemExit(f"Ошибка: входной файл '{path}' не найден")
    return path


def ensure_output_dir(path_str: str) -> Path:
    """Создаёт директорию для выходного файла, если её нет."""
    path = Path(path_str)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SystemExit(f"Ошибка при создании директории '{path.parent}': {exc}")
    return path



def cmd_json2csv(args: argparse.Namespace) -> int:
    input_path = ensure_input_file(args.input)
    output_path = ensure_output_dir(args.output)

    try:
        json_to_csv(str(input_path), str(output_path))
    except Exception as exc:
        raise SystemExit(f"Ошибка конвертации JSON -> CSV: {exc}")

    print(f"Успешно: {input_path} -> {output_path}")
    return 0


def cmd_csv2json(args: argparse.Namespace) -> int:
    input_path = ensure_input_file(args.input)
    output_path = ensure_output_dir(args.output)

    try:
        csv_to_json(str(input_path), str(output_path))
    except Exception as exc:
        raise SystemExit(f"Ошибка конвертации CSV -> JSON: {exc}")

    print(f"Успешно: {input_path} -> {output_path}")
    return 0


def cmd_csv2xlsx(args: argparse.Namespace) -> int:
    input_path = ensure_input_file(args.input)
    output_path = ensure_output_dir(args.output)

    try:
        csv_to_xlsx(str(input_path), str(output_path))
    except Exception as exc:
        raise SystemExit(f"Ошибка конвертации CSV -> XLSX: {exc}")

    print(f"Успешно: {input_path} -> {output_path}")
    return 0




def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI-конвертеры данных (JSON/CSV/XLSX) для ЛР6 (на основе lab05)."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="команды",
        help="доступные операции конвертации",
    )


    p_json2csv = subparsers.add_parser(
        "json2csv",
        help="конвертация JSON -> CSV",
    )
    p_json2csv.add_argument(
        "--in",
        dest="input",
        required=True,
        help="путь к входному JSON-файлу (.json)",
    )
    p_json2csv.add_argument(
        "--out",
        dest="output",
        required=True,
        help="путь к выходному CSV-файлу (.csv)",
    )
    p_json2csv.set_defaults(func=cmd_json2csv)


    p_csv2json = subparsers.add_parser(
        "csv2json",
        help="конвертация CSV -> JSON",
    )
    p_csv2json.add_argument(
        "--in",
        dest="input",
        required=True,
        help="путь к входному CSV-файлу (.csv)",
    )
    p_csv2json.add_argument(
        "--out",
        dest="output",
        required=True,
        help="путь к выходному JSON-файлу (.json)",
    )
    p_csv2json.set_defaults(func=cmd_csv2json)


    p_csv2xlsx = subparsers.add_parser(
        "csv2xlsx",
        help="конвертация CSV -> XLSX",
    )
    p_csv2xlsx.add_argument(
        "--in",
        dest="input",
        required=True,
        help="путь к входному CSV-файлу (.csv)",
    )
    p_csv2xlsx.add_argument(
        "--out",
        dest="output",
        required=True,
        help="путь к выходному XLSX-файлу (.xlsx)",
    )
    p_csv2xlsx.set_defaults(func=cmd_csv2xlsx)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
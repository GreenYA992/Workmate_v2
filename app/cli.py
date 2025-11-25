import argparse
import os.path
import sys

from analyzers.employee_analyzer import EmployeeAnalyzer
from reports.console_report import ConsoleReport, TableReport
from reports.csv_report import CsvReport
from validators.file_validator import FileValidator

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def main() -> None:
    """Основная функция Cli"""
    parser = argparse.ArgumentParser(description="Анализ рейтинга по позициям")
    parser.add_argument("--files", nargs="+", required=True, help="файлы для анализа")
    parser.add_argument(
        "--report",
        nargs="+",
        required=True,
        choices=["performance", "table", "csv"],
        help="тип отчета: performance - списком, table - таблица, csv - в файл",
    )
    parser.add_argument("--output", help="Название файла (для сохранения в CSV)")

    args = parser.parse_args()

    try:
        valid_files = FileValidator.validate_file_path(args.files)
    except argparse.ArgumentTypeError as e:
        print(f"Ошибка {e}")
        sys.exit(1)

    all_emp = EmployeeAnalyzer.combine_files(valid_files)
    stats = EmployeeAnalyzer.calculate_statistics(all_emp)

    report_map = {
        "performance": ConsoleReport(),
        "table": TableReport(),
        "csv": CsvReport(args.output or "report.csv"),
    }

    for report_type in args.report:
        report = report_map[report_type]
        report.generate(stats)


if __name__ == "__main__":
    main()

# python cli.py --files ../data_folder/employees1.csv ../data_folder/employees2.csv --report performance

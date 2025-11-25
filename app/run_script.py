"""Модуль для простого запуска с установленными настройками"""

import sys

from cli import main

if __name__ == "__main__":
    files = [
        "C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate/"
        "/data_folder//employees1.csv",
        "C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate/"
        "/data_folder//employees2.csv",
    ]
    sys.argv = (
        ["cli.py", "--files"]
        + files
        + ["--report", "table", "csv", "--output", "new_report.csv"]
    )

    main()

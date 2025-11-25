import csv
import os
from typing import List

from models import PositionStats

from .base import Report


class CsvReport(Report):
    """Отчет в CSV файле"""

    def __init__(self, filename: str = "report.csv"):
        self.filename = filename
        # Поднимаемся из app/reports/ на уровень выше (в app), затем в data_folder
        base_dir = os.path.dirname(os.path.dirname(__file__))  # из app/reports/ -> app/
        parent_dir = os.path.dirname(base_dir)  # из app/ -> workmate/
        self.default_save_path = os.path.join(parent_dir, "data_folder", filename)

    def generate(self, stats: List[PositionStats]) -> None:
        os.makedirs(os.path.dirname(self.default_save_path), exist_ok=True)
        with open(self.default_save_path, "w", newline="", encoding="utf-8") as f:
            # noinspection PyTypeChecker
            writer = csv.DictWriter(f, fieldnames=["#", "Должность", "Рейтинг"])
            writer.writeheader()
            for i, stat in enumerate(stats, 1):
                writer.writerow(
                    {
                        "#": i,
                        "Должность": stat.position,
                        "Рейтинг": round(stat.avg_performance, 2),
                    }
                )
        print(f"Отчет сохранен в файл: {self.default_save_path}")

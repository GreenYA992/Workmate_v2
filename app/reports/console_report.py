from tabulate import tabulate
from typing import List
from .base import Report
from models import PositionStats

class ConsoleReport(Report):
    """Отчет в виде списка в консоли"""
    def generate(self, stats: List[PositionStats]) -> None:
        data = []
        for i, stat in enumerate(stats, 1):
            data.append([i, stat.position, stat.avg_performance])
        headers = ['', 'position', 'performance']
        print(
            tabulate(
                data, headers=headers, stralign="left", numalign="right", floatfmt=".2f"
            )
        )

class TableReport(Report):
    """Отчет в виде таблицы в консоли"""
    def generate(self, stats: List[PositionStats]) -> None:
        data = []
        for stat in stats:
            data.append([
                stat.position,
                round(stat.avg_performance, 2),
                stat.employee_count,
            ])
        headers = ["Должность", "Рейтинг", "Количество сотрудников"]
        print(tabulate(data, headers=headers, tablefmt="grid", stralign="center"))
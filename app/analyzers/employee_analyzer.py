from collections import defaultdict
from typing import List

from models import EmployeesData, PositionStats
from readers.base import DataReader


class EmployeeAnalyzer:
    """Анализатор сотрудников"""

    @staticmethod
    def combine_files(file_paths: List[str]) -> List[EmployeesData]:
        """Объединяем файлы из нескольких файлов"""
        all_employees = []

        for file_path in file_paths:
            reader = DataReader.create_reader(file_path)
            employees = reader.read(file_path)
            all_employees.extend(employees)

        return all_employees

    @staticmethod
    def calculate_statistics(employees: List[EmployeesData]) -> List[PositionStats]:
        """Вычисляем статистику по должностям"""
        position_data = defaultdict(list)

        for emp in employees:
            position_data[emp.position].append(emp.performance)

        stats = []
        for position, performance in position_data.items():
            avg_performance = sum(performance) / len(performance)
            stats.append(
                PositionStats(
                    position=position,
                    avg_performance=avg_performance,
                    employee_count=len(performance),
                )
            )
        return sorted(stats, key=lambda x: x.avg_performance, reverse=True)

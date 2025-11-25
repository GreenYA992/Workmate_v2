"""Тесты для модуля EmpAnalyzer"""

import os
import tempfile
from typing import List

import pytest
from models import EmployeesData
from tests.conftest import sample_employees

from app.analyzers.employee_analyzer import EmployeeAnalyzer


class TestEmpAnalyzer:
    """Тестирование класса EmpAnalyzer"""

    def test_calc_stat(self, sample_employees: List[EmployeesData]) -> None:
        """Тест расчета статистики"""

        res = EmployeeAnalyzer.calculate_statistics(sample_employees)

        assert len(res) == 2
        dev_stat = next(item for item in res if item.position == "Developer")
        assert dev_stat.avg_performance == 4.75
        assert dev_stat.employee_count == 2
        # проверяем сортировку по убыванию
        assert res[0].avg_performance >= res[1].avg_performance

    def test_calc_empty_data(self) -> None:
        """Тест на пустых данных"""
        res = EmployeeAnalyzer.calculate_statistics([])
        assert res == []

    def test_calc_single_emp(self) -> None:
        """Тест с одним сотрудником"""
        emp = [EmployeesData(name="test", position="Developer", performance=4.5)]
        res = EmployeeAnalyzer.calculate_statistics(emp)  # noqa

        assert len(res) == 1
        assert res[0].avg_performance == 4.5
        assert res[0].employee_count == 1

    def test_combining_files(self, multiple_temp_file: List[str]) -> None:
        """Тест объединения нескольких файлов"""

        res = EmployeeAnalyzer.combine_files(multiple_temp_file)

        assert len(res) == 4  # 2 разработчика и 2 QA

        names = [emp.name for emp in res]
        assert "Alex" in names
        assert "Maria" in names
        assert "John" in names
        assert "Anna" in names

        positions = [emp.position for emp in res]
        assert "Developer" in positions
        assert "QA" in positions

        performances = [emp.performance for emp in res]
        assert 4.5 in performances
        assert 4.8 in performances
        assert 5.0 in performances
        assert 4.2 in performances


class TestEmpAnalyzerErrors:
    """Тест обработки ошибок EmpAnalyzer"""

    def test_calc_stat_invalid_performance(self, temp_csv_invalid_data: str) -> None:
        """Тест с неправильными значениями performance"""
        with pytest.raises(ValueError, match="could not convert string to float"):
            EmployeeAnalyzer.combine_files([temp_csv_invalid_data])

    def test_calc_stat_missing_keys(self) -> None:
        """Тест с отсутствием ключевых данных"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,position,performance\n")
            f.write("Alex,Developer,\n")  # Пустой performance
            temp_path = f.name
        try:
            with pytest.raises(ValueError, match="could not convert string to float"):
                EmployeeAnalyzer.combine_files([temp_path])
        finally:
            os.unlink(temp_path)

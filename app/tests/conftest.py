import csv
import json
import os
import tempfile
from typing import Generator, List

import pytest

from app.models import EmployeesData, PositionStats

# Базовые тестовые данные
TEST_EMPLOYEE_DATA = [
    EmployeesData(name="Alex", position="Developer", performance=4.5),
    EmployeesData(name="Maria", position="QA", performance=4.8),
    EmployeesData(name="John", position="Developer", performance=5.0),
    EmployeesData(name="Anna", position="QA", performance=4.2),
]

TEST_STATS_DATA = [
    PositionStats(position="Developer", avg_performance=4.75, employee_count=2),
    PositionStats(position="QA", avg_performance=4.1, employee_count=1),
]


@pytest.fixture
def sample_employees() -> List[EmployeesData]:
    """Тестовые сотрудники (словари)"""
    return [
        EmployeesData(name="Alex", position="Developer", performance=4.5),
        EmployeesData(name="John", position="Developer", performance=5.0),
        EmployeesData(name="Anna", position="QA", performance=4.2),
    ]


@pytest.fixture
def sample_stats() -> List[PositionStats]:
    """Тестовые данные со статистикой"""
    return TEST_STATS_DATA.copy()


@pytest.fixture
def temp_csv_file() -> str:
    """Временный CSV файл"""
    return _create_temp_file(
        data=TEST_EMPLOYEE_DATA[:2], format_type="csv"  # берем первых двух сотрудников
    )


@pytest.fixture
def temp_json_file() -> str:
    """Временный JSON файл"""
    return _create_temp_file(
        data=TEST_EMPLOYEE_DATA[:2], format_type="json"  # берем первых двух сотрудников
    )


@pytest.fixture
def multiple_temp_file() -> Generator[List[str], None, None]:
    """Несколько временных файлов с разными данными"""
    files = []
    try:
        # Первый -Developers
        dev_data = [emp for emp in TEST_EMPLOYEE_DATA if emp.position == "Developer"]
        files.append(_create_temp_file(dev_data, "csv", suffix="_dev"))

        # Второй -Developers
        qa_data = [emp for emp in TEST_EMPLOYEE_DATA if emp.position == "QA"]
        files.append(_create_temp_file(qa_data, "csv", suffix="_qa"))

        yield files

    finally:
        # Удаляем
        for file_path in files:
            if os.path.exists(file_path):
                os.unlink(file_path)


@pytest.fixture
def temp_csv_invalid_data() -> str:
    """CSV с некорректными данными"""
    return _create_temp_file(
        data=[{"name": "Alex", "position": "Developer", "performance": "invalid"}],
        format_type="csv",
        suffix="_invalid",
    )


@pytest.fixture
def invalid_structure_csv() -> Generator[str, None, None]:
    """CSV с неправильной структурой"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(["email", "age", "hobbies"])
        writer.writerow(["test1@mail.ru", "35", "football"])
        writer.writerow(["test2@mail.ru", "25", "games"])
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def _create_temp_file(data: List, format_type: str, suffix: str = "") -> str:
    """Функция для создания временных файлов"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=f"{suffix}.{format_type}", delete=False
    ) as f:
        if format_type == "csv":
            writer = csv.writer(f)
            if data:
                # Записываем заголовки
                writer.writerow(["name", "position", "performance"])
                # Записываем данные
                for item in data:
                    if isinstance(item, EmployeesData):
                        writer.writerow(
                            [item.name, item.position, str(item.performance)]
                        )
                    else:
                        writer.writerow(
                            [item["name"], item["position"], item["performance"]]
                        )
        elif format_type == "json":
            if data and isinstance(data[0], EmployeesData):
                json_data = [
                    {
                        "name": emp.name,
                        "position": emp.position,
                        "performance": str(emp.performance),
                    }
                    for emp in data
                ]
                json.dump(json_data, f)
            else:
                json.dump(data, f)

    temp_path = f.name
    return temp_path

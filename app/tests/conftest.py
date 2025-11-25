import pytest
import tempfile
import csv
import json
import os

from app.models import PositionStats


# Базовые тестовые данные
TEST_EMPLOYEE_DATA = [
    {'name': 'Alex', 'position': 'Developer', 'performance': '4.5'},
    {'name': 'Maria', 'position': 'QA', 'performance': '4.8'},
    {'name': 'John', 'position': 'Developer', 'performance': '5.0'},
    {'name': 'Anna', 'position': 'QA', 'performance': '4.2'},
]

TEST_STATS_DATA = [
    PositionStats(position='Developer', avg_performance=4.75, employee_count=2),
    PositionStats(position='QA', avg_performance=4.1, employee_count=1),
]

@pytest.fixture
def sample_employees():
    """Тестовые сотрудники (словари)"""
    return [
        {'position': 'Developer', 'performance': '4.5'},
        {'position': 'Developer', 'performance': '5.0'},
        {'position': 'QA', 'performance': '4.0'},
    ]

@pytest.fixture
def sample_stats():
    """Тестовые данные со статистикой"""
    return TEST_STATS_DATA.copy()

@pytest.fixture
def temp_csv_file():
    """Временный CSV файл"""
    return _create_temp_file(
        data=TEST_EMPLOYEE_DATA[:2], # берем первых двух сотрудников
        format_type='csv'
    )

@pytest.fixture
def temp_json_file():
    """Временный JSON файл"""
    return _create_temp_file(
        data=TEST_EMPLOYEE_DATA[:2], # берем первых двух сотрудников
        format_type='json'
    )

@pytest.fixture
def multiple_temp_file():
    """Несколько временных файлов с разными данными"""
    files = []
    try:
        # Первый -Developers
        dev_data = [emp for emp in TEST_EMPLOYEE_DATA if emp['position'] == 'Developer']
        files.append(_create_temp_file(dev_data, 'csv', suffix='_dev'))

        # Второй -Developers
        qa_data = [emp for emp in TEST_EMPLOYEE_DATA if emp['position'] == 'QA']
        files.append(_create_temp_file(qa_data, 'csv', suffix='_qa'))

        yield  files

    finally:
        # Удаляем
        for file_path in files:
            if os.path.exists(file_path):
                os.unlink(file_path)

@pytest.fixture
def temp_csv_invalid_data():
    """CSV с некорректными данными"""
    return _create_temp_file(
        data=[{'name': 'Alex', 'position': 'Developer', 'performance': 'invalid'}],
        format_type='csv',
        suffix='_invalid'
    )

def invalid_structure_csv():
    """CSV с неправильной структурой"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['email', 'age', 'hobbies'])
        writer.writerow(['test1@mail.ru', '35', 'football'])
        writer.writerow(['test2@mail.ru', '25', 'games'])
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)

def _create_temp_file(data, format_type, suffix=''):
    """Функция для создания временных файлов"""
    with tempfile.NamedTemporaryFile(mode='w', suffix=f'{suffix}.{format_type}', delete=False) as f:
        if format_type == 'csv':
            writer = csv.writer(f)
            if data and isinstance(data[0], dict):
                # Записываем заголовки
                writer.writerow(['name','position','performance'])
                # Записываем данные
                for item in data:
                    writer.writerow([item['name'], item['position'], item['performance']])
        elif format_type == 'json':
            json.dump(data, f)

    temp_path = f.name
    return temp_path
"""Тесты для модуля DataReader"""

import os
import tempfile

import pytest

from app.readers.base import DataReader
from app.readers.csv_reader import CsvReader
from app.readers.json_reader import JsonReader


class TestDataReader:
    """Тестирование класса DataReader"""

    def test_read_csv_valid_file(self, temp_csv_file: str) -> None:
        """Тест чтения CSV файла"""
        reader = CsvReader()
        res = reader.read(temp_csv_file)
        assert len(res) == 2
        assert res[0].name == "Alex"
        assert res[0].position == "Developer"

    def test_read_json_valid_file(self, temp_json_file: str) -> None:
        """Тест чтения JSON файла, другой формат"""
        reader = JsonReader()
        res = reader.read(temp_json_file)
        assert len(res) == 2
        assert res[0].name == "Alex"
        assert res[1].name == "Maria"
        assert res[1].position == "QA"

    def test_both_readers_same_data(
        self, temp_csv_file: str, temp_json_file: str
    ) -> None:
        """Тест чтения JSON файла, другой формат"""
        csv_reader = CsvReader()
        json_reader = JsonReader()

        csv_data = csv_reader.read(temp_csv_file)
        json_data = json_reader.read(temp_json_file)
        assert len(csv_data) == len(json_data)
        assert csv_data[0].name == json_data[0].name

    def test_read_csv_nonexistent_file(self) -> None:
        """Тест чтение несуществующего файла"""
        reader = CsvReader()
        with pytest.raises(FileNotFoundError):
            reader.read("nonexistent_file.csv")

    def test_read_unsupported_format(self) -> None:
        """Тест чтение неподдерживаемого формата"""
        with pytest.raises(ValueError):
            DataReader.create_reader("file.txt")


class TestDataReaderErrors:
    """Тесты на обработку ошибок"""

    @pytest.fixture
    def test_read_csv_invalid_structure(
        self, invalid_structure_csv: str
    ) -> None:  # noqa
        """Тест чтение CSV с неправильной структурой"""

        reader = CsvReader()
        res = reader.read(invalid_structure_csv)

        assert len(res) == 2
        assert res[0].name == "test1@mail.ru"
        assert res[0].position == "35"
        assert res[0].performance == "football"

    def test_read_csv_empty_file(self) -> None:
        """Тест чтение пустого CSV"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("")
            temp_path = f.name
        try:
            reader = CsvReader()
            res = reader.read(temp_path)
            assert res == []
        finally:
            os.unlink(temp_path)

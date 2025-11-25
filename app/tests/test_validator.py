"""Тесты для модуля Validator"""

import argparse

import pytest

from app.validators.file_validator import FileValidator


class TestValidator:
    """Тесты для класса Validator"""

    def test_validate_file_paths_all_valid(self, temp_csv_file, temp_json_file):
        """Тест когда все файлы корректные"""

        files = [temp_csv_file, temp_json_file]
        res = FileValidator.validate_file_path(files)

        assert len(res) == 2
        assert temp_csv_file in res
        assert temp_json_file in res

    def test_validate_file_paths_mixed(self, temp_csv_file):
        """Тест когда часть файлов не корректна"""

        files = [temp_csv_file, "nonexistent.csv", "file.txt"]
        res = FileValidator.validate_file_path(files)
        assert res == [temp_csv_file]
        assert len(res) == 1

    def test_validate_file_paths_all_invalid(self):
        """Тест когда все файлы не корректные"""
        files = ["nonexistent.csv", "file.txt", "img.png"]
        with pytest.raises(argparse.ArgumentTypeError):
            FileValidator.validate_file_path(files)


class TestValidatorErrors:
    """Тест обработки ошибок в Validator"""

    def test_validate_path_nonexistent_file(self):
        """Тест с несуществующими файлами"""
        files = ["nonexistent1.csv", "nonexistent2.csv"]

        with pytest.raises(argparse.ArgumentTypeError) as e:
            FileValidator.validate_file_path(files)

        assert "Не найдено ни одного файла" in str(e.value)

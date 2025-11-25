"""Тесты для модуля Validator"""

import argparse
import os
import tempfile

import pytest
from app.validators.file_validator import FileValidator


class TestValidator:
    """Тесты для класса Validator"""

    def test_validate_file_paths_all_valid(self):
        """Тест когда все файлы корректные"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f1:
            f1_path = f1.name
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f2:
            f2_path = f2.name
        try:
            files = [f1_path, f2_path]
            res = FileValidator.validate_file_path(files)
            assert res == files
            assert len(res) == 2
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_validate_file_paths_mixed(self):
        """Тест когда часть файлов не корректна"""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            valid_file = f.name
        try:
            files = [valid_file, "nonexistent.csv", "file.txt"]
            res = FileValidator.validate_file_path(files)
            assert res == [valid_file]
            assert len(res) == 1
        finally:
            os.unlink(valid_file)

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

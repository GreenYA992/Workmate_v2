import os
import argparse
from typing import List

class FileValidator:
    """Класс для валидации данных"""

    SUPPORTED_EXTENSIONS = ["csv", "json"]

    @classmethod
    def validate_file_path(cls, file_paths: List[str]) -> List[str]:
        """Проверяет список путей к файлам"""
        valid_files = []
        missing_files = []
        invalid_format_files = []
        messages = []

        for file_path in file_paths:
            file_ext = file_path.lower().split(".")[-1]
            if file_ext not in cls.SUPPORTED_EXTENSIONS:
                invalid_format_files.append(file_path)
                continue
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                continue
            valid_files.append(file_path)

        if valid_files:
            messages.append(f"Обработано файлов: {len(valid_files)}")
        if missing_files:
            messages.append(f"Файлы не найдены: {', '.join(missing_files)}")
        if invalid_format_files:
            messages.append(f"Нераспознанный формат: {', '.join(invalid_format_files)}")

        if messages:
            print("\n".join(messages))

        if not valid_files:
            raise argparse.ArgumentTypeError(
                f"Не найдено ни одного файла для обработки. "
                f"Проверьте пути и форматы файлов. "
                f"Поддерживаемые форматы: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
            )
        return valid_files
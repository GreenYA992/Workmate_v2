from abc import ABC, abstractmethod
from typing import Dict, List, Type

from models import EmployeesData


class DataReader(ABC):
    """Абстрактный класс для чтения данных"""

    _readers: Dict[str, Type["DataReader"]] = {}

    @abstractmethod
    def read(self, file_path: str) -> List[EmployeesData]:
        """Читает файл и возвращает данные"""
        pass

    @classmethod
    def registry_reader(
        cls, format_name: str, reader_class: Type["DataReader"]
    ) -> None:
        """Регистрируем ридер для формата"""
        cls._readers[format_name] = reader_class

    @classmethod
    def create_reader(cls, file_path: str) -> "DataReader":
        """Метод для создания ридера"""
        file_ext = file_path.lower().split(".")[-1]

        if file_ext not in cls._readers:
            raise ValueError(f"Неправильный формат файла {file_ext}")

        return cls._readers[file_ext]()

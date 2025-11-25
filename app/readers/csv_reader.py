import csv
from typing import List
from .base import DataReader
from models import EmployeesData

class CsvReader(DataReader):
    """Реализация чтения CSV"""
    def read(self, file_path: str) -> List[EmployeesData]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [EmployeesData(**item) for item in reader]

DataReader.registry_reader('csv', CsvReader)
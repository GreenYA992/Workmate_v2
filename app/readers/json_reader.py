import json
from typing import List

from models import EmployeesData

from .base import DataReader


class JsonReader(DataReader):
    """Реализации чтения Json файлов"""

    def read(self, file_path: str) -> List[EmployeesData]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = json.load(f)
            return [EmployeesData.from_dict(item) for item in reader]


DataReader.registry_reader("json", JsonReader)

from abc import ABC, abstractmethod
from typing import List

from models import PositionStats


class Report(ABC):
    """Абстрактный класс для генерации отчетов"""

    @abstractmethod
    def generate(self, stats: List[PositionStats]) -> None:
        """Генерируем отчет"""
        pass

from dataclasses import dataclass
from typing import Dict, Any, TypedDict

class EmployeesData(TypedDict):
    """Типизированный словарь для сотрудников"""
    name: str
    position: str
    performance: str

@dataclass
class PositionStats:
    """DTO для статистики по должностям"""
    position: str
    avg_performance: float
    employee_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            'position': self.position,
            'avg_performance': round(self.avg_performance, 2),
            'employee_count': self.employee_count
        }
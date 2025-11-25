from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class EmployeesData:
    """DTO для дынных сотрудника"""

    name: str
    position: str
    performance: float

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "EmployeesData":
        """Объект словаря с преобразованием типов"""
        return cls(
            name=data["name"],
            position=data["position"],
            performance=float(data["performance"]),
        )


@dataclass
class PositionStats:
    """DTO для статистики по должностям"""

    position: str
    avg_performance: float
    employee_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "avg_performance": round(self.avg_performance, 2),
            "employee_count": self.employee_count,
        }

from typing import List

import pytest

from app.analyzers.employee_analyzer import EmployeeAnalyzer
from app.reports.console_report import ConsoleReport


class TestIntegration:
    """Интеграционные тесты"""

    def test_workflow(
        self, capsys: pytest.CaptureFixture, multiple_temp_file: List[str]
    ) -> None:
        """Тест полного workflow"""

        emp = EmployeeAnalyzer.combine_files(multiple_temp_file)
        stats = EmployeeAnalyzer.calculate_statistics(emp)

        report = ConsoleReport()
        report.generate(stats)

        captured = capsys.readouterr()
        output = captured.out

        assert "Developer" in output
        assert "QA" in output
        assert "4.75" in output
        assert "4.5" in output


class TestIntegrationErrors:
    """Интеграционный тест с ошибками"""

    def test_workflow_with_invalid_data(self, temp_csv_invalid_data: str) -> None:
        """Тест workflow с некорректными данными"""
        with pytest.raises(ValueError, match="could not convert string to float"):
            EmployeeAnalyzer.combine_files([temp_csv_invalid_data])

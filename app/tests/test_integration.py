import pytest

from app.analyzers.employee_analyzer import EmployeeAnalyzer
from app.reports.console_report import ConsoleReport


class TestIntegration:
    """Интеграционные тесты"""

    def test_workflow(self, capsys, multiple_temp_file):
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

    def test_workflow_with_invalid_data(self, temp_csv_invalid_data):
        """Тест workflow с некорректными данными"""

        emp = EmployeeAnalyzer.combine_files([temp_csv_invalid_data])

        with pytest.raises(ValueError):
            EmployeeAnalyzer.calculate_statistics(emp)

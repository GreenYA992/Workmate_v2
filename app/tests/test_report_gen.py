"""Тест для модуля ReportGen"""

from models import PositionStats
from reports.console_report import ConsoleReport, TableReport


class TestReportGen:
    """Тестирование класса ReportGen"""

    def test_report_output(self, capsys):
        """Тест вывода отчета performance"""
        stats = [
            PositionStats(position="Developer", avg_performance=4.75, employee_count=2),
            PositionStats(position="QA", avg_performance=4.1, employee_count=1),
        ]
        report = ConsoleReport()
        report.generate(stats)

        captured = capsys.readouterr()
        output = captured.out

        assert "Developer" in output and "4.75" in output
        assert "QA" in output and "4.10" in output
        assert "1" in output and "2" in output

        lines = output.strip().split("\n")
        assert len(lines) >= 4  # заголовок, разделитель и 2 строки

    def test_table_report(self, capsys):
        """Тест табличного отчета"""
        stats = [
            PositionStats(position="Developer", avg_performance=4.75, employee_count=2),
        ]

        report = TableReport()
        report.generate(stats)
        captured = capsys.readouterr()
        output = captured.out

        assert "Должность" in output
        assert "Рейтинг" in output
        assert "Developer" in output
        assert "4.75" in output

    def test_report_empty_stats(self, capsys):
        """Тест отчета с пустой статистикой"""
        report = ConsoleReport()
        report.generate([])
        captured = capsys.readouterr()
        output = captured.out

        # Должны быть заголовки, даже при пустых данных
        assert "position" in output
        assert "performance" in output

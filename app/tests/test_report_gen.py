"""Тест для модуля ReportGen"""
import tempfile
import os
import csv

from app.models import PositionStats
from app.reports.console_report import ConsoleReport, TableReport
from reports.csv_report import CsvReport


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

    def test_csv_report_create(self):
        """Тест создания CSV отчета"""
        stats = [PositionStats(position='Developer', avg_performance=4.75, employee_count=2)]
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test_report.csv')
            report = CsvReport(test_file)
            report.generate(stats)

            assert os.path.exists(test_file)

            with open(test_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 1
                assert rows[0]['Должность'] == 'Developer'
                assert rows[0]['Рейтинг'] == '4.75'

    def test_report_empty_stats(self, capsys):
        """Тест отчета с пустой статистикой"""
        report = ConsoleReport()
        report.generate([])
        captured = capsys.readouterr()
        output = captured.out

        # Должны быть заголовки, даже при пустых данных
        assert "position" in output
        assert "performance" in output


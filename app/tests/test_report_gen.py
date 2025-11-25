"""Тест для модуля ReportGen"""

import csv
import os
import tempfile
from typing import List

import pytest

from app.models import PositionStats
from app.reports.console_report import ConsoleReport, TableReport
from app.reports.csv_report import CsvReport


class TestReportGen:
    """Тестирование класса ReportGen"""

    def test_report_output(
        self, capsys: pytest.CaptureFixture, sample_stats: List[PositionStats]
    ) -> None:
        """Тест вывода отчета performance"""

        report = ConsoleReport()
        report.generate(sample_stats)

        captured = capsys.readouterr()
        output = captured.out

        assert "Developer" in output and "4.75" in output
        assert "QA" in output and "4.10" in output
        assert "1" in output and "2" in output

        lines = output.strip().split("\n")
        assert len(lines) >= 4  # заголовок, разделитель и 2 строки

    def test_table_report(
        self, capsys: pytest.CaptureFixture, sample_stats: List[PositionStats]
    ) -> None:
        """Тест табличного отчета"""

        report = TableReport()
        report.generate(sample_stats)
        captured = capsys.readouterr()
        output = captured.out

        assert "Должность" in output
        assert "Рейтинг" in output
        assert "Developer" in output
        assert "4.75" in output

    def test_csv_report_create(self, sample_stats: List[PositionStats]) -> None:
        """Тест создания CSV отчета"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test_report.csv")
            report = CsvReport(test_file)
            report.generate(sample_stats)

            assert os.path.exists(test_file)

            with open(test_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 2
                dev_row = next(row for row in rows if row["Должность"] == "Developer")
                assert dev_row["Рейтинг"] == "4.75"

    def test_report_empty_stats(self, capsys: pytest.CaptureFixture) -> None:
        """Тест отчета с пустой статистикой"""
        report = ConsoleReport()
        report.generate([])
        captured = capsys.readouterr()
        output = captured.out

        # Должны быть заголовки, даже при пустых данных
        assert "position" in output
        assert "performance" in output

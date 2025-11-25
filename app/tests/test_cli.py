from unittest.mock import patch

import pytest

from app.cli import main


def test_cli_nonexistent_files() -> None:
    """Тест CLI с несуществующими данными"""
    with patch(
        "sys.argv", ["cli.py", "--files", "nonexistent.csv", "--report", "performance"]
    ):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0


def test_cli_missing_args() -> None:
    """Тест CLI отсутствующими аргументами"""
    with patch("sys.argv", ["cli.py"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0


def test_cli_invalid_report_type() -> None:
    """Тест CLI с неверным типом отчета"""
    with patch(
        "sys.argv", ["cli.py", "--files", "nonexistent.csv", "--report", "invalid_type"]
    ):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0

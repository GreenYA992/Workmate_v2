import pytest
from app.cli import main
from unittest.mock import patch


def test_cli_nonexistent_files():
    """Тест CLI с несуществующими данными"""
    with patch('sys.argv', ['cli.py', '--files', 'nonexistent.csv', '--report', 'performance']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0

def test_cli_missing_args():
    """Тест CLI отсутствующими аргументами"""
    with patch('sys.argv', ['cli.py']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0

def test_cli_invalid_report_type():
    """Тест CLI с неверным типом отчета"""
    with patch('sys.argv', ['cli.py', '--files', 'nonexistent.csv', '--report', 'invalid_type']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0


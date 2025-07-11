from unittest.mock import patch, mock_open
import pytest
from adapter.ssd_shell_adapter import SSDShellAdapter

driver = SSDShellAdapter()


@patch("pathlib.Path.open", new_callable=mock_open, read_data="0xCAFEBABE")
@patch("subprocess.run")
def test_read(mock_subproc_run, mock_file):
    result = driver.read(10)

    mock_subproc_run.assert_called_once_with(
        ["python", "ssd.py", "R", "10"], check=True
    )
    mock_file.assert_called_once()  # Path.open()이 호출됐는지 확인
    assert result == "0xCAFEBABE"


@patch("subprocess.run")
def test_write(mock_subproc_run):
    driver.write(5, 0x12345678)

    mock_subproc_run.assert_called_once_with(["python", "ssd.py", "W", "5", "0x12345678"], check=True)


@patch("subprocess.run")
def test_erase(mock_subproc_run):
    driver.erase(3, 2)

    mock_subproc_run.assert_called_once_with(["python", "ssd.py", "E", "3", "2"], check=True)


@patch("subprocess.run")
def test_flush(mock_subproc_run):
    driver.flush()

    mock_subproc_run.assert_called_once_with(["python", "ssd.py", "F"], check=True)

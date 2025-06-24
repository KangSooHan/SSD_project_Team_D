import os
import subprocess
import textwrap
import pytest
from unittest.mock import patch
import builtins
import sys

from shell import Shell, main


def init_nand_file_for_test():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nand_path = os.path.join(project_root, "ssd_nand.txt")
    with open(nand_path, "w") as f:
        for i in range(100):
            f.write(f"{i} 0x00000005\n")


def shell_system_call(input_script: str) -> str:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    shell_py_path = os.path.join(project_root, "shell.py")

    process = subprocess.Popen(
        ["python", shell_py_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
        cwd=project_root
    )

    try:
        stdout, stderr = process.communicate(input=input_script, timeout=15)
        if process.returncode != 0:
            print("=== STDERR ===\n", stderr)
            pytest.fail(f"Shell exited with status {process.returncode}")
        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        pytest.fail("Shell command timed out")


def test_shell_exit_only():
    stdout = shell_system_call("exit\n")
    assert "Test Shell Application" in stdout


def test_shell_read():
    init_nand_file_for_test()
    stdout = shell_system_call("read 10\nexit\n")
    assert "[Read] LBA 10 : 0x00000005" in stdout


def test_shell_write():
    stdout = shell_system_call("write 0 0x00000001\nexit\n")
    assert "[Write] Done" in stdout


def test_shell_help():
    stdout = shell_system_call("help\nexit\n")
    assert "- write : write {LBA} {VALUE}" in stdout
    assert "- read : read {LBA}" in stdout
    assert "- exit : exit" in stdout


def test_shell_invalid_command():
    stdout = shell_system_call("invalid_command\nexit\n")
    assert "INVALID COMMAND" in stdout


def test_shell_fullwrite_and_fullread():
    stdout = shell_system_call("fullwrite 0xABCDFFFF\nfullread\nexit\n")
    for i in range(100):
        assert f"[Read] LBA {i:02d} : 0xABCDFFFF" in stdout


@patch.object(builtins, 'input', side_effect=SystemExit)
def test_start_shell_outputs_start_message(mock_input, capsys):
    shell = Shell()
    try:
        shell.start_interactive()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "<< Test Shell Application >> Start" in captured.out


@patch.object(sys, 'argv', ["shell.py"])
@patch.object(builtins, 'input', side_effect=SystemExit)
def test_main_without_args_runs_shell(mock_input, capsys):
    try:
        main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "<< Test Shell Application >> Start" in captured.out

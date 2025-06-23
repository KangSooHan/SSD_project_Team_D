import os
import subprocess
import textwrap

import pytest


def init_nand_file_for_test():
    """테스트용 NAND 파일 생성"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nand_path = os.path.join(project_root, "ssd_nand.txt")
    with open(nand_path, "w") as f:
        for i in range(100):
            f.write(f"{i} 0x00000005\n")


def shell_system_call(input_script: str) -> str:
    """
    shell.py를 루트에서 실행하고 stdout, stderr를 받아 반환합니다.
    에러 발생 시 디버깅 정보를 출력합니다.
    """
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
        print("=== STDOUT ===\n", stdout)
        print("=== STDERR ===\n", stderr)
        if process.returncode != 0:
            pytest.fail(f"Shell exited with status {process.returncode}.\nSTDERR:\n{stderr}")
        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("=== TIMEOUT STDOUT ===\n", stdout)
        print("=== TIMEOUT STDERR ===\n", stderr)
        pytest.fail("타임아웃 에러")


def test_shell_단순실행테스트():
    input_script = "exit\n"
    stdout = shell_system_call(input_script)
    assert "Test Shell Application" in stdout


def test_shell_read_실행테스트():
    init_nand_file_for_test()
    input_script = "read 10\nexit\n"
    stdout = shell_system_call(input_script)
    assert "[Read] LBA 10 : 0x00000005" in stdout


def test_shell_write_실행테스트():
    input_script = "write 0 0x00000001\nexit\n"
    stdout = shell_system_call(input_script)
    assert "[Write] Done" in stdout


def test_shell_help_실행테스트():
    input_script = "help\nexit\n"
    stdout = shell_system_call(input_script)
    cmd_msg = textwrap.dedent('''
        - write : write {LBA} {VALUE}
        - read : read {LBA}
        - exit : exit
        - help : help
        - fullwrite : fullwrite {VALUE}
        - fullread : fullread
        ''').strip()
    assert cmd_msg in stdout


def test_shell_잘못된_입력시_INVALID_실행테스트():
    input_script = "test\nexit\n"
    stdout = shell_system_call(input_script)
    assert "INVALID COMMAND" in stdout


def test_shell_fullwrite_then_fullread_실행테스트():
    """fullwrite 후 fullread 명령을 통해 결과를 검증"""
    input_script = "fullwrite 0xABCDFFFF\nfullread\nexit\n"
    stdout = shell_system_call(input_script)
    expected_lines = [f"[Read] LBA {i:02d} : 0xABCDFFFF" for i in range(100)]
    for line in expected_lines:
        assert line in stdout


def test_shell_runner_1_실행테스트():
    input_script = "shell_scripts.txt\nexit\n"
    stdout = shell_system_call(input_script)
    cmd_msg = textwrap.dedent('''
    1_FullWriteAndReadCompare ___ Run...Pass
    ''').strip()
    assert cmd_msg in stdout

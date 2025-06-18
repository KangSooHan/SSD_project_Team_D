import io
import subprocess
import sys

import pytest


def pipe(input_script):
    process = subprocess.Popen(
        ["python", "../shell/shell.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # 입력을 전달 하고 출력을 받아옴
    try:
        stdout, stderr = process.communicate(input=input_script, timeout=3)
        print("stdout")
        print(stdout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        pytest.fail("Mock shell 타임 아웃 에러")
    return stdout

def test_mock_shell_init():
    process = subprocess.Popen(
        ["python", "../shell/shell.py"],  # <-- 테스트 대상을 mock_shell.py로 변경
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert 1 == 1

def test_mock_shell_exit():
    input_script = "exit"
    stdout = pipe(input_script)

    assert "Exit" in stdout


def test_mock_shell_read():
    input_script = "read 0"
    stdout = pipe(input_script)

    read_message = "[Read] LBA 00 : 0x00000000"

    assert read_message in stdout


def test_mock_shell_write():
    input_script = "write 0 0x00000001"
    stdout = pipe(input_script)
    write_message = "[Write] Done"

    assert write_message in stdout



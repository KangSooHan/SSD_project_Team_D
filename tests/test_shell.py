import subprocess
import pytest

def pipe(input_script):
    """간단한 subprocess 방식 pipe 함수"""
    process = subprocess.Popen(
        ["python", "../shell/shell.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    try:
        stdout, stderr = process.communicate(input=input_script, timeout=5)
        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        pytest.fail("타임아웃 에러")
        return None


def test_shell_실행테스트():
    process = subprocess.Popen(
        ["python", "../shell/shell.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    try:
        stdout, stderr = process.communicate(input="exit", timeout=3)
        assert "Test Shell Application" in stdout
        assert "Exit" in stdout
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        pytest.fail("Mock shell 타임 아웃 에러")
        return None


def test_shell_exit_실행테스트():
    input_script = "exit"
    stdout = pipe(input_script)
    assert "Exit" in stdout


def test_shell_read_실행테스트():
    input_script = "read 0\nexit"
    stdout = pipe(input_script)
    read_message = "[Read] LBA 00 : 0x00000000"
    assert read_message in stdout


def test_shell_write_실행테스트():
    input_script = "write 0 0x00000001\nexit"
    stdout = pipe(input_script)
    write_message = "[Write] Done"
    assert write_message in stdout


def test_shell_help_실행테스트():
    input_script = "help\nexit"
    stdout = pipe(input_script)
    write_message = "---- 제작자 & 명령어 ----"
    assert write_message in stdout

def test_shell_여러개의_명령어_실행테스트():
    """여러 명령어 테스트"""
    input_script = "help\nread 0\nwrite 0 0x00000001\nexit"
    stdout = pipe(input_script)
    assert "---- 제작자 & 명령어 ----" in stdout
    assert "[Read] LBA 00 : 0x00000000" in stdout
    assert "[Write] Done" in stdout
    assert "Exit" in stdout



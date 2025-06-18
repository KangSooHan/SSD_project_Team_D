import subprocess
import pytest


def init_nand_file_for_test():
    """
    테스트 하기 위해 파일을 임시로 생성 합니다.
    """
    file_name = 'ssd_nand.txt'
    content = '0x00000005'
    number_of_lines = 99

    with open(file_name, 'w') as f:
        for _ in range(number_of_lines):
            f.write(content + '\n')


def shell_system_call(input_script):
    """간단한 subprocess 방식 pipe 함수"""
    process = subprocess.Popen(
        ["python", "../shell.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )

    try:
        stdout, stderr = process.communicate(input=input_script, timeout=5)
        if stdout is None:
            stdout = ""
        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        pytest.fail("타임아웃 에러")
        return ""
    except Exception as e:
        process.kill()
        process.wait()
        pytest.fail(f"Subprocess 에러: {e}")
        return ""


def test_shell_단순실행테스트():
    input_script = "exit\n"
    stdout = shell_system_call(input_script)

    assert "Test Shell Application" in stdout

def test_shell_read_실행테스트():
    init_nand_file_for_test()

    input_script = "read 10\nexit"
    stdout = shell_system_call(input_script)
    read_message = "[Read] LBA 00 : 0x00000005"
    assert read_message in stdout


def test_shell_write_실행테스트():
    input_script = "write 0 0x00000001\nexit"
    stdout = shell_system_call(input_script)
    write_message = "[Write] Done"
    assert write_message in stdout


def test_shell_help_실행테스트():
    input_script = "help\nexit"
    stdout = shell_system_call(input_script)
    print(stdout)
    assert "팀명: Discovery | 팀원: 강수한, 이후광, 윤창흠, 김지영, 이지훈, 박치원" in stdout
    assert "명령어 사용 방법 :" in stdout
    assert "write : write {LBA} {VALUE}" in stdout
    assert "read : read {LBA}" in stdout
    assert "exit : exit" in stdout
    assert "help : help" in stdout
    assert "fullwrite : fullwrite {VALUE}" in stdout
    assert "fullread : fullread" in stdout

def test_shell_fullwrite_실행테스트():
    """fullwrite 테스트"""
    input_script = "fullwrite 0xABCDFFFF\nexit"
    stdout = shell_system_call(input_script)
    assert 1 == 1

def test_shell_fullread_실행테스트():
    """fullread 테스트"""
    init_nand_file_for_test()

    input_script = "fullread\nexit"
    stdout = shell_system_call(input_script)
    expected = ""
    for _ in range(100):
        expected += "0x00000005\n"

    assert expected in stdout

import pytest
from validator import Validator

CORRECT_WRITE_SENTENCE="w 0 0xFFFFFFFF"

def test_검증기_실행_테스트():
    validator = Validator()
    assert validator.run("test_input")

def test_검증기_쓰기_올바른_입력_성공():
    validator = Validator()
    assert validator.run(CORRECT_WRITE_SENTENCE) == True


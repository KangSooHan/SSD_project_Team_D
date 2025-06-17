import pytest
from validator import Validator

CORRECT_WRITE_SENTENCE="w 0 0xFFFFFFFF"

def test_검증기_실행_테스트():
    validator = Validator()
    assert validator.run("test_input")

def test_검증기_쓰기_올바른_입력_성공():
    validator = Validator()
    assert validator.run(CORRECT_WRITE_SENTENCE) == True

@pytest.mark.parametrize("wrong_input", ["w", "0", "0xFFFFFFFF",
                                         "w 0", "w 0xFFFFFFFF", "0 0xFFFFFFFF",
                                         "w 0 0xFFFFFFFF 0xFFFFFFFF"])
def test_검증기_쓰기_틀린_입력_잘못된_입력_길이(wrong_input):
    validator = Validator()
    assert validator.run(wrong_input) == False
import pytest
from validator import Validator

CORRECT_WRITE_SENTENCE="w 0 0xFFFFFFFF"
CORRECT_READ_SENTENCE="r 0"

@pytest.fixture
def validator():
    return Validator()

def test_검증기_실행_테스트(validator):
    assert validator.run("test_input")

def test_검증기_쓰기_올바른_입력_성공(validator):
    assert validator.run(CORRECT_WRITE_SENTENCE) == True

@pytest.mark.parametrize("wrong_input", ["w", "0", "0xFFFFFFFF",
                                         "w 0", "w 0xFFFFFFFF", "0 0xFFFFFFFF",
                                         "w 0 0xFFFFFFFF 0xFFFFFFFF"])
def test_검증기_쓰기_잘못된_입력_길이(wrong_input, validator):
    assert validator.run(wrong_input) == False
    
def test_검증기_읽기_올바른_입력_성공(validator):
    assert validator.run(CORRECT_READ_SENTENCE) == True

@pytest.mark.parametrize("wrong_input", ["r", "0", "r 0 0"])
def test_검증기_읽기_잘못된_입력_길이(wrong_input, validator):
    assert validator.run(wrong_input) == False

def make_wrong_sentences():
    wrong_sentences = []
    wrong_sentences.append(" " + CORRECT_READ_SENTENCE)
    wrong_sentences.append(CORRECT_READ_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_READ_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_WRITE_SENTENCE)
    wrong_sentences.append(CORRECT_WRITE_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_WRITE_SENTENCE + " ")

    return wrong_sentences

def test_검증기_앞뒤_공백_문자(validator):
    wrong_sentences = make_wrong_sentences()
    for wrong_sentence in wrong_sentences:
        assert validator.run(wrong_sentence) == True
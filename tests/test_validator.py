import pytest
from validator import Validator

CORRECT_WRITE_SENTENCE="w 0 0xFFFFFFFF"
CORRECT_READ_SENTENCE="r 0"

@pytest.fixture
def validator():
    return Validator()

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

def make_correct_upper_lower_sentences():
    sentences = []
    sentences.append(CORRECT_WRITE_SENTENCE.upper())
    sentences.append(CORRECT_READ_SENTENCE.upper())
    sentences.append(CORRECT_WRITE_SENTENCE.lower())
    sentences.append(CORRECT_READ_SENTENCE.lower())
    return sentences

def test_검증기_대소문자_성공(validator):
    correct_sentences = make_correct_upper_lower_sentences()

    for correct_sentence in correct_sentences:
        assert validator.run(correct_sentence) == True

@pytest.mark.parametrize("wrong_input", ["w -1 0xFFFFFFFF", "w 100 0xFFFFFFFF", "w w 0xFFFFFFFF",
                                         "r -1", "r 100", "r r"])
def test_검증기_잘못된_LBA_입력(wrong_input, validator):
    assert validator.run(wrong_input) == False

@pytest.mark.parametrize("wrong_input", ["wrong 0 0xFFFFFFFF",  "wrong 100"])
def test_검증기_잘못된_COMMAND_입력(wrong_input, validator):
    assert validator.run(wrong_input) == False

@pytest.mark.parametrize("wrong_input", ["w 0 00FFFFFFFF", "w 0 0xGFFFFFFF",
                                        "w 0 0x-1FFFFFFF", "w 0 0xZZZZZZZZ"])
def test_검증기_잘못된_VALUE_입력(wrong_input, validator):
    assert validator.run(wrong_input) == False
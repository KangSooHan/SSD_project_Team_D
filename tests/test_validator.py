import pytest
from validator import SSDValidator, ShellValidator

CORRECT_WRITE_SENTENCE = "w 0 0xFFFFFFFF"
CORRECT_READ_SENTENCE = "r 0"


@pytest.fixture
def ssdvalidator():
    return SSDValidator()

@pytest.fixture
def shellvalidator():
    return ShellValidator()

def test_검증기_쓰기_올바른_입력_성공(ssdvalidator):
    assert ssdvalidator._validate_test(CORRECT_WRITE_SENTENCE) == True


@pytest.mark.parametrize("wrong_input", ["w", "0", "0xFFFFFFFF",
                                         "w 0", "w 0xFFFFFFFF", "0 0xFFFFFFFF",
                                         "w 0 0xFFFFFFFF 0xFFFFFFFF"])
def test_검증기_쓰기_잘못된_입력_길이(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False


def test_검증기_읽기_올바른_입력_성공(ssdvalidator):
    assert ssdvalidator._validate_test(CORRECT_READ_SENTENCE) == True


@pytest.mark.parametrize("wrong_input", ["r", "0", "r 0 0"])
def test_검증기_읽기_잘못된_입력_길이(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False


def make_wrong_sentences():
    wrong_sentences = []
    wrong_sentences.append(" " + CORRECT_READ_SENTENCE)
    wrong_sentences.append(CORRECT_READ_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_READ_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_WRITE_SENTENCE)
    wrong_sentences.append(CORRECT_WRITE_SENTENCE + " ")
    wrong_sentences.append(" " + CORRECT_WRITE_SENTENCE + " ")

    return wrong_sentences


def test_검증기_앞뒤_공백_문자(ssdvalidator):
    wrong_sentences = make_wrong_sentences()
    for wrong_sentence in wrong_sentences:
        assert ssdvalidator._validate_test(wrong_sentence) == True


def make_correct_upper_lower_sentences():
    sentences = []
    sentences.append(CORRECT_WRITE_SENTENCE.upper())
    sentences.append(CORRECT_READ_SENTENCE.upper())
    sentences.append(CORRECT_WRITE_SENTENCE.lower())
    sentences.append(CORRECT_READ_SENTENCE.lower())
    return sentences


def test_검증기_대소문자_성공(ssdvalidator):
    correct_sentences = make_correct_upper_lower_sentences()

    for correct_sentence in correct_sentences:
        assert ssdvalidator._validate_test(correct_sentence) == True


@pytest.mark.parametrize("wrong_input", ["w -1 0xFFFFFFFF", "w 100 0xFFFFFFFF", "w w 0xFFFFFFFF",
                                         "r -1", "r 100", "r r"])
def test_검증기_잘못된_LBA_입력(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False


@pytest.mark.parametrize("wrong_input", ["wrong 0 0xFFFFFFFF", "wrong 100"])
def test_검증기_잘못된_COMMAND_입력(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False


@pytest.mark.parametrize("wrong_input", ["w 0 00FFFFFFFF", "w 0 0xGFFFFFFF",
                                         "w 0 0x-1FFFFFFF", "w 0 0xZZZZZZZZ"])
def test_검증기_잘못된_VALUE_입력(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False

def test_검증기_값_가져오는_함수(ssdvalidator):
    assert ssdvalidator.run(CORRECT_WRITE_SENTENCE) == ("W", 0, int("0xFFFFFFFF", 16))
    assert ssdvalidator.run(CORRECT_READ_SENTENCE) == ("R", 0, None)

@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("write 0 0xFFFFFFFF", ("write", 0, int("0xFFFFFFFF", 16))),
        ("read 0", ("read", 0, None)),
        ("help", ("help", None, None)),
        ("fullwrite 0xFFFFFFFF", ("fullwrite", None, int("0xFFFFFFFF", 16))),
        ("fullread", ("fullread", None, None)),
        ("exit", ("exit", None, None)),
    ]
)
def test_SHELL_VALIDATOR_검증(shellvalidator, input, output):
    assert shellvalidator.run(input) == output

@pytest.mark.parametrize(
    ("wrong_input"),
    [
        "write -1 0xFFFFFFFF",
        "write 0 0xFFGFFFFF",
        "write 0 0xFFGFFFFF 1",
        "read -1",
        "read 100",
        "read 0 1",
        "help 1",
        "fullwrite 0xFFFFFFGF",
        "fullwrite 0xFFFFFFFF 1",
        "fullread 1",
        "exit 1",
    ]
)
def test_SHELL_검증기_잘못된_VALUE_입력(wrong_input, shellvalidator):
    assert shellvalidator._validate_test(wrong_input) == False
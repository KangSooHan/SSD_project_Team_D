import pytest
from validator import SSDValidator, ShellValidator, Packet

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

@pytest.mark.parametrize("wrong_input", ["f 0", "f 0 0"])
def test_검증기_플러시_잘못된_입력_길이(wrong_input, ssdvalidator):
    assert ssdvalidator._validate_test(wrong_input) == False

def test_검증기_플러시_올바른_입력_성공(ssdvalidator):
    assert ssdvalidator._validate_test("F") == True

@pytest.mark.parametrize("wrong_input", ["e 0", "e 0 50 50"])
def test_검증기_지우기_잘못된_입력_길이(wrong_input, ssdvalidator):
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
    assert ssdvalidator.run(CORRECT_WRITE_SENTENCE) == Packet("W", 0, int("0xFFFFFFFF", 16))
    assert ssdvalidator.run(CORRECT_READ_SENTENCE) == Packet("R", 0, None)


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("write 0 0xFFFFFFFF", Packet("write", 0, int("0xFFFFFFFF", 16))),
        ("read 0", Packet("read", 0, None)),
        ("help", Packet("help", None, None)),
        ("fullwrite 0xFFFFFFFF", Packet("fullwrite", None, int("0xFFFFFFFF", 16))),
        ("fullread", Packet("fullread", None, None)),
        ("exit", Packet("exit", None, None)),
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


@pytest.mark.parametrize(
    ("input","expected_output"),
    [
        ("1_", "1_"),
        ("2_", "2_"),
        ("3_", "3_"),
        ("4_", "4_"),
        ("shell_scripts.txt", "Runner")
    ]
)
def test_SHELL_검증기_올바른_커맨드_입력(input, expected_output, shellvalidator):
    result = shellvalidator.run(input)
    assert result.COMMAND == expected_output


@pytest.mark.parametrize(
    ("wrong_input"),
    [
        "1_ extra_argument",
        "2_ extra_argument",
        "3_ extra_argument",
        "4_ extra_argument",
        "shell_scripts.txt extra_argument"
    ]
)
def test_SHELL_검증기_시나리오_잘못된_길이_입력(wrong_input, shellvalidator):
    result = shellvalidator.run(wrong_input)
    assert result.COMMAND == "ERR", f"입력 '{wrong_input}'는 ERR를 반환해야 합니다."

@pytest.mark.parametrize(
    "input_cmd, expected_command, expected_addr, expected_value",
    [
        # flush 정상 (길이 1)
        ("flush", "flush", None, None),
        # flush 오류 (길이 != 1)
        ("flush extra", "ERR", None, None),

        # erase 정상 (길이 3, 유효한 addr/size)
        ("erase 10 5", "erase", 10, 5),
        # erase 오류 (길이 != 3)
        ("erase 10", "ERR", None, None),
        ("erase 10 5 7", "ERR", None, None),
        # erase 오류 (addr invalid)
        ("erase abc 5", "ERR", None, None),
        # erase 오류 (size invalid)
        ("erase 10 xyz", "ERR", None, None),

        # erase_range 정상 (길이 3, valid start/end)
        ("erase_range 0 10", "erase_range", 0, 10),
        # erase_range 오류 (길이 != 3)
        ("erase_range 0", "ERR", None, None),
        ("erase_range 0 10 15", "ERR", None, None),
        # erase_range 오류 (start invalid)
        ("erase_range abc 10", "ERR", None, None),
        # erase_range 오류 (end invalid)
        ("erase_range 0 xyz", "ERR", None, None),
    ]
)
def test_SHELL_검증기_ERASE_ERASERANGE_FLUSH_검증(input_cmd, expected_command, expected_addr, expected_value, shellvalidator):
    packet = shellvalidator.run(input_cmd)

    assert packet.COMMAND == expected_command
    assert packet.ADDR == expected_addr
    assert packet.VALUE == expected_value

def test_SHELL_Validate_함수_빈_리스트_검증(shellvalidator):
    packet = shellvalidator._validate([])
    assert packet.COMMAND == "ERR"
    assert packet.ADDR is None
    assert packet.VALUE is None

def test_SSD_Validate_함수_빈_리스트_검증(ssdvalidator):
    packet = ssdvalidator._validate([])
    assert packet.COMMAND == "ERR"
    assert packet.ADDR is None
    assert packet.VALUE is None
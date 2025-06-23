import pytest

from utils import to_4byte_hex_str


@pytest.mark.parametrize("input_int, expected_str", [
    (0, "0x00000000"),
    (1, "0x00000001"),
    (2 ** 31 - 1, "0x7FFFFFFF")
])
def test_입력된정수를_16진수_문자열로_변환한다(input_int: int, expected_str: str):
    converted_str = to_4byte_hex_str(input_int)

    assert converted_str == expected_str

import pytest
from buffer_core.buffer import Buffer
from pytest_mock import MockFixture

@pytest.fixture
def buffer(mocker:MockFixture):
    buffer = mocker.Mock(spec=Buffer)
    return buffer

def test_Buffer_구현_성공():
    buffer_test = Buffer()
    assert True


def test_Buffer_insert_5보다_큰_입력(buffer):
    for i in range(10):
        buffer.insert(str(i))

    assert buffer.insert.call_count == 10

def test_Buffer_insert_5보다_작은_입력(buffer):
    for i in range(3):
        buffer.insert(str(i))

    assert buffer.insert.call_count == 3

def test_Buffer_flush_5보다_작은_입력(buffer):
    inputs = [str(i) for i in range(1, 4)]
    for input in inputs:
        buffer.insert(input)

    assert buffer._print() == inputs
    assert buffer.flush() == inputs

def test_Buffer_flush_5보다_큰_입력(buffer):
    inputs = [str(i) for i in range(1, 10)]
    for input in inputs:
        buffer.insert(input)

    # flush가 한 번 호출되었는지 확인
    buffer.flush.assert_called_once()

    # 출력 결과 검증
    assert buffer._print() == [str(i) for i in range(6, 10)]
import pytest
from buffer.buffer import Buffer

@pytest.fixture()
def buffer():
    return Buffer()

def test_Buffer_구현_성공():
    buffer_test = Buffer()
    assert True


def test_Buffer_5보다_큰_입력(buffer):
    for i in range(10):
        buffer.insert(str(i))

    assert buffer.len() == 5

def test_Buffer_5보다_작은_입력(buffer):
    for i in range(3):
        buffer.insert(str(i))

    assert buffer.len() == 3
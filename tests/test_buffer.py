import pytest
from validator import Packet
from ssd_core.normal_ssd import NormalSSD
from ssd_core.buffer import Buffer
from pytest_mock import MockerFixture

@pytest.fixture
def ssd(mocker: MockerFixture):
    mock = mocker.Mock(spec=NormalSSD)
    mock.write.return_value = None
    mock.erase.return_value = None
    return mock

def test_Buffer객체는_파라미터_없이_생성되어야_한다(ssd):
    buffer = Buffer(ssd)
    assert isinstance(buffer, Buffer)

def test_Buffer객체는_flush_명령으로_buffer를_비운다(ssd):
    buffer = Buffer(ssd)
    buffer.insert(Packet("W", 0, 0xABCD))

    assert len(buffer) == 1

    buffer.flush()

    assert len(buffer) == 0
    ssd.write.assert_called_once_with(0, 0xABCD)

def test_Buffer객체는_최적화대상이_아닌_명령에_대해_5개_항목을_유지한다(ssd, mocker:MockerFixture):
    buffer = Buffer(ssd)
    spy_optimize = mocker.spy(buffer, "optimize")
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 1, 0))
    buffer.insert(Packet("W", 2, 0))
    buffer.insert(Packet("W", 3, 0))
    buffer.insert(Packet("W", 4, 0))

    assert spy_optimize.call_count == 5
    assert len(buffer) == 0



def test_Buffer객체는_최적화_알고리즘_계산을위해_입력순서를_유지한다(ssd):
    buffer = Buffer(ssd)
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 1, 0))
    buffer.insert(Packet("W", 2, 0))
    buffer.insert(Packet("W", 3, 0))

    assert buffer._memory[0] == Packet("W", 0, 0)
    assert buffer._memory[1] == Packet("W", 1, 0)
    assert buffer._memory[2] == Packet("W", 2, 0)
    assert buffer._memory[3] == Packet("W", 3, 0)

"""
test cases for buffer optimization
"""
@pytest.mark.skip
def test_ignore_cmd_동일한_LBA에_대한_W_명령은_마지막_명령을_적용한다_1(ssd):
    buffer = Buffer(ssd)
    # 동일 위치에 다른 값을 write
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 1))

    buffer.optimize()

    assert len(buffer) == 1
    assert buffer.fast_read_from(0) == 1

@pytest.mark.skip
def test_ignore_cmd_동일한_LBA에_대한_W_명령은_마지막_명령을_적용한다_2(ssd):
    buffer = Buffer(ssd)

    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 1))

    buffer.optimize()

    assert len(buffer) == 1
    assert buffer.fast_read_from(0) == 1
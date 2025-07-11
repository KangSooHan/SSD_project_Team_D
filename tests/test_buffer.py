import pytest
from validator import Packet
from ssd_core.hardware.normal_ssd import NormalSSD
from ssd_core.command_buffer import CommandBuffer
from pytest_mock import MockerFixture

@pytest.fixture
def ssd(mocker: MockerFixture):
    mock = mocker.Mock(spec=NormalSSD)
    mock.write.return_value = None
    mock.erase.return_value = None
    return mock

def test_Buffer객체는_파라미터_없이_생성되어야_한다(ssd):
    buffer = CommandBuffer(ssd)
    buffer.clear()
    assert isinstance(buffer, CommandBuffer)

def test_Buffer객체는_flush_명령으로_buffer를_비운다(ssd):
    buffer = CommandBuffer(ssd)
    buffer.clear()
    buffer.insert(Packet("W", 0, 0xABCD))

    assert len(buffer) == 1

    buffer.flush()

    assert len(buffer) == 0
    ssd.write.assert_called_once_with(0, 0xABCD)

def test_Buffer객체는_최적화대상이_아닌_명령에_대해_5개_항목을_유지한다(ssd, mocker:MockerFixture):
    buffer = CommandBuffer(ssd)
    buffer.clear()
    spy_optimize = mocker.spy(buffer, "optimize")
    buffer.insert(Packet("W", 0, 1))
    buffer.insert(Packet("W", 1, 1))
    buffer.insert(Packet("W", 2, 1))
    buffer.insert(Packet("W", 3, 1))
    buffer.insert(Packet("W", 4, 1))
    buffer.insert(Packet("W", 5, 1))

    assert spy_optimize.call_count == 6
    assert len(buffer) == 1



def test_Buffer객체는_최적화_알고리즘_계산을위해_입력순서를_유지한다(ssd):
    buffer = CommandBuffer(ssd)
    buffer.clear()

    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 1, 1))
    buffer.insert(Packet("W", 2, 2))
    buffer.insert(Packet("W", 3, 3))

    assert buffer._memory[0] == Packet("W", 0, 0)
    assert buffer._memory[1] == Packet("W", 1, 1)
    assert buffer._memory[2] == Packet("W", 2, 2)
    assert buffer._memory[3] == Packet("W", 3, 3)

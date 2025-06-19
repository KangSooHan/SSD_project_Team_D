import pytest

from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer
from ssd_core.simple_buffer_optimizer import SimpleBufferOptimizer
from validator import Packet


# 실제 구현체로 교체 필요
class FakeBuffer:
    def __init__(self, optimizer: AbstractBufferOptimizer):
        self.memory: list[Packet] = []
        self._optimizer = optimizer

    def insert(self, packet: Packet):
        self.memory.append(packet)

    def len(self):
        return len(self.memory)

    def flush(self):
        ret = self.memory.copy()
        self.memory = []
        return ret

    def _print(self):
        return self.memory

    def optimize(self):
        self.memory = self._optimizer.calculate(self.memory)

    def fast_read_from(self, lba: int) -> int:
        pass


@pytest.fixture
def buffer():
    return FakeBuffer(SimpleBufferOptimizer())


def test_Buffer객체_초기_길이값은_0이다(buffer):
    assert buffer.len() == 0


def test_Buffer객체는_flush_명령으로_buffer를_비운다(buffer):
    buffer.insert(Packet("W", 0, 0))

    assert buffer.len() == 1

    buffer.flush()

    assert buffer.len() == 0


def test_Buffer객체는_최적화대상이_아닌_명령에_대해_5개_항목을_유지한다(buffer):
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 1, 0))
    buffer.insert(Packet("W", 2, 0))
    buffer.insert(Packet("W", 3, 0))
    buffer.insert(Packet("W", 4, 0))

    assert buffer.len() == 5


def test_Buffer객체는_최적화_알고리즘_계산을위해_입력순서를_유지한다(buffer):
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 1, 0))
    buffer.insert(Packet("W", 2, 0))
    buffer.insert(Packet("W", 3, 0))
    buffer.insert(Packet("W", 4, 0))

    assert buffer.memory[0] == Packet("W", 0, 0)
    assert buffer.memory[1] == Packet("W", 1, 0)
    assert buffer.memory[2] == Packet("W", 2, 0)
    assert buffer.memory[3] == Packet("W", 3, 0)
    assert buffer.memory[4] == Packet("W", 4, 0)


"""
test cases for buffer optimization
"""


@pytest.mark.skip
def test_ignore_cmd_동일한_LBA에_대한_W_명령은_마지막_명령을_적용한다_1(buffer):
    # 동일 위치에 다른 값을 write
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 1))

    buffer.optimize()

    assert buffer.len() == 1
    assert buffer.fast_read_from(0) == 1


@pytest.mark.skip
def test_ignore_cmd_동일한_LBA에_대한_W_명령은_마지막_명령을_적용한다_2(buffer):
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 0))
    buffer.insert(Packet("W", 0, 1))

    buffer.optimize()

    assert buffer.len() == 1
    assert buffer.fast_read_from(0) == 1

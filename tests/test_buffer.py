import pytest

# 실제 구현체로 교체 필요
class Buffer:
    def __init__(self):
        self.memory = []

    def insert(self, value: str):
        self.memory.append(value)
        if self.len() == 5:
            self.flush()

    def len(self):
        return len(self.memory)

    def flush(self):
        ret = self.memory.copy()
        self.memory = []
        return ret

    def _print(self):
        return self.memory


@pytest.fixture
def buffer():
    return Buffer()


def test_Buffer객체는_파라미터_없이_생성되어야_한다():
    buffer = Buffer()
    assert True


def test_Buffer객체_초기_길이값은_0이다(buffer):
    assert buffer.len == 0


def test_Buffer객체는_W_명령을_개별_인자로_분리한다(buffer):
    # W [LBA] [VALUE]
    buffer.insert("W 0 0x00000000")

    assert buffer.len == 1
    assert len(buffer.memory[0]) == 3  # (CMD, LBA, VALUE)
    assert type(buffer.memory[0][0]) == str
    assert type(buffer.memory[0][1]) == int
    assert type(buffer.memory[0][2]) == int


def test_Buffer객체는_E_명령을_개별_인자로_분리한다(buffer):
    # E [LBA] [SIZE]
    buffer.insert("E 0 10")

    assert buffer.len == 1
    assert len(buffer.memory[0]) == 3  # (CMD, LBA, SIZE)
    assert type(buffer.memory[0][0]) == str
    assert type(buffer.memory[0][1]) == int
    assert type(buffer.memory[0][2]) == int


def test_Buffer객체는_R_명령을_저장하지_않는다(buffer):
    # R [LBA]
    buffer.insert("R 0")

    assert buffer.len == 0


def test_Buffer객체는_flush_명령으로_buffer를_비운다(buffer):
    buffer.insert("W 0 0x00000000")
    buffer.flush()

    assert buffer.len == 0


def test_Buffer객체는_최적화대상이_아닌_명령에_대해_5개_항목을_유지한다(buffer):
    buffer.insert("W 0 0x00000000")
    buffer.insert("W 1 0x00000000")
    buffer.insert("W 2 0x00000000")
    buffer.insert("W 3 0x00000000")
    buffer.insert("W 4 0x00000000")

    assert buffer.len == 5

def test_Buffer객체는_최적화대상이_아닌_명령이_5개를초과하면_flush를_수행한다(buffer):
    buffer.insert("W 0 0x00000000")
    buffer.insert("W 1 0x00000000")
    buffer.insert("W 2 0x00000000")
    buffer.insert("W 3 0x00000000")
    buffer.insert("W 4 0x00000000")
    # flush
    buffer.insert("W 5 0x00000000")

    assert buffer.len == 1

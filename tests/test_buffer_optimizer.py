import sys, os, pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssd_core.simple_buffer_optimizer import SimpleBufferOptimizer
from validator import Packet


@pytest.mark.parametrize("buf_in, expected", [

    # 1. 중복 Write 제거
    ([Packet("W", 10, 0xA), Packet("W", 10, 0xB)],
     [Packet("W", 10, 0xB)]),

    # 2. 여러 중복 Write 제거
    ([Packet("W", 5, 0x1), Packet("W", 5, 0x2), Packet("W", 5, 0x3)],
     [Packet("W", 5, 0x3)]),

    # 3. Erase가 Write 무효화
    ([Packet("W", 20, 0xAAA), Packet("E", 19, SIZE=2)],
     [Packet("E", 19, SIZE=2)]),

    # 4. Erase가 Write에 영향 없음
    ([Packet("W", 20, 0xAAA), Packet("E", 10, SIZE=5)],
     [Packet("W", 20, 0xAAA), Packet("E", 10, SIZE=5)]),

    # 5. Erase 병합 (연속 영역)
    ([Packet("E", 30, SIZE=5), Packet("E", 35, SIZE=3)],
     [Packet("E", 30, SIZE=8)]),

    # 6. Erase 병합 불가 (간격 존재)
    ([Packet("E", 30, SIZE=3), Packet("E", 40, SIZE=2)],
     [Packet("E", 30, SIZE=3), Packet("E", 40, SIZE=2)]),

    # 7. 병합은 가능하나 size > 10
    ([Packet("E", 10, SIZE=6), Packet("E", 16, SIZE=6)],
     [Packet("E", 10, SIZE=6), Packet("E", 16, SIZE=6)]),

    # 8. 중복 W 제거 + Erase로 W 제거 + Erase 병합
    ([Packet("W", 1, 0x111), Packet("W", 1, 0x222), Packet("E", 0, SIZE=2), Packet("E", 2, SIZE=2)],
     [Packet("E", 0, SIZE=4)]),

    # ✅ 9. Write가 Erase 범위 밖 → 유지 (결과 순서 수정됨)
    ([Packet("E", 90, SIZE=5), Packet("W", 80, 0x1)],
     [Packet("E", 90, SIZE=5), Packet("W", 80, 0x1)]),

    # 10. 모든 Write 무효화됨
    ([Packet("W", 1, 0x1), Packet("W", 1, 0x2), Packet("E", 0, SIZE=5)],
     [Packet("E", 0, SIZE=5)]),
])
def test_buffer_optimizer(buf_in, expected):
    optimizer = SimpleBufferOptimizer()
    result = optimizer.calculate(buf_in)

    assert len(result) == len(expected), f"Expected {len(expected)} packets, got {len(result)}"
    for r, e in zip(result, expected):
        assert r.COMMAND == e.COMMAND
        assert r.ADDR == e.ADDR
        assert r.VALUE == e.VALUE
        assert r.SIZE == e.SIZE

import pytest

from ssd_core.discovery_buffer_optimizer import DiscoveryBufferOptimizer
from validator import Packet

@pytest.fixture
def discovery_optimizer():
    return DiscoveryBufferOptimizer()

@pytest.fixture
def abstract_buffer_optimizer():
    return DiscoveryBufferOptimizer()

def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_1(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1)
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_2(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=0, SIZE=1)
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_3(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=0, SIZE=2)
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_4(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=3, SIZE=2)
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_5(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_6(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
        Packet(COMMAND="E", ADDR=12, SIZE=5),
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_7(discovery_optimizer):
    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
        Packet(COMMAND="E", ADDR=12, SIZE=5),
        Packet(COMMAND="E", ADDR=95, SIZE=5),
    ]

    erase_lst = discovery_optimizer.project_erase(tc)
    assert erase_lst == [
        1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
    ]


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_1(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_2(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=0, VALUE=1),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_3(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_4(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_5(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_6(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=10, SIZE=10),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_7(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=10, SIZE=10),
        Packet(COMMAND="W", ADDR=10, VALUE=1),
    ]

    erase_lst, _ = discovery_optimizer.project_write(tc)
    assert erase_lst == [
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]


def test_W_명령값이_0_인경우_E명령으로_대체한다_1(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=3, VALUE=0),
    ]

    result = discovery_optimizer.replace_zero_write(tc)

    assert len(result) == 1
    assert result[0].COMMAND == "E"
    assert result[0].ADDR == 3
    assert result[0].SIZE == 1


def test_W_명령값이_0_인경우_E명령으로_대체한다_2(discovery_optimizer):
    tc = [
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="W", ADDR=3, VALUE=0),
        Packet(COMMAND="W", ADDR=2, VALUE=2),
    ]

    result = discovery_optimizer.replace_zero_write(tc)

    assert len(result) == 3
    assert result[0] == tc[0]
    assert result[2] == tc[2]

    assert result[1].COMMAND == "E"
    assert result[1].ADDR == 3
    assert result[1].SIZE == 1

"""
AbstractBufferOptimizer 구현체에 대한 테스트 코드
"""
@pytest.mark.parametrize("tc", [
    [],
    [Packet(COMMAND="W", ADDR=0, VALUE=1)],
    [Packet(COMMAND="E", ADDR=0, VALUE=1)],
])
def test_명령어가_1개이하인경우_최적화하지_않는다(abstract_buffer_optimizer, tc):
    result = abstract_buffer_optimizer.calculate(tc)

    assert result == tc


@pytest.mark.parametrize("tc, expected_cmd", [
    #1. 중복 erase 제거
    [
        [Packet(COMMAND="E", ADDR=0, SIZE=5), Packet(COMMAND="E", ADDR=0, SIZE=5)],
        [Packet(COMMAND="E", ADDR=0, SIZE=5)]
    ],
    [
        [Packet(COMMAND="E", ADDR=10, SIZE=5), Packet(COMMAND="E", ADDR=10, SIZE=2)],
        [Packet(COMMAND="E", ADDR=10, SIZE=5)]
    ],

    # 2. 중첩, 연속 erase merge (총 길이 10 이하)
    [
        [Packet(COMMAND="E", ADDR=0, SIZE=5), Packet(COMMAND="E", ADDR=5, SIZE=5)],
        [Packet(COMMAND="E", ADDR=0, SIZE=10)]
    ],
    [
        [Packet(COMMAND="E", ADDR=10, SIZE=5), Packet(COMMAND="E", ADDR=10, SIZE=7)],
        [Packet(COMMAND="E", ADDR=10, SIZE=7)]
    ],
    [
        [Packet(COMMAND="E", ADDR=10, SIZE=5), Packet(COMMAND="E", ADDR=10, SIZE=7), Packet(COMMAND="E", ADDR=12, SIZE=3)],
        [Packet(COMMAND="E", ADDR=10, SIZE=7)]
    ],

    # 3. 중첩, 연속 erase merge (총 길이 10 이상)
    [
        [Packet(COMMAND="E", ADDR=0, SIZE=7), Packet(COMMAND="E", ADDR=7, SIZE=7), Packet(COMMAND="E", ADDR=14, SIZE=6)],
        [Packet(COMMAND="E", ADDR=0, SIZE=10), Packet(COMMAND="E", ADDR=10, SIZE=10)]
    ],

    # 4. erase에 의해 overwrite 되는 write 명령 제거
    [
        [Packet(COMMAND="W", ADDR=1, VALUE=0x1), Packet(COMMAND="W", ADDR=3, VALUE=0x3), Packet(COMMAND="W", ADDR=5, VALUE=0x5),
         Packet(COMMAND="E", ADDR=0, SIZE=10)],
        [Packet(COMMAND="E", ADDR=0, SIZE=10)]
    ],

    # 5. erase가 write 보다 먼저 수행되는 경우 write 명령 유지
    [
        [Packet(COMMAND="E", ADDR=0, SIZE=10),
        Packet(COMMAND="W", ADDR=1, VALUE=0x1), Packet(COMMAND="W", ADDR=3, VALUE=0x3), Packet(COMMAND="W", ADDR=5, VALUE=0x5)],
        [Packet(COMMAND="E", ADDR=0, SIZE=10),
         Packet(COMMAND="W", ADDR=1, VALUE=0x1), Packet(COMMAND="W", ADDR=3, VALUE=0x3), Packet(COMMAND="W", ADDR=5, VALUE=0x5)]
    ],

    # 6. write로 덮어지는 영역이 2개 이상의 erase 영역을 접합하는 경우
    [
        [Packet(COMMAND="E", ADDR=0, SIZE=2), Packet(COMMAND="E", ADDR=3, SIZE=2), Packet(COMMAND="E", ADDR=6, SIZE=2),
        Packet(COMMAND="W", ADDR=2, VALUE=0x2), Packet(COMMAND="W", ADDR=5, VALUE=0x5)],
        [Packet(COMMAND="E", ADDR=0, SIZE=8),
         Packet(COMMAND="W", ADDR=2, VALUE=0x2), Packet(COMMAND="W", ADDR=5, VALUE=0x5)]
    ],

    # tc from SimpleBufferOptimizer
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

    # 101. erase 2개를 write 3개가 연결, write/erase 1개 겹침
    ([Packet("E", 0, SIZE=5), Packet("E", 7, SIZE=2), Packet("W", 5, 0x5), Packet("W", 6, 0x6), Packet("W", 7, 0x7)],
     [Packet("E", 0, SIZE=9), Packet("W", 5, 0x5), Packet("W", 6, 0x6), Packet("W", 7, 0x7)]),

    # 102. erase 2개를 write 3개가 연결, write/erase 겹치지 않음
    ([Packet("E", 0, SIZE=5), Packet("E", 8, SIZE=2), Packet("W", 5, 0x5), Packet("W", 6, 0x6), Packet("W", 7, 0x7)],
     [Packet("E", 0, SIZE=10), Packet("W", 5, 0x5), Packet("W", 6, 0x6), Packet("W", 7, 0x7)]),

    # 103. erase 2개를 write 3개가 연결하지만 erase 10개 초과로 연결하지 못함
    ([Packet("E", 0, SIZE=8), Packet("E", 11, SIZE=4), Packet("W", 8, 0x8), Packet("W", 9, 0x9), Packet("W", 10, 0x10)],
     [Packet("E", 0, SIZE=8), Packet("E", 11, SIZE=4), Packet("W", 8, 0x8), Packet("W", 9, 0x9), Packet("W", 10, 0x10)]),

    # 104. erase 명령이 배열 범위 끝에서 수행되는지 확인
    ([Packet("E", 99, SIZE=1), Packet("E", 98, SIZE=2), Packet("E", 97, SIZE=3),],
     [Packet("E", 97, SIZE=3)]),
])
def test_buffer_최적화_반환_커맨드_동일_케이스_검증(abstract_buffer_optimizer, tc, expected_cmd):
    result = abstract_buffer_optimizer.calculate(tc)
    assert result == expected_cmd


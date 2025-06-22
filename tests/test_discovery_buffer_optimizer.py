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

    # 5. erase가 write 보다 먼저 수행되는 경우 wirte 명령 유지
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
])
def test_buffer_최적화_반환_커맨드_동일_케이스_검증(abstract_buffer_optimizer, tc, expected_cmd):
    result = abstract_buffer_optimizer.calculate(tc)
    assert result == expected_cmd

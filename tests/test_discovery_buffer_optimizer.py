import pytest

from ssd_core.discovery_buffer_optimizer import DiscoveryBufferOptimizer
from validator import Packet


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_1():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1)
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_2():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=0, SIZE=1)
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_3():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=0, SIZE=2)
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_4():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=3, SIZE=2)
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_5():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_6():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
        Packet(COMMAND="E", ADDR=12, SIZE=5),
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Erase영역에_해당하는_주소를_1로_마킹해서_리턴한다_7():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="E", ADDR=0, SIZE=1),
        Packet(COMMAND="E", ADDR=4, SIZE=5),
        Packet(COMMAND="E", ADDR=10, SIZE=5),
        Packet(COMMAND="E", ADDR=12, SIZE=5),
        Packet(COMMAND="E", ADDR=95, SIZE=5),
    ]

    erase_lst = algo.project_erase(tc)
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


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_1():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
    ]

    erase_lst = algo.project_write(tc)
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

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_2():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=0, VALUE=1),
    ]

    erase_lst = algo.project_write(tc)
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


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_3():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
    ]

    erase_lst = algo.project_write(tc)
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


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_4():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
    ]

    erase_lst = algo.project_write(tc)
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

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_5():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
    ]

    erase_lst = algo.project_write(tc)
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


def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_6():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=10, SIZE=10),
    ]

    erase_lst = algo.project_write(tc)
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

def test_Write영역에_해당하는_주소를_1로_마킹해서_리턴한다_7():
    algo = DiscoveryBufferOptimizer()

    tc = [
        Packet(COMMAND="W", ADDR=0, VALUE=1),
        Packet(COMMAND="E", ADDR=1, SIZE=2),
        Packet(COMMAND="W", ADDR=1, VALUE=1),
        Packet(COMMAND="E", ADDR=10, SIZE=10),
        Packet(COMMAND="W", ADDR=10, VALUE=1),
    ]

    erase_lst = algo.project_write(tc)
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
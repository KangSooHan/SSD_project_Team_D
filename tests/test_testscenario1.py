import io
import sys

import pytest
from pytest_mock import MockerFixture

from command_core.shell_commands.testscenario import TestScenario1
from ssd_core.abstract_ssd import AbstractSSD
from utils import to_4byte_hex_str


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=AbstractSSD)
    #mock.read.return_value = f"0x{1:08X}"
    mock.read.return_value = to_4byte_hex_str(1)
    return mock


def test_테스트시나리오1_객체를_생성한다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    assert True


def test_테스트시나리오1_객체는_SSD_인터페이스를_의존성으로_주입받는다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    assert True


def test_테스트시나리오1_객체는_execute_메서드로_시나리오를_실행한다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    sut.execute()
    assert True


def test_read_compare_기능은_정상적으로_읽은_경우_true를_리턴한다(ssd_mock):
    sut = TestScenario1(ssd_mock)

    assert sut.read_compare(0x00, 1) == True


def test_read_compare_기능은_읽기에_실패한_경우_false를_반환한다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    ssd_mock.read.return_value = hex(1)

    assert sut.read_compare(0x00, hex(2)) == False


def test_전체시나리오에_실패할경우_FAIL값을_출력한다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    output = io.StringIO()
    sys.stdout = output

    sut.execute()
    assert output.getvalue() == "FAIL\n"


def test_전체시나리오에_성공할경우_PASS값을_출력한다(ssd_mock):
    sut = TestScenario1(ssd_mock)
    #ssd_mock.read.side_effect = [f'0x{value:08X}' for value in range(100)]
    ssd_mock.read.side_effect = [to_4byte_hex_str(value) for value in range(100)]
    output = io.StringIO()
    sys.stdout = output

    sut.execute()
    assert output.getvalue() == "PASS\n"

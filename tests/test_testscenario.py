from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell.commands.testscenario1 import TestScenario1
from ssd import ssd
from ssd.abstract_ssd import AbstractSSD

@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    return mocker.Mock(spe=AbstractSSD)

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

def test_테스트시나리오1_객체는_0에서_4번지까지_write명령을_실행한다(ssd_mock):
    sut = TestScenario1(ssd_mock)

    sut.execute()

    assert ssd_mock.write.call_count == 4
    ssd_mock.write.assert_has_calls([
        call(0x00, hex(0)),
        call(0x01, hex(1)),
        call(0x02, hex(2)),
        call(0x03, hex(3)),
    ])
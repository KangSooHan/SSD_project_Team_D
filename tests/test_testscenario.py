import pytest
from pytest_mock import MockerFixture

from shell.commands.testscenario1 import TestScenario1
from ssd import ssd
from ssd.abstract_ssd import AbstractSSD


def test_테스트시나리오1_객체를_생성한다(mocker: MockerFixture):
    sdd_mock = mocker.Mock(spec=AbstractSSD)
    sut = TestScenario1(sdd_mock)
    assert True

def test_테스트시나리오1_객체는_SSD_인터페이스를_의존성으로_주입받는다(mocker: MockerFixture):
    sdd_mock = mocker.Mock(spec=AbstractSSD)
    sut = TestScenario1(sdd_mock)
    assert True

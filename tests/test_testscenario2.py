from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell.commands.testscenario2 import TestScenario2
from ssd import ssd
from ssd.abstract_ssd import AbstractSSD


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    return mocker.Mock(spec=AbstractSSD)


def test_전체시나리오에_실패할경우_FAIL값을_리턴한다(ssd_mock):
    sut = TestScenario2(ssd_mock)
    assert sut.execute() == "FAIL"


def test_전체시나리오에_성공할경우_PASS값을_리턴한다(ssd_mock):
    sut = TestScenario2(ssd_mock)
    ssd_mock.read.return_value = sut.test_constant
    assert sut.execute() == "PASS"

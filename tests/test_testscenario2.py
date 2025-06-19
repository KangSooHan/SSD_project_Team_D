import io
import sys
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell_core.commands.testscenario2 import TestScenario2
from ssd_core.abstract_ssd import AbstractSSD


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=AbstractSSD)
    mock.read_from.return_value = f"0x{1:08X}"
    return mock


def test_전체시나리오에_실패할경우_FAIL값을_출력한다(mocker: MockerFixture):
    ssd_mock = mocker.Mock(spec=AbstractSSD)
    sut = TestScenario2(ssd_mock)
    output = io.StringIO()
    sys.stdout = output

    sut.execute()
    assert output.getvalue() == "FAIL\n"


def test_전체시나리오에_성공할경우_PASS값을_출력한다(ssd_mock):
    sut = TestScenario2(ssd_mock)
    output = io.StringIO()
    sys.stdout = output

    sut.execute()
    assert output.getvalue() == "PASS\n"

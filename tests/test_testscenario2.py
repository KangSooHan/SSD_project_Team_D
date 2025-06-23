import io
import sys

import pytest
from pytest_mock import MockerFixture

from command_core.shell_commands.testscenario import TestScenario2
from ssd_core.abstract_ssd import AbstractSSD
from utils import to_4byte_hex_str


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=AbstractSSD)
    mock.read.return_value = to_4byte_hex_str(1)
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

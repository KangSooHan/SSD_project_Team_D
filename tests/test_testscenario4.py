import io
import sys

import pytest
from pytest_mock import MockerFixture

from command_core.shell_commands.testscenario import TestScenario4
from ssd_core.abstract_ssd import AbstractSSD


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=AbstractSSD)
    mock.read.return_value = f"0x{1:08X}"
    return mock


def test_테스트시나리오4_객체를_생성한다(ssd_mock):
    sut = TestScenario4(ssd_mock)
    assert True

import io
import random
import sys
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell_core.commands.testscenario3 import TestScenario3
from shell_core.commands.write_command import WriteCommand
from ssd_core.abstract_ssd import AbstractSSD


@pytest.fixture
def ssd_mock(mocker: MockerFixture):
    return mocker.Mock(spec=AbstractSSD)


def test_전체시나리오에_실패할경우_FAIL값을_출력한다(ssd_mock):
    sut = TestScenario3(ssd_mock)
    output = io.StringIO()
    sys.stdout = output

    sut.execute()
    assert output.getvalue() == "FAIL\n"


def test_전체시나리오에_성공할경우_PASS값을_출력한다(ssd_mock):
    sut = TestScenario3(ssd_mock)
    output = io.StringIO()
    sys.stdout = output

    random.seed(0)
    ssd_mock.read.side_effect = [f'0x{random.randint(1, 10):08X}' for i in range(200 * 2)]

    # sut.execute() 실행 시 동일한 시퀀스의 랜덤값을 추출하기 위해 시드 초기화
    random.seed(0)

    sut.execute()
    assert output.getvalue() == "PASS\n"

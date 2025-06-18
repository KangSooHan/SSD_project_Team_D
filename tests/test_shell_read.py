import pytest
from ssd_core.abstract_ssd import AbstractSSD
from ssd_core.normal_ssd import NormalSSD
from shell_core.commands.read_command import ReadCommand


@pytest.mark.parametrize("lba", [1, 2, 3, 4, 99])
def test_read_성공(mocker, lba):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd)

    # act
    read_cmd.execute(lba)

    # assert
    assert ssd.read.call_count == 1


@pytest.mark.parametrize("lba", [-1, 100])
def test_read_실패(mocker, lba):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        read_cmd.execute(lba)


@pytest.mark.parametrize("lba", [1, 2, 3, 4, 99])
def test_read_올바른값_성공(mocker, lba):
    # arrange
    ssd: NormalSSD = mocker.Mock()
    ssd.read.return_value = 0xABABABAB

    read_cmd = ReadCommand(ssd)

    # act
    result = read_cmd.execute(lba)

    # assert
    assert result == 0xABABABAB


@pytest.mark.parametrize("lba", [-1, 100, 2000])
def test_read_잘못된범위_실패(mocker, lba):
    # arrange
    ssd: NormalSSD = mocker.Mock()

    read_cmd = ReadCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        read_cmd.execute(lba)


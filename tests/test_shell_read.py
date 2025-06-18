import pytest
from ssd_core.abstract_ssd import AbstractSSD
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

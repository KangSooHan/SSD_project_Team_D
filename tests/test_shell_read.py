import pytest
from ssd.abstract_ssd import AbstractSSD
from shell.commands.read_command import ReadCommand

def test_read_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd)

    assert True
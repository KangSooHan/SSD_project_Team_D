import pytest
from ssd.abstract_ssd import AbstractSSD
from shell.commands.write_command import WriteCommand

def test_write_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act
    write_cmd.execute(3, 0xAAAABBBB)

    # assert
    assert ssd.write.call_count == 1

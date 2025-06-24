import pytest
from ssd_core.hardware.abstract_ssd import AbstractSSD
from command_core.shell_commands.flush_command import FlushCommand


def test_erase_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    flush_cmd = FlushCommand(ssd)

    # act
    flush_cmd.execute()

    # assert
    assert ssd.flush.call_count == 1

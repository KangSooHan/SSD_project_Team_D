import pytest
from ssd_core.hardware.abstract_ssd import AbstractSSD
from command_core.shell_commands.full_write_command import FullWriteCommand

@pytest.mark.parametrize("value", [0xAAAABBBB, 0x11111111])
def test_full_write_성공(mocker, value):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    full_write_cmd = FullWriteCommand(ssd, value)

    # act
    full_write_cmd.execute()

    # assert
    assert ssd.write.call_count == 100


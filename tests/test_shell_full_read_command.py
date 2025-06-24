from command_core.shell_commands.full_read_command import FullReadCommand
from ssd_core.hardware.abstract_ssd import AbstractSSD
#from shell_core.shell_commands.full_read_command import FullReadCommand

def test_full_read_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    full_read_cmd = FullReadCommand(ssd)

    # act
    full_read_cmd.execute()

    # assert
    assert ssd.read.call_count == 100

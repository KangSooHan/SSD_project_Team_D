import pytest
from ssd_core.abstract_ssd import AbstractSSD
#from shell_core.commands.full_read_command import FullReadCommand

@pytest.mark.skip
def test_full_read_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    full_read_cmd = FullReadCommand(ssd)

    # act
    full_read_cmd.execute()

    # assert
    assert ssd.read.call_count == 100

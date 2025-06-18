import pytest
from ssd_core.abstract_ssd import AbstractSSD
from shell.commands.write_command import WriteCommand

def test_write_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act
    write_cmd.execute(3, int(0xAAAABBBB))

    # assert
    assert ssd.write.call_count == 1

def test_write_실패_LBA범위초과(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute(100, int(0xAAAABBBB))


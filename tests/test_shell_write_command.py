import pytest
from ssd_core.hardware.abstract_ssd import AbstractSSD
from command_core.shell_commands.write_command import WriteCommand


def test_write_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd, 3, int(0xAAAABBBB))

    # act
    write_cmd.execute()

    # assert
    assert ssd.write.call_count == 1


def test_write_실패_LBA범위초과(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd, 100, int(0xAAAABBBB))

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute()

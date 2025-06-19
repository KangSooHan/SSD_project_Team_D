import pytest
from shell_core.normal_ssd_driver import NormalSSDDriver
from command_core.shell_commands.write_command import WriteCommand
from command_core.shell_commands.read_command import ReadCommand


@pytest.mark.parametrize("write_lba, data", [
    (0, "0x11111111"),
    (99, "0x22222222")])
def test_normal_ssd_driver_쓰기성공(mocker, write_lba, data):
    # arrange
    ssd: NormalSSDDriver = mocker.Mock()
    write_cmd = WriteCommand(ssd, write_lba, data)

    write_cmd.execute()
    assert ssd.write.call_count == 1


@pytest.mark.parametrize("read_lba", [0, 99])
def test_normal_ssd_driver_읽기성공(mocker, read_lba):
    # arrange
    ssd: NormalSSDDriver = mocker.Mock()
    read_cmd = ReadCommand(ssd, read_lba)

    read_cmd.execute()
    assert ssd.read.call_count == 1

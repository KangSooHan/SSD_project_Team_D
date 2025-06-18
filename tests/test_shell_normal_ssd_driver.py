import os
import pytest
from shell.normal_ssd_driver import NormalSSDDriver
from shell.commands.write_command import WriteCommand

@pytest.mark.parametrize("write_lba, data", [
    (0, "0x11111111"),
    (99, "0x22222222")])
def test_normal_ssd_driver_write_성공(mocker, write_lba, data):
    # arrange
    ssd: NormalSSDDriver = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    write_cmd.execute(write_lba, data)

    assert ssd.write.call_count == 1

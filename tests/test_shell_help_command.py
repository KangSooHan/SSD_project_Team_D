import pytest
from ssd.abstract_ssd import AbstractSSD
from shell.commands.help_command import HelpCommand

def test_help_객체생성(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    help_cmd = HelpCommand(ssd)

    # act & assert
    assert help_cmd.execute() == True
    assert ssd.write.call_count == 1

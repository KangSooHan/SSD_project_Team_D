import pytest
from ssd.abstract_ssd import AbstractSSD
from shell.commands.help_command import HelpCommand

def test_help_객체생성(mocker):
    # arrange
    help_cmd: HelpCommand = mocker.Mock()

    # act
    help_cmd.execute()

    # assert
    assert help_cmd.execute.call_count == 1

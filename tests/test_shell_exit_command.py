import pytest
from shell.commands.exit_command import ExitCommand


def test_exit_성공():
    # arrange
    exit_cmd = ExitCommand()

    # act & assert
    with pytest.raises(SystemExit) as e:
        exit_cmd.execute()
    assert e.value.code == 0

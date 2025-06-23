import pytest
from shell_core.normal_ssd_driver import NormalSSDDriver
from command_core.shell_commands.runner import Runner


def test_runner_성공():
    # arrange
    ssd = NormalSSDDriver()
    runner = Runner(ssd)

    # act
    with pytest.raises(SystemExit) as exc_info:
        runner.execute()

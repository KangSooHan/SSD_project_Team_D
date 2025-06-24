import pytest
from adapter.ssd_shell_adapter import SSDShellAdapter
from command_core.shell_commands.runner import Runner


def test_runner_성공():
    # arrange
    ssd = SSDShellAdapter()
    runner = Runner(ssd)

    # act
    with pytest.raises(SystemExit) as exc_info:
        runner.execute()

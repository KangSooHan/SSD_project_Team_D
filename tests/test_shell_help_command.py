import io
import sys
import textwrap

import pytest
from shell_core.commands.help_command import HelpCommand


def test_help명령어():
    # arrange
    help_cmd = HelpCommand()
    output = io.StringIO()
    sys.stdout = output

    # act
    help_cmd.execute()

    # assert
    assert "팀명: Discovery | 팀원: 강수한, 이후광, 윤창흠, 김지영, 이지훈, 박치원" in output.getvalue()
    cmd_msg = textwrap.dedent('''
    - write : write {LBA} {VALUE}
    - read : read {LBA}
    - exit : exit
    - help : help
    - fullwrite : fullwrite {VALUE}
    - fullread : fullread
    ''').strip()
    assert cmd_msg in output.getvalue()

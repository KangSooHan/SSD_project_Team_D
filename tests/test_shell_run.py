import io
import pytest
from unittest.mock import MagicMock, patch
from contextlib import redirect_stdout

from shell import run


@pytest.fixture
def mock_ssd():
    return MagicMock()


@pytest.fixture
def mock_validator():
    return MagicMock()


@pytest.mark.parametrize("user_input, mock_return, expected_output", [
    ("read 1", ("read", 1, None), "[Read]"),
    ("write 2 0xABCD1234", ("write", 2, "0xABCD1234"), "[Write]"),
    ("help", ("help", None, None), "[Help]"),
    ("exit", ("exit", None, None), ""),  # SystemExit expected
    ("fullread", ("fullread", None, None), "[FullRead]"),
    ("fullwrite 0xFFFFFFFF", ("fullwrite", None, "0xFFFFFFFF"), "[FullWrite]"),
    ("1_", ("1_", None, None), "[FullWriteAndReadCompare]"),
    ("2_", ("2_", None, None), "[PartialLBAWrite]"),
    ("3_", ("3_", None, None), "[WriteReadAging]"),
    ("invalidcmd", (False, None, None), "INVALID COMMAND"),
])
def test_shell_run(user_input, mock_return, expected_output, mock_ssd, mock_validator):
    mock_validator.run.return_value = mock_return

    # 명령어 출력 시뮬레이션
    print_map = {
        "read": "[Read]",
        "write": "[Write]",
        "help": "[Help]",
        "fullread": "[FullRead]",
        "fullwrite": "[FullWrite]",
        "1_": "[FullWriteAndReadCompare]",
        "2_": "[PartialLBAWrite]",
        "3_": "[WriteReadAging]",
    }

    command = mock_return[0]
    mock_command = MagicMock()

    if command in print_map:
        mock_command.execute.side_effect = lambda: print(print_map[command])
    elif command == "exit":
        mock_command.execute.side_effect = lambda: (_ for _ in ()).throw(SystemExit)
    else:
        mock_command.execute.return_value = None

    with patch("shell_core.command_factory.CommandFactory.create", return_value=mock_command):
        f = io.StringIO()
        if command == "exit":
            with pytest.raises(SystemExit):
                with redirect_stdout(f):
                    run(user_input, mock_ssd, mock_validator)
        else:
            with redirect_stdout(f):
                run(user_input, mock_ssd, mock_validator)
            output = f.getvalue()
            assert expected_output in output

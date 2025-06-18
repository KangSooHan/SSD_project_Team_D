import io
import pytest
from contextlib import redirect_stdout

from shell import run
from shell_core.normal_ssd_driver import NormalSSDDriver
from validator import Validator

@pytest.mark.parametrize("user_input, expected_output_contains", [
    ("read 1", "[Read]"),
    ("write 2 0xABCD1234", "[Write]"),
    ("help", "[Help]"),
    ("exit", ""),  # SystemExit 예외가 발생하므로 별도 처리
    ("fullread", "[FullRead]"),
    ("fullwrite 0xFFFFFFFF", "[FullWrite]"),
    ("1_", "[FullWriteAndReadCompare]"),
    ("2_", "[PartialLBAWrite]"),
    ("3_", "[WriteReadAging]"),
    ("invalidcmd", "INVALID COMMAND"),
])
def test_run_commands(user_input, expected_output_contains):
    ssd = NormalSSDDriver()
    validator = Validator()
    f = io.StringIO()

    if user_input == "exit":
        with pytest.raises(SystemExit):
            with redirect_stdout(f):
                run(user_input, ssd, validator)
    else:
        with redirect_stdout(f):
            run(user_input, ssd, validator)
        output = f.getvalue()
        assert expected_output_contains in output

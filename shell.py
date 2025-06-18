import sys

from shell_core.commands.help_command import HelpCommand
from shell_core.commands.read_command import ReadCommand
from shell_core.commands.testscenario1 import TestScenario1
from shell_core.commands.testscenario2 import TestScenario2
from shell_core.commands.testscenario3 import TestScenario3
from shell_core.commands.write_command import WriteCommand
from shell_core.normal_ssd_driver import NormalSSDDriver
from ssd_core.abstract_ssd import AbstractSSD
from validator import Validator


def main():
    print("<< Test Shell Application>> Start")

    validator = Validator()
    ssd = NormalSSDDriver()

    while True:
        # 입력 줄의 앞뒤 공백 및 개행 문자 제거
        line = input("Shell> ")
        user_input = line.strip()

        if not user_input:
            continue

        parts = user_input.split()

        if len(parts) <= 1:  # 1 맞나요?
            print("INVALID COMMAND")
            continue

        command = parts[0].lower()

        if command == "write":
            valid_cmd, address, data = validator.run(user_input)
            executor = WriteCommand(ssd, address, data)
            executor.execute()
            print("[Write] Done")
        elif command == "read":
            valid_cmd, address, data = validator.run(user_input)
            executor = ReadCommand(ssd, address)
            executor.execute()
        elif command == "help":
            executor = HelpCommand()
            executor.execute()
        elif command == "fullwrite":
            print(f"[FullWrite] TBU")
        elif command == "fullread":
            print(f"[FullRead] TBU")
        elif command == "exit":
            pass
        elif command.startswith("1_"):
            executor = TestScenario1(ssd)
            executor.execute()
        elif command.startswith("2_"):
            executor = TestScenario2(ssd)
            executor.execute()
        elif command.startswith("2_"):
            executor = TestScenario3(ssd)
            executor.execute()
        else:
            print("INVALID COMMAND")
            continue


if __name__ == "__main__":
    main()

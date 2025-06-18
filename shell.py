import sys

from shell_core.commands.help_command import HelpCommand
from shell_core.commands.read_command import ReadCommand
from shell_core.commands.write_command import WriteCommand
from ssd_core.abstract_ssd import AbstractSSD
from validator import Validator


class NormalSSDDriver(AbstractSSD):
    # 실행 오류 방지를 위한 임시 구현체
    def write(self, address: int, data: str) -> None:
        pass

    def read(self, address: int) -> str:
        pass


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
            executor = WriteCommand(ssd)
            executor.execute(address, data)
            print("[Write] Done")
        elif command == "read":
            valid_cmd, address, data = validator.run(user_input)
            executor = ReadCommand(ssd)
            receive_data = executor.execute(address)  # return type 불일치, duck typing 적용
            print(f"[Read] LBA {address} : {receive_data}")
        elif command == "help":
            executor = HelpCommand()
            executor.execute()
        elif command == "fullwrite":
            print(f"[FullWrite] TBU")
        elif command == "fullread":
            print(f"[FullRead] TBU")
        elif command == "exit":
            pass
        else:
            print("INVALID COMMAND")
            continue


if __name__ == "__main__":
    main()

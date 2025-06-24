import sys
from shell_core.logger import logger
from command_core.command_factory import CommandFactory
from adapter.ssd_shell_adapter import SSDShellAdapter
from validator import ShellValidator
from command_core.exceptions import InvalidLBAError


class Shell:
    def __init__(self):
        self.ssd = SSDShellAdapter()
        self.validator = ShellValidator()

    def run(self, user_input: str) -> None:
        user_input = user_input.strip()
        if not user_input:
            return

        logger.print(f"User input received: {user_input}")
        packet = self.validator.run(user_input)

        if packet.COMMAND is False:
            logger.print(f"INVALID COMMAND: {user_input}")
            print("INVALID COMMAND")
            return

        executor = CommandFactory.create(packet.COMMAND, self.ssd, packet.ADDR, packet.VALUE)
        executor.execute()
        logger.print(f"Command executed: {packet.COMMAND} {packet.ADDR} {packet.VALUE}")

    def start_interactive(self):
        logger.print("Test Shell started")
        print("<< Test Shell Application >> Start")

        while True:
            try:
                user_input = input("Shell> ")
                self.run(user_input)
            except SystemExit:
                logger.print("Test Shell exited")
                break
            except InvalidLBAError as e:
                logger.print(f"LBA 범위 오류: {e}")
                print(f"LBA 범위 오류: {e}")
            except Exception as e:
                logger.print(f"INVALID COMMAND: {e}")
                print("INVALID COMMAND")

    def run_script(self, filename: str):
        logger.print("Running shell in automatic mode without prompt")
        self.run(filename)


def main():
    shell = Shell()
    if len(sys.argv) > 1 and sys.argv[1] == 'shell_scripts.txt':
        shell.run_script('shell_scripts.txt')
    shell.start_interactive()


if __name__ == "__main__":
    main()

import sys
from shell_core.logger import logger
from command_core.command_factory import CommandFactory
from shell_core.normal_ssd_driver import NormalSSDDriver
from validator import ShellValidator


def run(user_input: str, ssd: NormalSSDDriver, validator: ShellValidator) -> None:
    user_input = user_input.strip()
    if not user_input:
        return

    logger.print(f"User input received: {user_input}")

    packet = validator.run(user_input)

    if packet.COMMAND is False:
        logger.print(f"INVALID COMMAND: {user_input}")
        print("INVALID COMMAND")
        return

    executor = CommandFactory.create(packet.COMMAND, ssd, packet.ADDR, packet.VALUE)
    executor.execute()
    logger.print(f"Command executed: {packet.COMMAND} {packet.ADDR} {packet.VALUE}")


def start_shell():
    logger.print("Test Shell started")
    print("<< Test Shell Application >> Start")

    validator = ShellValidator()
    ssd = NormalSSDDriver()

    while True:
        try:
            user_input = input("Shell> ")
            run(user_input, ssd, validator)

        except SystemExit:
            logger.print("Test Shell exited")
            break
        except Exception as e:
            logger.print(f"INVALID COMMAND: {e}")
            print(f"INVALID COMMAND")

def run_shell_automatically():
    logger.print("Running shell in automatic mode without prompt")
    validator = ShellValidator()
    ssd = NormalSSDDriver()

    run("shell_scripts.txt", ssd, validator)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'shell_scripts.txt':
        # 인자가 있을 경우: 자동 실행 모드
        run_shell_automatically()
    start_shell()



if __name__ == "__main__":
    main()

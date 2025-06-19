from shell_core.logger import logger
from command_core.command_factory import CommandFactory
from shell_core.normal_ssd_driver import NormalSSDDriver
from validator import ShellValidator


def run(user_input: str, ssd: NormalSSDDriver, validator: ShellValidator) -> None:
    user_input = user_input.strip()
    if not user_input:
        return

    logger.print(f"User input received: {user_input}")

    cmd_type, address, value = validator.run(user_input)

    if cmd_type is False:
        logger.print(f"Invalid command: {user_input}")
        print("INVALID COMMAND")
        return

    executor = CommandFactory.create(cmd_type, ssd, address, value)
    executor.execute()
    logger.print(f"Command executed: {cmd_type} {address} {value}")


def main():
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
            logger.print(f"Unhandled exception: {e}")
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()

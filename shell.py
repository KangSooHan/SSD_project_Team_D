from shell_core.command_factory import CommandFactory
from shell_core.normal_ssd_driver import NormalSSDDriver
from validator import Validator


def run(user_input: str, ssd: NormalSSDDriver, validator: Validator) -> None:
    user_input = user_input.strip()
    if not user_input:
        return

    cmd_type, address, value = validator.run(user_input)

    if cmd_type is False:
        print("INVALID COMMAND")
        return

    executor = CommandFactory.create(cmd_type, ssd, address, value)
    executor.execute()


def main():
    print("<< Test Shell Application >> Start")

    validator = Validator()
    ssd = NormalSSDDriver()

    while True:
        try:
            user_input = input("Shell> ")
            run(user_input, ssd, validator)

        except SystemExit:
            break
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()

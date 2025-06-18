from typing import Callable, Dict
from shell_core.commands.base_command import BaseCommand
from shell_core.commands.read_command import ReadCommand
from shell_core.commands.write_command import WriteCommand
from shell_core.commands.exit_command import ExitCommand
from shell_core.commands.help_command import HelpCommand
from shell_core.commands.full_read_command import FullReadCommand
from shell_core.commands.full_write_command import FullWriteCommand
from shell_core.commands.testscenario1 import TestScenario1
from shell_core.commands.testscenario2 import TestScenario2
from shell_core.commands.testscenario3 import TestScenario3
from ssd_core.abstract_ssd_driver import AbstractSSDDriver


class CommandFactory:
    _registry: Dict[str, Callable[[AbstractSSDDriver, int | None, int | None], BaseCommand]] = {
        "read": lambda ssd, address, value=None: ReadCommand(ssd, address),
        "write": lambda ssd, address, value: WriteCommand(ssd, address, value),
        "exit": lambda ssd, address=None, value=None: ExitCommand(),
        "help": lambda ssd, address=None, value=None: HelpCommand(),
        "fullread": lambda ssd, address=None, value=None: FullReadCommand(ssd),
        "fullwrite": lambda ssd, address=None, value=None: FullWriteCommand(ssd, value),
        "1_": lambda ssd, address=None, value=None: TestScenario1(ssd),
        "2_": lambda ssd, address=None, value=None: TestScenario2(ssd),
        "3_": lambda ssd, address=None, value=None: TestScenario3(ssd),
    }

    @classmethod
    def create(cls, cmd_type: str, ssd: AbstractSSDDriver, address: int | None = None, value: int | None = None) -> BaseCommand:
        return cls._registry[cmd_type](ssd, address, value)

from typing import Callable, Dict
from command_core.base_command import BaseCommand
from command_core.shell_commands.read_command import ReadCommand
from command_core.shell_commands.write_command import WriteCommand
from command_core.shell_commands.exit_command import ExitCommand
from command_core.shell_commands.help_command import HelpCommand
from command_core.shell_commands.full_read_command import FullReadCommand
from command_core.shell_commands.full_write_command import FullWriteCommand
from command_core.shell_commands.erase_command import EraseCommand
from command_core.shell_commands.erase_range_command import EraseRangeCommand
from command_core.shell_commands.testscenario import TestScenario1
from command_core.shell_commands.testscenario import TestScenario2
from command_core.shell_commands.testscenario import TestScenario3
from command_core.shell_commands.testscenario import TestScenario4
from ssd_core.abstract_ssd_driver import AbstractSSDDriver


class CommandFactory:
    _registry: Dict[str, Callable[[AbstractSSDDriver, int | None, int | None], BaseCommand]] = {
        "read": lambda ssd, address, value=None: ReadCommand(ssd, address),
        "write": lambda ssd, address, value: WriteCommand(ssd, address, value),
        "exit": lambda ssd, address=None, value=None: ExitCommand(),
        "help": lambda ssd, address=None, value=None: HelpCommand(),
        "fullread": lambda ssd, address=None, value=None: FullReadCommand(ssd),
        "fullwrite": lambda ssd, address, value: FullWriteCommand(ssd, value),
        "erase": lambda ssd, address, value: EraseCommand(ssd, address, value),
        "erase_range": lambda ssd, address, value: EraseRangeCommand(ssd, address, value),
        "1_": lambda ssd, address=None, value=None: TestScenario1(ssd),
        "2_": lambda ssd, address=None, value=None: TestScenario2(ssd),
        "3_": lambda ssd, address=None, value=None: TestScenario3(ssd),
        "4_": lambda ssd, address=None, value=None: TestScenario4(ssd),
    }

    @classmethod
    def create(cls, cmd_type: str, ssd: AbstractSSDDriver, address: int | None = None, value: int | None = None) -> BaseCommand:
        return cls._registry[cmd_type](ssd, address, value)

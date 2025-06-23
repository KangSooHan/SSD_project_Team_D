from command_core.base_command import BaseCommand
from ssd_core.abstract_ssd_driver import AbstractSSDDriver


class FlushCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSDDriver):
        self._ssd = ssd

    def execute(self) -> None:
        self._ssd.flush()
        print('[Flush] Done')
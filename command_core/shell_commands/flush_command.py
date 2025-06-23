from command_core.base_command import BaseCommand
from adapter.ssd_adapter_interface import SSDShellInterface


class FlushCommand(BaseCommand):
    def __init__(self, ssd: SSDShellInterface):
        self._ssd = ssd

    def execute(self) -> None:
        self._ssd.flush()
        print('[Flush] Done')
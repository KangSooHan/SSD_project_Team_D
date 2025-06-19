import sys
from command_core.base_command import BaseCommand

class ExitCommand(BaseCommand):
    def execute(self):
        sys.exit(0)

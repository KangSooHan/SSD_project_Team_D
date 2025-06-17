from shell.commands.base import Command

class HelpCommand(Command):
    def execute(self, args: list[str]) -> None:
        print("팀명: D팀 | 팀원: 박치원")
        print("Available commands: write, read, fullwrite, fullread, help, exit")
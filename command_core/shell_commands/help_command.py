import textwrap
from command_core.base_command import BaseCommand

class HelpCommand(BaseCommand):
    def execute(self) -> None:
        print("팀명: Discovery | 팀원: 강수한, 이후광, 윤창흠, 김지영, 이지훈, 박치원")
        print("명령어 사용 방법 : ")
        command_usage = textwrap.dedent('''
        - write : write {LBA} {VALUE}
        - read : read {LBA}
        - exit : exit
        - help : help
        - fullwrite : fullwrite {VALUE}
        - fullread : fullread
        - erase : erase {LBA} {SIZE}
        - erase_range : erase_range {START_LBA} {END_LBA}
        - 1_FullWriteAndReadCompare : 1_
        - 2_PartialLBAWrite : 2_
        - 3_WriteReadAging : 3_
        - 4_EraseAndWriteAging : 4_
        ''').strip()
        print(command_usage)

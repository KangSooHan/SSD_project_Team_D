from ssd.abstract_ssd import AbstractSSD

class HelpCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self) -> None:
        print("팀명: Discovery | 팀원: 강수한, 이후광, 윤창흠, 김지영, 이지훈, 박치원")
        print("명령어 사용 방법 : ")
        command_usage = '''
        - write : write {LBA} {VALUE}
        - read : read {LBA}
        - exit : exit
        - help : help
        - fullwrite : fullwrite {VALUE}
        - fullread : fullread
        '''
        print(command_usage)
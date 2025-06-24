class InvalidLBAError(Exception):
    """
    LBA 범위가 잘못된 경우 발생하는 예외
    LBA는 0부터 99까지의 정수여야 함
    """
    def __init__(self, lba, message=None):
        if message is None:
            message = f"Invalid LBA: {lba}. LBA 는 0~99 사이의 정수여야 함"
        super().__init__(message)
        self.lba = lba

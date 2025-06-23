def to_4byte_hex_str(value: int):
    """
    입력된 int 데이터를 4 byte 범위의 16진수 문자열로 변환
    """
    return f'0x{value:08X}'

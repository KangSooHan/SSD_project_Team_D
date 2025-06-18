import sys

def main():
    print("<< Test Shell Application>> Start")

    while True:
        # 입력 줄의 앞뒤 공백 및 개행 문자 제거
        line = input("Shell> ")
        user_input = line.strip()

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "help":
            print("---- 제작자 & 명령어 ----")

        elif command == "write":
            print("[Write] Done")

        elif command == "read":
            print("[Read] LBA 00 : 0x00000000")

        elif command == "exit":
            print("Exit")
            break

        else:
            print("INVALID COMMAND")

if __name__ == "__main__":
    main()
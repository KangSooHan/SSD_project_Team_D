from ssd_core.normal_ssd import NormalSSD

def main(args=None):
    import sys
    args = args if args is not None else sys.argv[1:]
    if not args:
        return

    command_type = args[0]
    ssd = NormalSSD()

    if command_type == "R" and len(args) == 2:
        lba = int(args[1])
        ssd.read(lba)
        return

    if command_type == "W" and len(args) == 3:
        lba = int(args[1])
        value = args[2]
        ssd.write(lba, value)
        return

    ssd._write_output(NormalSSD.INVALID_OUTPUT)

if __name__ == "__main__":
    main()

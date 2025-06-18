from ssd_core.normal_ssd import NormalSSD
from validator import Validator

def main(args=None):
    import sys
    args = args if args is not None else sys.argv[1:]
    if not args:
        return

    validator = Validator()
    command_type, lba, value = validator.run(" ".join(args))

    ssd = NormalSSD()

    if command_type == "R" and len(args) == 2:
        ssd.read(lba)
        return

    if command_type == "W" and len(args) == 3:
        ssd.write(lba, value)
        return

    ssd._write_output(NormalSSD.INVALID_OUTPUT)

if __name__ == "__main__":
    main()

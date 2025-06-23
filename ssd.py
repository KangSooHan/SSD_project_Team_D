from ssd_core.normal_ssd import NormalSSD
from validator import SSDValidator
from ssd_core.buffer import Buffer

def main(args=None):
    import sys
    args = args if args is not None else sys.argv[1:]
    if not args:
        return

    validator = SSDValidator()
    packet = validator.run(" ".join(args))
    ssd = NormalSSD()
    buffer = Buffer(ssd)

    if buffer.insert(packet):
        #buffer.flush()
        return

    buffer.write_invalid_output()


def main_test(args=None):
    import sys
    args = args if args is not None else sys.argv[1:]
    if not args:
        return

    validator = SSDValidator()
    packet = validator.run(" ".join(args))
    ssd = NormalSSD()
    buffer = Buffer(ssd)

    if buffer.insert(packet):
        buffer.flush()
        return

    buffer.write_invalid_output()

if __name__ == "__main__":
    main()

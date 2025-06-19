from ssd_core.normal_ssd import NormalSSD
from validator import SSDValidator

def main(args=None):
    import sys
    args = args if args is not None else sys.argv[1:]
    if not args:
        return

    validator = SSDValidator()
    packet = validator.run(" ".join(args))
    ssd = NormalSSD()

    if packet.COMMAND == "R":
        ssd.read(packet.ADDR)
        return

    if packet.COMMAND == "W":
        ssd.write(packet.ADDR, packet.VALUE)
        return

    ssd._write_output(NormalSSD.INVALID_OUTPUT)

if __name__ == "__main__":
    main()

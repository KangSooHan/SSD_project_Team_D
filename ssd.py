from ssd_core.hardware.normal_ssd import NormalSSD
from validator import SSDValidator
from ssd_core.command_buffer import CommandBuffer
import sys


def _run_buffer_command(args, flush: bool):
    if not args:
        return

    validator = SSDValidator()
    packet = validator.run(" ".join(args))
    ssd = NormalSSD()
    buffer = CommandBuffer(ssd)

    if buffer.insert(packet):
        if flush:
            buffer.flush()
        return

    buffer.write_invalid_output()


def main(args=None):
    args = args if args is not None else sys.argv[1:]
    _run_buffer_command(args, flush=False)


def main_test(args=None):
    args = args if args is not None else sys.argv[1:]
    _run_buffer_command(args, flush=True)


if __name__ == "__main__":
    main()

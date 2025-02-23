import argparse
import traceback
import termios
import sys
import select
import base64
import logging
from src.main import CPU, Bus

# References:
# https://zserge.com/posts/6502/
# https://www.sbprojects.net/projects/apple1/wozmon.php

WOZMON = base64.b64decode(
    "2Figf4wS0KmnjRHQjRPQyd/wE8mb8APIEA+p3CDv/6mNIO//oAGIMPatEdAQ+60Q0JkAAiDv/8mN0NSg/6kAqgqFK8i5AALJjfDUya6Q9PDwybrw68nS8DuGKIYphCq5AAJJsMkKkAZpiMn6kBEKCgoKogQKJigmKcrQ+MjQ4MQq8JckK1AQpSiBJuYm0LXmJ0xE/2wkADArogK1J5UllSPK0PfQFKmNIO//pSUg3P+lJCDc/6m6IO//qaAg7/+hJCDc/4YrpSTFKKUl5SmwweYk0ALmJaUkKQcQyEhKSkpKIOX/aCkPCbDJupACaQYsEtAw+40S0GAAAAAPAP8AAA=="
)


class MemoryAppleI:
    def __init__(self, data: bytearray):
        self.data = data
        self.keys: list[int] = []

    def __setitem__(self, address, value):
        logging.debug(f"W {address:#06x}: {self.data[address]:x}")

        if address == 0xD012:  # Display
            if value & 0x7F == 0x0D:  # '\r'
                print("")
            elif value & 0x7F == 0x5F:  # '_'
                # '_' works as backspace
                print("\b", end="", flush=True)
            else:
                print(chr(value & 0x7F), end="", flush=True)
        else:
            self.data[address] = value

    def __getitem__(self, address):
        logger.debug(f"R {address:#06x}: {self.data[address]:x}")

        if address == 0xD010:  # KBD
            return self.keys.pop(0) | 0x80 if len(self.keys) else 0x80
        elif address == 0xD011:  # KBDCR
            return 0x80 if len(self.keys) else 0
        else:
            return self.data[address]

    def send_key(self, c):
        logger.debug(f"SEND KEY {c} {chr(c)}")
        self.keys.append(c)

    def dump(self, start=0, end=None):
        if end is None:
            end = len(self.data)

        for index in range(start, end, 16):
            print(
                f"{index:04x}\t{' '.join(f'{x:02x}' for x in self.data[index : index + 16])}"
            )


def init():
    mem = MemoryAppleI(
        [0x00] * 0xFF00  # RAM
        + list(WOZMON)
    )

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.reset()

    print("Starting the Woz Monitor")
    print("Press q to quit")
    old = termios.tcgetattr(sys.stdin)
    try:
        tc = termios.tcgetattr(sys.stdin)
        tc[3] = tc[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, tc)
        while True:
            cpu.step()
            if select.select([sys.stdin], [], [], 0.000001) == ([sys.stdin], [], []):
                c = sys.stdin.read(1)
                if c == "q":
                    print("Quitting")
                    break
                mem.send_key(13 if c == "\n" else ord(c))
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)

    print(cpu)
    mem.dump(cpu.PC, cpu.PC + 1)
    mem.dump(0x20, 0x2F)

    match mem[0x2B]:
        case 0x00:
            mode = "XAM"
        case 0x7F:
            mode = "STOR"
        case 0xAE:
            mode = "BLOCK XAM"
        case _:
            mode = None

    print(
        f"XAML {mem[0x24]:#04x} XAMH {mem[0x25]:#04x} STL {mem[0x26]:#04x} STH {mem[0x27]:#04x} L {mem[0x28]:#04x} H {mem[0x29]:#04x} YSAV {mem[0x2A]:#04x} Mode {mode}"
    )


parser = argparse.ArgumentParser(description="Wozmon on Apple I (6502)")
parser.add_argument(
    "--log",
    default="WARNING",
    help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
args = parser.parse_args()
logging.basicConfig(
    filename="wozmon.log", level=args.log.upper(), format="%(levelname)s: %(message)s"
)
logger = logging.getLogger()

init()

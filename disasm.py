#!/usr/bin/env python
import argparse
import logging
from src.instructions import decode_standard, AddressingMode

instruction_length = {
    AddressingMode.A: 1,
    AddressingMode.ABS: 3,
    AddressingMode.ABS_X: 3,
    AddressingMode.ABS_Y: 3,
    AddressingMode.IMM: 2,
    AddressingMode.IMPL: 1,
    AddressingMode.IMPL: 1,
    AddressingMode.IND: 3,
    AddressingMode.IND_X: 2,
    AddressingMode.IND_Y: 2,
    AddressingMode.REL: 2,
    AddressingMode.ZPG: 2,
    AddressingMode.ZPG_X: 2,
    AddressingMode.ZPG_Y: 2,
}


def asInt(s: str):
    return int(s, 16)


def print_unknown(code: str):
    print(f"{code:#04X},".ljust(20), end="")
    print("# ???")


def disasm(data):
    opcodes = data.read().strip().split(",")
    data_length = len(opcodes)
    i = 0

    while i < data_length:
        opcode = asInt(opcodes[i])

        try:
            inst, mode = decode_standard(opcode)
        except NotImplementedError:
            print_unknown(opcode)
            i += 1
            continue

        operands_length = instruction_length[mode]

        if i + operands_length > data_length:
            # Not enough data for the operand, consider as unknown
            print_unknown(opcode)
            i += 1
            continue

        bin_repr = f"{opcode:#04X},"
        for j in range(1, operands_length):
            bin_repr += f" {asInt(opcodes[i + j]):#04X}, "

        print(bin_repr.ljust(20), end="")
        print(f"# {inst.name}, {mode.name}")
        i += operands_length

    print(f"{data_length} bytes")


parser = argparse.ArgumentParser(description="Disassembler for 6502")

parser.add_argument(
    "infile", type=argparse.FileType("r"), help="Binary file to disassemble"
)
parser.parse_args(["-"])

parser.add_argument(
    "--log",
    default="WARNING",
    help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
args = parser.parse_args()
logging.basicConfig(
    filename="disasm.log", level=args.log.upper(), format="%(levelname)s: %(message)s"
)
logger = logging.getLogger()

disasm(args.infile)

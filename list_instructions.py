#!/usr/bin/env python

import argparse
from src.instructions import standard

parser = argparse.ArgumentParser(description="List implemented 6502 instructions")
parser.add_argument("-i", "--instruction", help="Search for a specific instruction (e.g. LDA)")
parser.add_argument("-c", "--code", help="Search for a specific instruction code (e.g. a5)")
parser.add_argument("-m", "--mode", help="Search for a specific addressing mode (e.g. abs)")
args = parser.parse_args()

def accept(code, instruction, mode):
    return (
        (args.code is None or code.lower() == args.code.lower()) and
        (args.instruction is None or instruction.value.lower() == args.instruction.lower()) and
        (args.mode is None or mode.value.lower() == args.mode.lower())
    )

entries = [
    (f'{i:x}{j:x}', entry[0], entry[1])
    for i, row in enumerate(standard)
    for j, entry in enumerate(row) if entry
]

for code, instruction, mode in entries:
    if accept(code, instruction, mode):
        print(f'{code} {instruction.value} {mode.value}')

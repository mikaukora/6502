#!/usr/bin/env python

import argparse
from src.instructions import standard

parser = argparse.ArgumentParser(description="List implemented 6502 instructions")
parser.add_argument("-i", "--instruction", help="Search for a specific instruction (e.g. LDA)")
parser.add_argument("-c", "--code", help="Search for a specific instruction code (e.g. a5)")
parser.add_argument("-m", "--mode", help="Search for a specific addressing mode (e.g. abs)")
args = parser.parse_args()

def accept(code, instruction, mode):
    def codeFilter(x):
        return True
    def instructionFilter(x):
        return True
    def modeFilter(x):
        return True

    if args.code:
        def codeFilter(code):
            return code.lower() == args.code.lower()
    if args.instruction:
        def instructionFilter(instruction):
            return instruction.value.lower() == args.instruction.lower()
    if args.mode:
        def modeFilter(mode):
            return mode.value.lower() == args.mode.lower()

    return codeFilter(code) and instructionFilter(instruction) and modeFilter(mode)

for i, row in enumerate(standard):
    for j, entry in enumerate(row):
        if entry is None:
            continue
        code = f'{i:x}{j:x}'
        instruction = entry[0]
        mode = entry[1]
        if accept(code, instruction, mode):
                print(f'{code} {instruction.value} {mode.value}')

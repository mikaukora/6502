from typing import Tuple, Optional
from enum import Enum

# Instruction set: https://www.masswerk.at/6502/6502_instruction_set.html#LDA


class Instruction(Enum):
    BRK = "BRK"
    ORA = "ORA"
    ASL = "ASL"
    PHP = "PHP"
    BPL = "BPL"
    CLC = "CLC"
    JSR = "JSR"
    AND = "AND"
    BIT = "BIT"
    ROL = "ROL"
    PLP = "PLP"
    SEC = "SEC"
    RTI = "RTI"
    EOR = "EOR"
    LSR = "LSR"
    PHA = "PHA"
    JMP = "JMP"
    CLI = "CLI"
    RTS = "RTS"
    ADC = "ADC"
    ROR = "ROR"
    PLA = "PLA"
    SEI = "SEI"
    STA = "STA"
    STY = "STY"
    STX = "STX"
    DEY = "DEY"
    TXA = "TXA"
    BCC = "BCC"
    TYA = "TYA"
    TXS = "TXS"
    LDY = "LDY"
    LDA = "LDA"
    LDX = "LDX"
    TAY = "TAY"
    TAX = "TAX"
    CLV = "CLV"
    TSX = "TSX"
    CPY = "CPY"
    CMP = "CMP"
    DEC = "DEC"
    INY = "INY"
    DEX = "DEX"
    CLD = "CLD"
    CPX = "CPX"
    SBC = "SBC"
    INC = "INC"
    INX = "INX"
    NOP = "NOP"
    BEQ = "BEQ"
    SED = "SED"


class AddressingMode(Enum):
    IMPL = "impl"
    IMM = "#"
    ZPG = "zpg"
    ZPG_X = "zpg,X"
    ZPG_Y = "zpg,Y"
    ABS = "abs"
    ABS_X = "abs,X"
    ABS_Y = "abs,Y"
    IND = "ind"
    IND_X = "X,ind"
    IND_Y = "ind,Y"
    REL = "rel"
    A = "A"


i = Instruction
m = AddressingMode

# 6502 standard set
# fmt: off
standard = [
        #0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], # 0
        [None, None, None, None, None, None, None, None, (i.CLC, m.IMPL), None, None, None, None, None, None, None], # 1
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], # 2
        [None, None, None, None, None, None, None, None, (i.SEC, m.IMPL), None, None, None, None, None, None, None], # 3
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], # 4
        [None, None, None, None, None, None, None, None, (i.CLI, m.IMPL), None, None, None, None, None, None, None], # 5
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], # 6
        [None, None, None, None, None, None, None, None, (i.SEI, m.IMPL), None, None, None, None, None, None, None], # 7
        [None, None, None, None, (i.STY, m.ZPG), (i.STA, m.ZPG), (i.STX, m.ZPG), None, (i.DEY, m.IMPL), None, (i.TXA, m.IMPL), None, None, None, None, None], # 8
        [None, None, None, None, None, None, None, None, (i.TYA, m.IMPL), None, (i.TXS, m.IMPL), None, None, None, None, None ], # 9
        [(i.LDY, m.IMM), None, (i.LDX, m.IMM), None, None, None, None, None, (i.TAY, m.IMPL), (i.LDA, m.IMM), (i.TAX, m.IMPL), None, None, None, None, None], # A
        [None, None, None, None, None, None, None, None, (i.CLV, m.IMPL), None, (i.TSX, m.IMPL), None, None, None, None, None], # B
        [None, None, None, None, None, None, (i.DEC, m.ZPG), None, (i.INY, m.IMPL), None, (i.DEX, m.IMPL), None, None, None, None, None], # C
        [None, None, None, None, None, None, None, None, (i.CLD, m.IMPL), None, None, None, None, None, None, None], # D
        [None, None, None, None, None, None, (i.INC, m.ZPG), None, (i.INX, m.IMPL), None, (i.NOP, m.IMPL), None, None, None, None, None], # E
        [None, None, None, None, None, None, None, None, (i.SED, m.IMPL), None, None, None, None, None, None, 1], # F
    ]
# fmt: on


def decode_standard(instruction) -> Optional[Tuple[Instruction, AddressingMode]]:
    try:
        i, m = standard[instruction >> 4][instruction & 0xF]
        print(f"{instruction:#04x} {i.value} {m.value}")
        return i, m
    except TypeError:
        raise NotImplementedError(f'Unknown instruction {instruction:#04x}')

from typing import List, Tuple, Optional
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
    BNE = "BNE"
    SED = "SED"
    BMI = "BMI"
    BCS = "BCS"


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
standard: List[List[Optional[Tuple[Instruction, AddressingMode]]]] = [
        #0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        [None, None, None, None, None, None, None, None, None, (i.ORA, m.IMM), None, None, None, None, None, None], # 0
        [(i.BPL, m.REL), None, None, None, None, None, None, None, (i.CLC, m.IMPL), None, None, None, None, None, None, None], # 1
        [None, None, None, None, None, None, None, None, None, (i.AND, m.IMM), None, None, None, None, None, None], # 2
        [(i.BMI, m.REL), None, None, None, None, None, None, None, (i.SEC, m.IMPL), None, None, None, None, None, None, None], # 3
        [None, None, None, None, None, None, None, None, None, (i.EOR, m.IMM), None, None, (i.JMP, m.ABS), None, None, None], # 4
        [None, None, None, None, None, None, None, None, (i.CLI, m.IMPL), None, None, None, None, None, None, None], # 5
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], # 6
        [None, None, None, None, None, None, None, None, (i.SEI, m.IMPL), None, None, None, None, None, None, None], # 7
        [None, None, None, None, (i.STY, m.ZPG), (i.STA, m.ZPG), (i.STX, m.ZPG), None, (i.DEY, m.IMPL), None, (i.TXA, m.IMPL), None, (i.STY, m.ABS), (i.STA, m.ABS), (i.STX, m.ABS), None], # 8
        [(i.BCC, m.REL), None, None, None, (i.STY, m.ZPG_X), (i.STA, m.ZPG_X), (i.STX, m.ZPG_Y), None, (i.TYA, m.IMPL), None, (i.TXS, m.IMPL), None, None, None, None, None ], # 9
        [(i.LDY, m.IMM), None, (i.LDX, m.IMM), None, (i.LDY, m.ZPG), (i.LDA, m.ZPG), (i.LDX, m.ZPG), None, (i.TAY, m.IMPL), (i.LDA, m.IMM), (i.TAX, m.IMPL), None, (i.LDY, m.ABS), (i.LDA, m.ABS), (i.LDX, m.ABS), None], # A
        [(i.BCS, m.REL), None, None, None, (i.LDY, m.ZPG_X), (i.LDA, m.ZPG_X), (i.LDX, m.ZPG_Y), None, (i.CLV, m.IMPL), (i.LDA, m.ABS_Y), (i.TSX, m.IMPL), None, (i.LDY, m.ABS_X), (i.LDA, m.ABS_X), (i.LDX, m.ABS_Y), None], # B
        [(i.CPY, m.IMM), None, None, None, (i.CPY, m.ZPG), None, (i.DEC, m.ZPG), None, (i.INY, m.IMPL), (i.CMP, m.IMM), (i.DEX, m.IMPL), None, (i.CPY, m.ABS), None, (i.DEC, m.ABS), None], # C
        [(i.BNE, m.REL), None, None, None, None, None, (i.DEC, m.ZPG_X), None, (i.CLD, m.IMPL), None, None, None, None, None, None, None], # D
        [(i.CPX, m.IMM), None, None, None, (i.CPX, m.ZPG), None, (i.INC, m.ZPG), None, (i.INX, m.IMPL), None, (i.NOP, m.IMPL), None, (i.CPX, m.ABS), None, (i.INC, m.ABS), None], # E
        [(i.BEQ, m.REL), None, None, None, None, None, (i.INC, m.ZPG_X), None, (i.SED, m.IMPL), None, None, None, None, None, None, None], # F
    ]
# fmt: on


def decode_standard(instruction) -> Optional[Tuple[Instruction, AddressingMode]]:
    try:
        i, m = standard[instruction >> 4][instruction & 0xF]
        print(f"{instruction:#04x} {i.value} {m.value}")
        return i, m
    except TypeError:
        raise NotImplementedError(f"Unknown instruction {instruction:#04x}")

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
        [None, (i.ORA, m.IND_X), None, None, None, (i.ORA, m.ZPG), (i.ASL, m.ZPG), None, (i.PHP, m.IMPL), (i.ORA, m.IMM), (i.ASL, m.A), None, None, (i.ORA, m.ABS), (i.ASL, m.ABS), None], # 0
        [(i.BPL, m.REL), (i.ORA, m.IND_Y), None, None, None, (i.ORA, m.ZPG_X), (i.ASL, m.ZPG_X), None, (i.CLC, m.IMPL), (i.ORA,m.ABS_Y), None, None, None, (i.ORA,m.ABS_X), (i.ASL, m.ABS_X), None], # 1
        [(i.JSR, m.ABS), (i.AND, m.IND_X), None, None, (i.BIT, m.ZPG), (i.AND, m.ZPG), (i.ROL, m.ZPG), None, (i.PLP, m.IMPL), (i.AND, m.IMM), (i.ROL, m.A), None, (i.BIT, m.ABS), (i.AND, m.ABS), (i.ROL, m.ABS), None], # 2
        [(i.BMI, m.REL), (i.AND, m.IND_Y), None, None, None, (i.AND, m.ZPG_X), (i.ROL, m.ZPG_X), None, (i.SEC, m.IMPL), (i.AND, m.ABS_Y), None, None, None, (i.AND, m.ABS_X), (i.ROL, m.ABS_X), None], # 3
        [None, (i.EOR, m.IND_X), None, None, (i.EOR, m.ZPG), None, (i.LSR, m.ZPG), None, (i.PHA, m.IMPL), (i.EOR, m.IMM), (i.LSR, m.A), None, (i.JMP, m.ABS), (i.EOR, m.ABS), (i.LSR, m.ABS), None], # 4
        [None, (i.EOR, m.IND_Y), None, None, None, (i.EOR, m.ZPG_X), (i.LSR, m.ZPG_X), None, (i.CLI, m.IMPL), (i.EOR, m.ABS_Y), None, None, None, (i.EOR, m.ABS_X), (i.LSR, m.ABS_X), None], # 5
        [(i.RTS, m.ABS), (i.ADC, m.IND_X), None, None, None, (i.ADC, m.ZPG), (i.ROR, m.ZPG), None, (i.PLA, m.IMPL), (i.ADC, m.IMM), (i.ROR, m.A), None, (i.JMP, m.IND), (i.ADC, m.ABS), (i.ROR, m.ABS), None], # 6
        [None, (i.ADC, m.IND_Y), None, None, None, (i.ADC, m.ZPG_X), (i.ROR, m.ZPG_X), None, (i.SEI, m.IMPL), (i.ADC, m.ABS_Y), None, None, None, (i.ADC, m.ABS_X), (i.ROR, m.ABS_X), None], # 7
        [None, None, None, None, (i.STY, m.ZPG), (i.STA, m.ZPG), (i.STX, m.ZPG), None, (i.DEY, m.IMPL), None, (i.TXA, m.IMPL), None, (i.STY, m.ABS), (i.STA, m.ABS), (i.STX, m.ABS), None], # 8
        [(i.BCC, m.REL), None, None, None, (i.STY, m.ZPG_X), (i.STA, m.ZPG_X), (i.STX, m.ZPG_Y), None, (i.TYA, m.IMPL), None, (i.TXS, m.IMPL), None, None, None, None, None ], # 9
        [(i.LDY, m.IMM), None, (i.LDX, m.IMM), None, (i.LDY, m.ZPG), (i.LDA, m.ZPG), (i.LDX, m.ZPG), None, (i.TAY, m.IMPL), (i.LDA, m.IMM), (i.TAX, m.IMPL), None, (i.LDY, m.ABS), (i.LDA, m.ABS), (i.LDX, m.ABS), None], # A
        [(i.BCS, m.REL), None, None, None, (i.LDY, m.ZPG_X), (i.LDA, m.ZPG_X), (i.LDX, m.ZPG_Y), None, (i.CLV, m.IMPL), (i.LDA, m.ABS_Y), (i.TSX, m.IMPL), None, (i.LDY, m.ABS_X), (i.LDA, m.ABS_X), (i.LDX, m.ABS_Y), None], # B
        [(i.CPY, m.IMM), (i.CMP, m.IND_X), None, None, (i.CPY, m.ZPG), (i.CMP, m.ZPG), (i.DEC, m.ZPG), None, (i.INY, m.IMPL), (i.CMP, m.IMM), (i.DEX, m.IMPL), None, (i.CPY, m.ABS), (i.CMP, m.ABS), (i.DEC, m.ABS), None], # C
        [(i.BNE, m.REL), (i.CMP, m.IND_Y), None, None, None, (i.CMP, m.ZPG_X), (i.DEC, m.ZPG_X), None, (i.CLD, m.IMPL), (i.CMP, m.ABS_Y), None, None, None, (i.CMP, m.ABS_X), (i.DEC, m.ABS_X), None], # D
        [(i.CPX, m.IMM), (i.SBC, m.IND_X), None, None, (i.CPX, m.ZPG), (i.SBC, m.ZPG), (i.INC, m.ZPG), None, (i.INX, m.IMPL), (i.SBC, m.IMM), (i.NOP, m.IMPL), None, (i.CPX, m.ABS), (i.SBC, m.ABS), (i.INC, m.ABS), None], # E
        [(i.BEQ, m.REL), (i.SBC, m.IND_Y), None, None, None, (i.SBC, m.ZPG_X), (i.INC, m.ZPG_X), None, (i.SED, m.IMPL), (i.SBC, m.ABS_Y), None, None, None, (i.SBC, m.ABS_X), (i.INC, m.ABS_X), None], # F
    ]
# fmt: on


def decode_standard(instruction) -> Optional[Tuple[Instruction, AddressingMode]]:
    try:
        i, m = standard[instruction >> 4][instruction & 0xF]
        print(f"{instruction:#04x} {i.value} {m.value}")
        return i, m
    except TypeError:
        raise NotImplementedError(f"Unknown instruction {instruction:#04x}")

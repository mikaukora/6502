from src.main import CPU, Bus, Memory


def test_registers():
    cpu = CPU()

    cpu.P = 0x00
    assert cpu.P == 0

    cpu.P = 0xFFFF
    assert cpu.P == 0xFF

    cpu.P = 0x00
    assert cpu.n == 0
    assert cpu.v == 0
    assert cpu.d == 0
    assert cpu.i == 0
    assert cpu.z == 0
    assert cpu.c == 0

    cpu.P = 0xFF
    assert cpu.n == 1
    assert cpu.v == 1
    assert cpu.d == 1
    assert cpu.i == 1
    assert cpu.z == 1
    assert cpu.c == 1

    cpu.P = 0x00
    cpu.n = 1
    assert cpu.P == 0x80
    cpu.v = 1
    assert cpu.P == 0xC0
    cpu.d = 1
    assert cpu.P == 0xC8
    cpu.i = 1
    assert cpu.P == 0xCC
    cpu.z = 1
    assert cpu.P == 0xCE
    cpu.c = 1
    assert cpu.P == 0xCF

    cpu.P = 0xFF
    cpu.n = 0
    assert cpu.P == 0x7F
    cpu.v = 0
    assert cpu.P == 0x3F
    cpu.d = 0
    assert cpu.P == 0x37
    cpu.i = 0
    assert cpu.P == 0x33
    cpu.z = 0
    assert cpu.P == 0x31
    cpu.c = 0
    assert cpu.P == 0x30


def test_fetch():
    bus = Bus(Memory([0xA9, 0x01]))

    cpu = CPU(bus)
    assert cpu.PC == 0x0000

    cpu.step()
    assert cpu.PC == 0x0002
    assert cpu.data == 0x01


def test_LDA_IMM():
    bus = Bus(Memory([0xA9, 0x01, 0xA9, 0x02, 0xA9, 0xFF, 0xA9, 0x00]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.A == 0x02
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.A == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01

    cpu.step()
    assert cpu.A == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00


def test_LDX_IMM():
    bus = Bus(Memory([0xA2, 0x01, 0xA2, 0x02, 0xA2, 0xFF, 0xA2, 0x00]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.X == 0x02
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.X == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01

    cpu.step()
    assert cpu.X == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00


def test_LDY_IMM():
    bus = Bus(Memory([0xA0, 0x01, 0xA0, 0x02, 0xA0, 0xFF, 0xA0, 0x00]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.Y == 0x02
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.Y == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01

    cpu.step()
    assert cpu.Y == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00


def test_LDA_LDX_LDY():
    memory = Memory([0xA9, 0x01, 0xA2, 0x01, 0xA0, 0x01])
    bus = Bus(memory)
    cpu = CPU(bus)

    assert cpu.A == 0x00
    assert cpu.X == 0x00
    assert cpu.Y == 0x00

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.X == 0x00
    assert cpu.Y == 0x00

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.X == 0x01
    assert cpu.Y == 0x00

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.X == 0x01
    assert cpu.Y == 0x01


def test_STA_ZPG():
    memory = Memory([0xA9, 0xEA, 0x85, 0x08, 0x85, 0x09, 0x85, 0x0A, 0x22, 0x22, 0x22])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0xEA

    cpu.step()
    assert memory[0x08] == 0xEA

    cpu.step()
    assert memory[0x09] == 0xEA

    cpu.step()
    assert memory[0x0A] == 0xEA


def test_STY_ZPG():
    memory = Memory([0xA0, 0xEA, 0x84, 0x08, 0x84, 0x09, 0x84, 0x0A, 0x22, 0x22, 0x22])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0xEA

    cpu.step()
    assert memory[0x08] == 0xEA

    cpu.step()
    assert memory[0x09] == 0xEA

    cpu.step()
    assert memory[0x0A] == 0xEA


def test_STX_ZPG():
    memory = Memory([0xA2, 0xEA, 0x86, 0x08, 0x86, 0x09, 0x86, 0x0A, 0x22, 0x22, 0x22])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0xEA

    cpu.step()
    assert memory[0x08] == 0xEA

    cpu.step()
    assert memory[0x09] == 0xEA

    cpu.step()
    assert memory[0x0A] == 0xEA


def test_TAX():
    bus = Bus(Memory([0xA9, 0x01, 0xAA, 0xA9, 0x02, 0xAA]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x01

    cpu.step()
    assert cpu.X == 0x01

    cpu.step()
    assert cpu.A == 0x02

    cpu.step()
    assert cpu.X == 0x02


def test_TAY():
    bus = Bus(Memory([0xA9, 0x01, 0xA8, 0xA9, 0x02, 0xA8]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x01

    cpu.step()
    assert cpu.Y == 0x01

    cpu.step()
    assert cpu.A == 0x02

    cpu.step()
    assert cpu.Y == 0x02


def test_TXA():
    bus = Bus(Memory([0xA2, 0x01, 0x8A, 0xA2, 0x02, 0x8A]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x01

    cpu.step()
    assert cpu.A == 0x01

    cpu.step()
    assert cpu.X == 0x02

    cpu.step()
    assert cpu.A == 0x02


def test_TYA():
    bus = Bus(Memory([0xA0, 0x01, 0x98, 0xA0, 0x02, 0x98]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x01

    cpu.step()
    assert cpu.A == 0x01

    cpu.step()
    assert cpu.Y == 0x02

    cpu.step()
    assert cpu.A == 0x02


def test_STX_TXS():
    bus = Bus(Memory([0xBA, 0xA2, 0x44, 0x9A]))
    cpu = CPU(bus)
    cpu.S = 0x55

    cpu.step()
    assert cpu.X == 0x55

    cpu.step()
    assert cpu.X == 0x44

    cpu.step()
    assert cpu.S == 0x44


def test_NOP():
    bus = Bus(Memory([0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.PC == 0x01
    cpu.step()
    assert cpu.PC == 0x02
    cpu.step()
    assert cpu.PC == 0x03
    cpu.step()
    assert cpu.PC == 0x04
    cpu.step()
    assert cpu.PC == 0x05


def test_CLC():
    bus = Bus(Memory([0x18, 0x18]))
    cpu = CPU(bus)
    cpu.c = 1

    cpu.step()
    assert cpu.c == 0
    cpu.step()
    assert cpu.c == 0


def test_CLD():
    bus = Bus(Memory([0xD8, 0xD8]))
    cpu = CPU(bus)
    cpu.d = 1

    cpu.step()
    assert cpu.d == 0
    cpu.step()
    assert cpu.d == 0


def test_CLI():
    bus = Bus(Memory([0x58, 0x58]))
    cpu = CPU(bus)
    cpu.i = 1

    cpu.step()
    assert cpu.i == 0
    cpu.step()
    assert cpu.i == 0


def test_CLV():
    bus = Bus(Memory([0xB8, 0xB8]))
    cpu = CPU(bus)
    cpu.v = 1

    cpu.step()
    assert cpu.v == 0
    cpu.step()
    assert cpu.v == 0


def test_SEC():
    bus = Bus(Memory([0x38, 0x38]))
    cpu = CPU(bus)
    cpu.c = 0

    cpu.step()
    assert cpu.c == 1
    cpu.step()
    assert cpu.c == 1


def test_SED():
    bus = Bus(Memory([0xF8, 0xF8]))
    cpu = CPU(bus)
    cpu.d = 0

    cpu.step()
    assert cpu.d == 1
    cpu.step()
    assert cpu.d == 1


def test_SEI():
    bus = Bus(Memory([0x78, 0x78]))
    cpu = CPU(bus)
    cpu.i = 0

    cpu.step()
    assert cpu.i == 1
    cpu.step()
    assert cpu.i == 1


def test_INX_DEX():
    bus = Bus(Memory([0xE8, 0xE8, 0xCA, 0xCA, 0xCA]))
    cpu = CPU(bus)
    cpu.X = 0

    cpu.step()
    assert cpu.X == 0x01
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.X == 0x02
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.X == 0x01
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.X == 0x00
    assert cpu.z == 1
    assert cpu.n == 0
    cpu.step()
    assert cpu.X == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1


def test_INY_DEY():
    bus = Bus(Memory([0xC8, 0xC8, 0x88, 0x88, 0x88]))
    cpu = CPU(bus)
    cpu.Y = 0

    cpu.step()
    assert cpu.Y == 0x01
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.Y == 0x02
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.Y == 0x01
    assert cpu.z == 0
    assert cpu.n == 0
    cpu.step()
    assert cpu.Y == 0x00
    assert cpu.z == 1
    assert cpu.n == 0
    cpu.step()
    assert cpu.Y == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1


def test_DEC_INC_ZPG():
    memory = Memory([0xC6, 0x08, 0xC6, 0x08, 0xE6, 0x08, 0xE6, 0x08, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.Y = 0

    cpu.step()
    assert memory[0x08] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x08] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x08] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x08] == 0x00
    assert cpu.z == 1
    assert cpu.n == 0


def test_LDA_ZPG():
    bus = Bus(Memory([0xA5, 0x06, 0xA5, 0x07, 0xA5, 0x08, 0x00, 0x01, 0xFF]))
    cpu = CPU(bus)
    cpu.A = 0xEA

    cpu.step()
    assert cpu.A == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.A == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_LDX_ZPG():
    bus = Bus(Memory([0xA6, 0x06, 0xA6, 0x07, 0xA6, 0x08, 0x00, 0x01, 0xFF]))
    cpu = CPU(bus)
    cpu.X = 0xEA

    cpu.step()
    assert cpu.X == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.X == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.X == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_LDY_ZPG():
    bus = Bus(Memory([0xA4, 0x06, 0xA4, 0x07, 0xA4, 0x08, 0x00, 0x01, 0xFF]))
    cpu = CPU(bus)
    cpu.Y = 0xEA

    cpu.step()
    assert cpu.Y == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.Y == 0x01
    assert cpu.z == 0x00
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.Y == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_LDA_ABS():
    bus = Bus(Memory([0xAD, 0x06, 0x00, 0xAD, 0x07, 0x00, 0x00, 0xFF]))
    cpu = CPU(bus)
    cpu.A = 0xEA

    cpu.step()
    assert cpu.A == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.A == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_LDX_ABS():
    bus = Bus(Memory([0xAE, 0x06, 0x00, 0xAE, 0x07, 0x00, 0x00, 0xFF]))
    cpu = CPU(bus)
    cpu.X = 0xEA

    cpu.step()
    assert cpu.X == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.X == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_LDY_ABS():
    bus = Bus(Memory([0xAC, 0x06, 0x00, 0xAC, 0x07, 0x00, 0x00, 0xFF]))
    cpu = CPU(bus)
    cpu.Y = 0xEA

    cpu.step()
    assert cpu.Y == 0x00
    assert cpu.z == 0x01
    assert cpu.n == 0x00

    cpu.step()
    assert cpu.Y == 0xFF
    assert cpu.z == 0x00
    assert cpu.n == 0x01


def test_STA_ABS():
    memory = Memory([0x8D, 0x06, 0x00, 0x8D, 0x07, 0x00, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.A = 0xEA

    cpu.step()
    assert memory[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory[(0x00 << 8) + 0x07] == 0xEA


def test_STX_ABS():
    memory = Memory([0x8E, 0x06, 0x00, 0x8E, 0x07, 0x00, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.X = 0xEA

    cpu.step()
    assert memory[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory[(0x00 << 8) + 0x07] == 0xEA


def test_STY_ABS():
    memory = Memory([0x8C, 0x06, 0x00, 0x8C, 0x07, 0x00, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.Y = 0xEA

    cpu.step()
    assert memory[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory[(0x00 << 8) + 0x07] == 0xEA


def test_DEC_INC_ABS():
    memory = Memory(
        [0xCE, 0x0C, 0x00, 0xCE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0x00]
    )
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.Y = 0

    cpu.step()
    assert memory[(0x00 << 8) + 0x0C] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[(0x00 << 8) + 0x0C] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[(0x00 << 8) + 0x0C] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[(0x00 << 8) + 0x0C] == 0x00
    assert cpu.z == 1
    assert cpu.n == 0


def test_LDA_ZPG_X():
    bus = Bus(Memory([0xA2, 0x07, 0xB5, 0x00, 0xE8, 0xB5, 0x00, 0xCC, 0xDD]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x07

    cpu.step()
    assert cpu.A == 0xCC

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert cpu.A == 0xDD


def test_LDY_ZPG_X():
    bus = Bus(Memory([0xA2, 0x07, 0xB4, 0x00, 0xE8, 0xB4, 0x00, 0xCC, 0xDD]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x07

    cpu.step()
    assert cpu.Y == 0xCC

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert cpu.Y == 0xDD


def test_STA_ZPG_X():
    memory = Memory([0xA2, 0x08, 0xA9, 0x55, 0x95, 0x00, 0xEA, 0xEA, 0xDD])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert cpu.A == 0x55

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert memory[0x08] == 0x55


def test_STY_ZPG_X():
    memory = Memory([0xA2, 0x08, 0xA0, 0x55, 0x94, 0x00, 0xEA, 0xEA, 0xDD])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert cpu.Y == 0x55

    cpu.step()
    assert cpu.X == 0x08

    cpu.step()
    assert memory[0x08] == 0x55


def test_DEC_INC_ZPG_X():
    memory = Memory([0xA2, 0x0A, 0xD6, 0x00, 0xD6, 0x00, 0xF6, 0x00, 0xF6, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x0A

    cpu.step()
    assert memory[0x0A] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x0A] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x0A] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory[0x0A] == 0x00
    assert cpu.z == 1
    assert cpu.n == 0


def test_LDX_ZPG_Y():
    bus = Bus(Memory([0xA0, 0x07, 0xB6, 0x00, 0xC8, 0xB6, 0x00, 0xCC, 0xDD]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x07

    cpu.step()
    assert cpu.X == 0xCC

    cpu.step()
    assert cpu.Y == 0x08

    cpu.step()
    assert cpu.X == 0xDD


def test_STX_ZPG_Y():
    memory = Memory(
        [
            0xA2,
            0xEA,
            0xA0,
            0x0C,
            0x96,
            0x00,
            0xC8,
            0x96,
            0x00,
            0xC8,
            0x96,
            0x00,
            0x22,
            0x22,
            0x22,
        ]
    )
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0xEA

    cpu.step()
    assert cpu.Y == 0x0C

    cpu.step()
    assert memory[0x0C] == 0xEA

    cpu.step()
    assert cpu.Y == 0x0D

    cpu.step()
    assert memory[0x0D] == 0xEA

    cpu.step()
    assert cpu.Y == 0x0E

    cpu.step()
    assert memory[0x0E] == 0xEA


def test_LDA_ABS_X():
    bus = Bus(
        Memory([0xA2, 0x09, 0xBD, 0x00, 0x00, 0xE8, 0xBD, 0x00, 0x00, 0xCC, 0xDD])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x09

    cpu.step()
    assert cpu.A == 0xCC

    cpu.step()
    assert cpu.X == 0x0A

    cpu.step()
    assert cpu.A == 0xDD


def test_LDA_ABS_Y():
    bus = Bus(
        Memory([0xA0, 0x09, 0xB9, 0x00, 0x00, 0xC8, 0xB9, 0x00, 0x00, 0xCC, 0xDD])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x09

    cpu.step()
    assert cpu.A == 0xCC

    cpu.step()
    assert cpu.Y == 0x0A

    cpu.step()
    assert cpu.A == 0xDD


"""
    Test high bytes handling.
"""


def test_STA_ABS_hi():
    program = [0x8D, 0x00, 0x01, 0x8D, 0x00, 0x02, 0x8D, 0x0F, 0x01, 0x8D, 0x0F, 0x02]

    memory = Memory(program + [0xEA] * (0x210 - len(program)))
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.A = 0x00

    cpu.step()
    assert memory[(0x01 << 8) + 0x00] == 0x00
    cpu.step()
    assert memory[(0x02 << 8) + 0x00] == 0x00
    cpu.step()
    assert memory[(0x01 << 8) + 0x0F] == 0x00
    cpu.step()
    assert memory[(0x02 << 8) + 0x0F] == 0x00


def test_CMP_IMM():
    bus = Bus(Memory([0xA9, 0x0F, 0xC9, 0x0F, 0xC9, 0x0E, 0xC9, 0x10]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, A == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, A > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, A < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPX_IMM():
    bus = Bus(Memory([0xA2, 0x0F, 0xE0, 0x0F, 0xE0, 0x0E, 0xE0, 0x10]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, X == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, X > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, X < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPY_IMM():
    bus = Bus(Memory([0xA0, 0x0F, 0xC0, 0x0F, 0xC0, 0x0E, 0xC0, 0x10]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0,Y == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, Y > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, Y < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPX_ZPG():
    bus = Bus(Memory([0xA2, 0x0F, 0xE4, 0x08, 0xE4, 0x09, 0xE4, 0x0A, 0x0F, 0x0E, 0x10]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, X == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, X > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, X < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPX_ABS():
    program = [0xA2, 0x0F, 0xEC, 0x00, 0x01, 0xEC, 0x01, 0x01, 0xEC, 0x02, 0x01]

    memory = Memory(program + [0xEA] * (0x210 - len(program)))
    memory[(0x01 << 8) + 0x00] = 0x0F
    memory[(0x01 << 8) + 0x01] = 0x0E
    memory[(0x01 << 8) + 0x02] = 0x10
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, X == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, X > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, X < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPY_ZPG():
    bus = Bus(Memory([0xA0, 0x0F, 0xC4, 0x08, 0xC4, 0x09, 0xC4, 0x0A, 0x0F, 0x0E, 0x10]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, Y == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, Y > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, Y < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_CPY_ABS():
    program = [0xA0, 0x0F, 0xCC, 0x00, 0x01, 0xCC, 0x01, 0x01, 0xCC, 0x02, 0x01]

    memory = Memory(program + [0xEA] * (0x210 - len(program)))
    memory[(0x01 << 8) + 0x00] = 0x0F
    memory[(0x01 << 8) + 0x01] = 0x0E
    memory[(0x01 << 8) + 0x02] = 0x10
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x0F

    cpu.step()
    #  0x0F - 0x0F = 0, Y == M
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x0E = 1, Y > M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 1
    assert cpu.n == 0

    #  0x0F - 0x10 = -1, Y < M
    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1


def test_LDX_ABS_Y():
    bus = Bus(
        Memory([0xA0, 0x09, 0xBE, 0x00, 0x00, 0xC8, 0xBE, 0x00, 0x00, 0xCC, 0xDD])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0x09

    cpu.step()
    assert cpu.X == 0xCC

    cpu.step()
    assert cpu.Y == 0x0A

    cpu.step()
    assert cpu.X == 0xDD


def test_LDY_ABS_X():
    bus = Bus(
        Memory([0xA2, 0x09, 0xBC, 0x00, 0x00, 0xE8, 0xBC, 0x00, 0x00, 0xCC, 0xDD])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x09

    cpu.step()
    assert cpu.Y == 0xCC

    cpu.step()
    assert cpu.X == 0x0A

    cpu.step()
    assert cpu.Y == 0xDD


def test_JMP():
    mem = Memory([
        0x4C, 0x05, 0x00,  # JMP $0005
        0xA9, 0x55,        # LDA #$55   (Skipped)
        0xA9, 0x66,        # LDA #$66
        0x6C, 0x0a, 0x00,  # JMP ($000a) (Indirect jump)
        0x0e, 0x00,        # Jump target: $000e
        0xEA, 0xEA,        # NOP, NOP (Padding)
        0xA9, 0x77,        # LDA #$77   (This is at $0014, should be executed)
    ])

    bus = Bus(mem)
    cpu = CPU(bus)

    cpu.step()  # JMP $0005
    assert cpu.PC == 0x0005  # Should land on LDA #$66

    cpu.step()  # LDA #$66
    assert cpu.A == 0x66

    cpu.step()  # JMP ($0010) - indirect
    assert cpu.PC == 0x000e

    cpu.step()  # LDA #$77
    assert cpu.A == 0x77



def test_BEQ():
    bus = Bus(
        Memory([0xA9, 0x01, 0xF0, 0x05, 0xA9, 0x00, 0xF0, 0x03, 0xa9, 0x55, 0xea, 0xa9, 0xFF])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x01
    assert cpu.z == 0

    cpu.step()
    cpu.step()
    assert cpu.A == 0x00
    assert cpu.z == 1

    cpu.step()
    cpu.step()
    assert cpu.A == 0xFF


def test_BNE():
    bus = Bus(
        Memory([0xA9, 0x00, 0xD0, 0x05, 0xA9, 0x01, 0xD0, 0x03, 0xa9, 0x55, 0xea, 0xa9, 0xFF])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x00
    assert cpu.z == 1

    cpu.step()
    cpu.step()
    assert cpu.A == 0x01
    assert cpu.z == 0

    cpu.step()
    cpu.step()
    assert cpu.A == 0xFF


def test_BMI():
    bus = Bus(
        Memory([0xA9, 0x00, 0x30, 0x05, 0xA9, 0xFF, 0x30, 0x03, 0xa9, 0x55, 0xea, 0xa9, 0xEE])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x00
    assert cpu.n == 0

    cpu.step()
    cpu.step()
    assert cpu.A == 0xFF
    assert cpu.n == 1

    cpu.step()
    cpu.step()
    assert cpu.A == 0xEE


def test_BPL():
    bus = Bus(
        Memory([0xA9, 0xFF, 0x10, 0x05, 0xA9, 0x00, 0x10, 0x03, 0xa9, 0x55, 0xea, 0xa9, 0xEE])
    )
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0xFF
    assert cpu.n == 1

    cpu.step()
    cpu.step()
    assert cpu.A == 0x00
    assert cpu.n == 0

    cpu.step()
    cpu.step()
    assert cpu.A == 0xEE


def test_BCS():
    bus = Bus(Memory([0xA9, 0x0F, 0xC9, 0x0F, 0xB0, 0x02, 0xA9, 0x10, 0xA9, 0xEE]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x0F

    cpu.step()
    assert cpu.z == 1
    assert cpu.c == 1
    assert cpu.n == 0

    cpu.step()

    cpu.step()
    assert cpu.A == 0xEE


def test_BCC():
    bus = Bus(Memory([0xA9, 0x0F, 0xC9, 0x10, 0x90, 0x02, 0xA9, 0x10, 0xA9, 0xEE]))
    cpu = CPU(bus)

    cpu.step()
    assert cpu.A == 0x0F

    cpu.step()
    assert cpu.z == 0
    assert cpu.c == 0
    assert cpu.n == 1

    cpu.step()

    cpu.step()
    assert cpu.A == 0xEE


def test_AND():
    program = [
        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x29, 0xAA,       # AND #$AA  ; A = $F0 AND $AA -> $A0
        0x8D, 0x00, 0x02, # STA $0200 ; Store result in safe memory area

        0xA9, 0x55,       # LDA #$55  ; Load A with $55
        0x2D, 0x00, 0x02, # AND $0200 ; A = $55 AND value at $0200 ($A0)

        0xA9, 0x0F,       # LDA #$0F  ; Load A with $0F
        0x3D, 0x10, 0x02, # AND $0210,X ; AND with absolute,X (assume X=0)

        0xA9, 0x33,       # LDA #$33  ; Load A with $33
        0x2D, 0x20, 0x02, # AND $0220 ; AND with absolute memory address

        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x39, 0x40, 0x02, # AND $0240,Y ; Absolute,Y addressing

        0xA2, 0x00,       # LDX #$00  ; Load X with 0
        0xA9, 0x22,       # LDA #$22  ; Load A with $22
        0x21, 0x50,       # AND ($50,X) ; Indirect,X addressing

        0xA9, 0x11,       # LDA #$11  ; Load A with $11
        0x31, 0x60        # AND ($60),Y ; Indirect,Y addressing
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    mem[0x0200] = 0xA0  # Used in absolute addressing
    mem[0x0210] = 0x0C  # Used in absolute,X addressing
    mem[0x0220] = 0xCC  # Used in absolute addressing
    mem[0x0240] = 0x0F  # Used in absolute,Y addressing
    mem[0x0050] = 0x80  # Pointer for (indirect,X)
    mem[0x0051] = 0x02
    mem[0x0280] = 0x77  # Value for (indirect,X)
    mem[0x0060] = 0x90  # Pointer for (indirect),Y
    mem[0x0061] = 0x02
    mem[0x0290] = 0x99  # Value for (indirect),Y

    # Execute and verify results
    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # AND #$AA
    assert cpu.A == (0xF0 & 0xAA)

    cpu.step()  # STA $0200
    assert mem[0x0200] == 0xA0

    cpu.step()  # LDA #$55
    assert cpu.A == 0x55

    cpu.step()  # AND $0200
    assert cpu.A == (0x55 & 0xA0)

    cpu.step()  # LDA #$0F
    assert cpu.A == 0x0F

    cpu.step()  # AND $0210,X
    assert cpu.A == (0x0F & 0x0C)

    cpu.step()  # LDA #$33
    assert cpu.A == 0x33

    cpu.step()  # AND $0220
    assert cpu.A == (0x33 & 0xCC)

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # AND $0240,Y
    assert cpu.A == (0xF0 & 0x0F)

    cpu.step()  # LDX #$00
    assert cpu.X == 0x00

    cpu.step()  # LDA #$22
    assert cpu.A == 0x22

    cpu.step()  # AND ($50,X)
    assert cpu.A == (0x22 & 0x77)

    cpu.step()  # LDA #$11
    assert cpu.A == 0x11

    cpu.step()  # AND ($60),Y
    assert cpu.A == (0x11 & 0x99)


def test_ORA():
    program = [
        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x09, 0xAA,       # ORA #$AA  ; A = $F0 OR $AA -> $FA
        0x8D, 0x00, 0x02, # STA $0200 ; Store result in safe memory area

        0xA9, 0x55,       # LDA #$55  ; Load A with $55
        0x0D, 0x00, 0x02, # ORA $0200 ; A = $55 OR value at $0200 ($FA)

        0xA9, 0x0F,       # LDA #$0F  ; Load A with $0F
        0x1D, 0x10, 0x02, # ORA $0210,X ; ORA with absolute,X (assume X=0)

        0xA9, 0x33,       # LDA #$33  ; Load A with $33
        0x0D, 0x20, 0x02, # ORA $0220 ; ORA with absolute memory address

        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x19, 0x40, 0x02, # ORA $0240,Y ; Absolute,Y addressing

        0xA2, 0x00,       # LDX #$00  ; Load X with 0
        0xA9, 0x22,       # LDA #$22  ; Load A with $22
        0x01, 0x50,       # ORA ($50,X) ; Indirect,X addressing

        0xA9, 0x11,       # LDA #$11  ; Load A with $11
        0x11, 0x60        # ORA ($60),Y ; Indirect,Y addressing
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    mem[0x0200] = 0xFA  # Used in absolute addressing
    mem[0x0210] = 0x0C  # Used in absolute,X addressing
    mem[0x0220] = 0xCC  # Used in absolute addressing
    mem[0x0240] = 0x0F  # Used in absolute,Y addressing
    mem[0x0050] = 0x80  # Pointer for (indirect,X)
    mem[0x0051] = 0x02
    mem[0x0280] = 0x77  # Value for (indirect,X)
    mem[0x0060] = 0x90  # Pointer for (indirect),Y
    mem[0x0061] = 0x02
    mem[0x0290] = 0x99  # Value for (indirect),Y

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # ORA #$AA
    assert cpu.A == 0xFA

    cpu.step()  # STA $0200
    assert mem[0x0200] == 0xFA

    cpu.step()  # LDA #$55
    assert cpu.A == 0x55

    cpu.step()  # ORA $0200
    assert cpu.A == (0x55 | 0xFA)

    cpu.step()  # LDA #$0F
    assert cpu.A == 0x0F

    cpu.step()  # ORA $0210,X
    assert cpu.A == (0x0F | 0x0C)

    cpu.step()  # LDA #$33
    assert cpu.A == 0x33

    cpu.step()  # ORA $0220
    assert cpu.A == (0x33 | 0xCC)

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # ORA $0240,Y
    assert cpu.A == (0xF0 | 0x0F)

    cpu.step()  # LDX #$00
    assert cpu.X == 0x00

    cpu.step()  # LDA #$22
    assert cpu.A == 0x22

    cpu.step()  # ORA ($50,X)
    assert cpu.A == (0x22 | 0x77)

    cpu.step()  # LDA #$11
    assert cpu.A == 0x11

    cpu.step()  # ORA ($60),Y
    assert cpu.A == (0x11 | 0x99)


def test_EOR():
    program = [
        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x49, 0xAA,       # EOR #$AA  ; A = $F0 XOR $AA -> $5A
        0x8D, 0x00, 0x02, # STA $0200 ; Store result in safe memory area

        0xA9, 0x55,       # LDA #$55  ; Load A with $55
        0x4D, 0x00, 0x02, # EOR $0200 ; A = $55 XOR value at $0200 ($5A)

        0xA9, 0x0F,       # LDA #$0F  ; Load A with $0F
        0x5D, 0x10, 0x02, # EOR $0210,X ; EOR with absolute,X (assume X=0)

        0xA9, 0x33,       # LDA #$33  ; Load A with $33
        0x4D, 0x20, 0x02, # EOR $0220 ; EOR with absolute memory address

        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0x59, 0x40, 0x02, # EOR $0240,Y ; Absolute,Y addressing

        0xA2, 0x00,       # LDX #$00  ; Load X with 0
        0xA9, 0x22,       # LDA #$22  ; Load A with $22
        0x41, 0x50,       # EOR ($50,X) ; Indirect,X addressing

        0xA9, 0x11,       # LDA #$11  ; Load A with $11
        0x51, 0x60        # EOR ($60),Y ; Indirect,Y addressing
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    mem[0x0200] = 0x5A  # Used in absolute addressing
    mem[0x0210] = 0x0C  # Used in absolute,X addressing
    mem[0x0220] = 0xCC  # Used in absolute addressing
    mem[0x0240] = 0x0F  # Used in absolute,Y addressing
    mem[0x0050] = 0x80  # Pointer for (indirect,X)
    mem[0x0051] = 0x02
    mem[0x0280] = 0x77  # Value for (indirect,X)
    mem[0x0060] = 0x90  # Pointer for (indirect),Y
    mem[0x0061] = 0x02
    mem[0x0290] = 0x99  # Value for (indirect),Y

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # EOR #$AA
    assert cpu.A == 0x5A

    cpu.step()  # STA $0200
    assert mem[0x0200] == 0x5A

    cpu.step()  # LDA #$55
    assert cpu.A == 0x55

    cpu.step()  # EOR $0200
    assert cpu.A == (0x55 ^ 0x5A)

    cpu.step()  # LDA #$0F
    assert cpu.A == 0x0F

    cpu.step()  # EOR $0210,X
    assert cpu.A == (0x0F ^ 0x0C)

    cpu.step()  # LDA #$33
    assert cpu.A == 0x33

    cpu.step()  # EOR $0220
    assert cpu.A == (0x33 ^ 0xCC)

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # EOR $0240,Y
    assert cpu.A == (0xF0 ^ 0x0F)

    cpu.step()  # LDX #$00
    assert cpu.X == 0x00

    cpu.step()  # LDA #$22
    assert cpu.A == 0x22

    cpu.step()  # EOR ($50,X)
    assert cpu.A == (0x22 ^ 0x77)

    cpu.step()  # LDA #$11
    assert cpu.A == 0x11

    cpu.step()  # EOR ($60),Y
    assert cpu.A == (0x11 ^ 0x99)


def test_CMP():
    program = [
        0xA9, 0x50,       # LDA #$50  ; Load A with $50
        0xC9, 0x50,       # CMP #$50  ; Compare A with immediate value

        0xA9, 0x30,       # LDA #$30  ; Load A with $30
        0xC5, 0x10,       # CMP $10   ; Compare A with value in zero page

        0xA9, 0x80,       # LDA #$80  ; Load A with $80
        0xD5, 0x20,       # CMP $20,X ; Compare with zero page, X (assume X=0)

        0xA9, 0xF0,       # LDA #$F0  ; Load A with $F0
        0xCD, 0x00, 0x02, # CMP $0200 ; Compare with absolute address

        0xA9, 0x70,       # LDA #$70  ; Load A with $70
        0xDD, 0x10, 0x02, # CMP $0210,X ; Compare with absolute, X (assume X=0)

        0xA9, 0x20,       # LDA #$20  ; Load A with $20
        0xD9, 0x20, 0x02, # CMP $0220,Y ; Compare with absolute, Y (assume Y=0)

        0xA2, 0x00,       # LDX #$00  ; Load X with 0
        0xA9, 0x60,       # LDA #$60  ; Load A with $60
        0xC1, 0x30,       # CMP ($30,X) ; Indirect, X

        0xA9, 0x90,       # LDA #$90  ; Load A with $90
        0xD1, 0x40        # CMP ($40),Y ; Indirect, Y
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    mem[0x0010] = 0x30  # Zero page value
    mem[0x0020] = 0x80  # Zero page,X value
    mem[0x0200] = 0xF0  # Absolute addressing value
    mem[0x0210] = 0x70  # Absolute,X value
    mem[0x0220] = 0x20  # Absolute,Y value
    mem[0x0030] = 0x90  # Pointer for (indirect,X)
    mem[0x0031] = 0x02
    mem[0x0290] = 0x60  # Value for (indirect,X)
    mem[0x0040] = 0xA0  # Pointer for (indirect),Y
    mem[0x0041] = 0x02
    mem[0x02A0] = 0x90  # Value for (indirect),Y

    # Execute and verify results
    cpu.step()  # LDA #$50
    assert cpu.A == 0x50

    cpu.step()  # CMP #$50
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$30
    assert cpu.A == 0x30

    cpu.step()  # CMP $10
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$80
    assert cpu.A == 0x80

    cpu.step()  # CMP $20,X
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$F0
    assert cpu.A == 0xF0

    cpu.step()  # CMP $0200
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$70
    assert cpu.A == 0x70

    cpu.step()  # CMP $0210,X
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$20
    assert cpu.A == 0x20

    cpu.step()  # CMP $0220,Y
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDX #$00
    assert cpu.X == 0x00

    cpu.step()  # LDA #$60
    assert cpu.A == 0x60

    cpu.step()  # CMP ($30,X)
    assert cpu.z == 1 and cpu.c == 1

    cpu.step()  # LDA #$90
    assert cpu.A == 0x90

    cpu.step()  # CMP ($40),Y
    assert cpu.z == 1 and cpu.c == 1


def test_JMP_page_border_bug():
    program = [
        0x6C, 0xFF, 0x00  # JMP $00FF (Absolute)
    ]

    jumped_program = [
        0xA9, 0x66,  # LDA #$66
    ]

    mem = Memory(
        [0xEA] * 0x0050 +
        program +
        [0xEA] * (0x0076 - (len(program) + 0x0050)) +
        jumped_program +
        [0xEA] * 0x0100
    )

    mem.data[0x00FF] = 0x76
    mem.data[0x0000] = 0x00
    mem.data[0x0100] = 0x10

    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0050  # Start execution

    cpu.step() # JMP ($00FF)
    assert cpu.PC == 0x0076

    cpu.step()
    assert cpu.PC == 0x0078
    assert cpu.A == 0x66


def test_PHA_PLA():
    program = [
        0xA9, 0x55,  # LDA #$55
        0x48,        # PHA        ; Push A onto stack
        0xA9, 0xAA,  # LDA #$AA
        0x68         # PLA        ; Pull A from stack (should restore $55)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    cpu.step()  # LDA #$55
    assert cpu.A == 0x55

    cpu.step()  # PHA (Push A to stack)

    cpu.step()  # LDA #$AA
    assert cpu.A == 0xAA

    cpu.step()  # PLA (Pull A from stack)
    assert cpu.A == 0x55  # Should restore original value


def test_JSR_RTS():
    program = [
        0x20, 0x05, 0x06,  # JSR $0605  (Jump to subroutine)
        0xA9, 0x11,        # LDA #$11   (Executed after subroutine returns)

        0xA9, 0x22,        # LDA #$22   (Subroutine: Load A with $22)
        0x60               # RTS        (Return to caller)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    cpu.step()  # JSR $0605
    assert cpu.PC == 0x0605  # Should jump to subroutine

    cpu.step()  # LDA #$22 (inside subroutine)
    assert cpu.A == 0x22

    cpu.step()  # RTS
    assert cpu.PC == 0x0603  # Should return to next instruction after JSR

    cpu.step()  # LDA #$11
    assert cpu.A == 0x11  # Should execute after returning from subroutine


def test_JSR_RTS_nested():
    program = [
        0x20, 0x05, 0x06,  # JSR $0605  (Jump to first subroutine)
        0xA9, 0x33,        # LDA #$33   (Executed after all subroutines return)

        # Subroutine 1
        0x20, 0x0B, 0x06,  # JSR $060B  (Call second subroutine)
        0xA9, 0x11,        # LDA #$11   (After returning from second subroutine)
        0x60,              # RTS        (Return to main program)

        # Subroutine 2
        0xA9, 0x22,        # LDA #$22   (Executed inside second subroutine)
        0x60               # RTS        (Return to first subroutine)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    cpu.step()  # JSR $0605 (First subroutine)
    assert cpu.PC == 0x0605  # Jumped to first subroutine

    cpu.step()  # JSR $060B (Second subroutine)
    assert cpu.PC == 0x060B  # Jumped to second subroutine

    cpu.step()  # LDA #$22 (Inside second subroutine)
    assert cpu.A == 0x22

    cpu.step()  # RTS (Return from second subroutine)
    assert cpu.PC == 0x0608  # Should return to instruction after JSR in first subroutine

    cpu.step()  # LDA #$11 (Inside first subroutine)
    assert cpu.A == 0x11

    cpu.step()  # RTS (Return from first subroutine)
    assert cpu.PC == 0x0603  # Should return to main program after JSR


def test_PHP_PLP():
    program = [
        0x38,        # SEC         (Set Carry Flag)
        0x08,        # PHP         (Push Processor Status onto Stack)
        0x18,        # CLC         (Clear Carry Flag)
        0x28         # PLP         (Pull Processor Status from Stack)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    # SEC: Set Carry Flag
    cpu.step()
    assert cpu.c == 1, "Carry flag should be set"

    # PHP: Push Processor Status onto Stack
    cpu.step()
    assert mem[0x0100 + cpu.S + 1] == 0b00011001, "Break and 5th flags should be set in stack copy"

    # CLC: Clear Carry Flag
    cpu.step()
    assert cpu.c == 0, "Carry flag should be cleared"

    # PLP: Pull Processor Status from Stack
    cpu.step()
    assert cpu.c == 1, "Carry flag should be restored"


def test_BIT():
    program = [
        0xA9, 0xFF,        # LDA #$FF   (Load A with all bits set)
        0x24, 0x10,        # BIT $10    (Zero-page mode)
        0x2C, 0x20, 0x06,  # BIT $0620  (Absolute mode)

        0xA9, 0x00,        # LDA #$00   (Load A with zero)
        0x24, 0x11,        # BIT $11    (Zero-page mode)
        0x2C, 0x21, 0x06   # BIT $0621  (Absolute mode)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600

    # Set up memory values for BIT tests
    mem[0x0010] = 0b11000000  # Zero-page: N=1, V=1, Z=0
    mem[0x0620] = 0b01000000  # Absolute: N=0, V=1, Z=0
    mem[0x0011] = 0b11000000  # Zero-page: N=1, V=1, Z=1 (A=0)
    mem[0x0621] = 0b00000000  # Absolute: N=0, V=0, Z=1 (A=0)

    # Load A with $FF and test BIT (zero-page)
    cpu.step()  # LDA #$FF
    assert cpu.A == 0xFF

    cpu.step()  # BIT $10 (zero-page)
    assert cpu.n == 1, "N flag should be set"
    assert cpu.v == 1, "V flag should be set"
    assert cpu.z == 0, "Z flag should NOT be set"

    cpu.step()  # BIT $0620 (absolute)
    assert cpu.n == 0, "N flag should be clear"
    assert cpu.v == 1, "V flag should be set"
    assert cpu.z == 0, "Z flag should NOT be set"

    # Load A with $00 and test BIT (zero-page)
    cpu.step()  # LDA #$00
    assert cpu.A == 0x00

    cpu.step()  # BIT $11 (zero-page)
    assert cpu.n == 1, "N flag should be set"
    assert cpu.v == 1, "V flag should be set"
    assert cpu.z == 1, "Z flag should be set"

    cpu.step()  # BIT $0621 (absolute)
    assert cpu.n == 0, "N flag should be clear"
    assert cpu.v == 0, "V flag should be clear"
    assert cpu.z == 1, "Z flag should be set"


def test_ASL():
    program = [
        0xA9, 0x40,        # LDA #$40   (Load A with $40)
        0x0A,              # ASL A      (Shift left in accumulator)

        0xA9, 0x80,        # LDA #$80   (Load A with $80)
        0x0A,              # ASL A      (Shift left in accumulator, should set carry)

        0xA9, 0x01,        # LDA #$01   (Load A with $01)
        0x85, 0x10,        # STA $10    (Store in zero-page)
        0x06, 0x10,        # ASL $10    (Shift left zero-page)

        0xA9, 0x02,        # LDA #$02   (Load A with $02)
        0x95, 0x20,        # STA $20,X  (Store at zero-page,X)
        0x16, 0x20,        # ASL $20,X  (Shift left zero-page,X)

        0xA9, 0x04,        # LDA #$04   (Load A with $04)
        0x8D, 0x30, 0x06,  # STA $0630  (Store in absolute memory)
        0x0E, 0x30, 0x06,  # ASL $0630  (Shift left absolute)

        0xA9, 0x08,        # LDA #$08   (Load A with $08)
        0x8D, 0x41, 0x06,  # STA $0641  (Store in absolute memory)
        0x1E, 0x40, 0x06   # ASL $0640,X (Shift left absolute,X)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600
    cpu.X = 0x01  # Set X register for indexed addressing

    # ASL A (accumulator)
    cpu.step()  # LDA #$40
    cpu.step()  # ASL A
    assert cpu.A == 0x80, "Accumulator should shift left to $80"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 1, "Negative flag should be set"
    assert cpu.z == 0, "Zero flag should be clear"

    cpu.step()  # LDA #$80
    cpu.step()  # ASL A
    assert cpu.A == 0x00, "Accumulator should shift left to $00"
    assert cpu.c == 1, "Carry should be set"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 1, "Zero flag should be set"

    # ASL $10 (zero-page)
    cpu.step()  # LDA #$01
    cpu.step()  # STA $10
    cpu.step()  # ASL $10
    assert mem[0x0010] == 0x02, "Memory at $10 should be $02 after shift"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 0, "Zero flag should be clear"

    # ASL $20,X (zero-page,X)
    cpu.step()  # LDA #$02
    cpu.step()  # STA $20,X
    cpu.step()  # ASL $20,X
    assert mem[0x0021] == 0x04, "Memory at $0021 should be $04 after shift"
    assert cpu.c == 0, "Carry should be clear"

    # ASL $0630 (absolute)
    cpu.step()  # LDA #$04
    cpu.step()  # STA $0630
    cpu.step()  # ASL $0630
    assert mem[0x0630] == 0x08, "Memory at $0630 should be $08 after shift"
    assert cpu.c == 0, "Carry should be clear"

    # ASL $0640,X (absolute,X)
    cpu.step()  # LDA #$08
    cpu.step()  # STA $0641
    cpu.step()  # ASL $0640,X
    assert mem[0x0641] == 0x10, "Memory at $0641 should be $10 after shift"
    assert cpu.c == 0, "Carry should be clear"


def test_LSR():
    program = [
        0xA9, 0x80,        # LDA #$80   (Load A with $80)
        0x4A,              # LSR A      (Shift right in accumulator)

        0xA9, 0x01,        # LDA #$01   (Load A with $01)
        0x4A,              # LSR A      (Shift right in accumulator, should set carry)

        0xA9, 0x04,        # LDA #$04   (Load A with $04)
        0x85, 0x10,        # STA $10    (Store in zero-page)
        0x46, 0x10,        # LSR $10    (Shift right zero-page)

        0xA9, 0x08,        # LDA #$08   (Load A with $08)
        0x95, 0x20,        # STA $20,X  (Store at zero-page,X)
        0x56, 0x20,        # LSR $20,X  (Shift right zero-page,X)

        0xA9, 0x10,        # LDA #$10   (Load A with $10)
        0x8D, 0x30, 0x06,  # STA $0630  (Store in absolute memory)
        0x4E, 0x30, 0x06,  # LSR $0630  (Shift right absolute)

        0xA9, 0x20,        # LDA #$20   (Load A with $20)
        0x8D, 0x41, 0x06,  # STA $0641  (Store in absolute memory)
        0x5E, 0x40, 0x06   # LSR $0640,X (Shift right absolute,X)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600
    cpu.X = 0x01  # Set X register for indexed addressing

    # LSR A (accumulator)
    cpu.step()  # LDA #$80
    cpu.step()  # LSR A
    assert cpu.A == 0x40, "Accumulator should shift right to $40"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 0, "Zero flag should be clear"

    cpu.step()  # LDA #$01
    cpu.step()  # LSR A
    assert cpu.A == 0x00, "Accumulator should shift right to $00"
    assert cpu.c == 1, "Carry should be set"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 1, "Zero flag should be set"

    # LSR $10 (zero-page)
    cpu.step()  # LDA #$04
    cpu.step()  # STA $10
    cpu.step()  # LSR $10
    assert mem[0x0010] == 0x02, "Memory at $10 should be $02 after shift"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 0, "Zero flag should be clear"

    # LSR $20,X (zero-page,X)
    cpu.step()  # LDA #$08
    cpu.step()  # STA $20,X
    cpu.step()  # LSR $20,X
    assert mem[0x0021] == 0x04, "Memory at $0021 should be $04 after shift"
    assert cpu.c == 0, "Carry should be clear"

    # LSR $0630 (absolute)
    cpu.step()  # LDA #$10
    cpu.step()  # STA $0630
    cpu.step()  # LSR $0630
    assert mem[0x0630] == 0x08, "Memory at $0630 should be $08 after shift"
    assert cpu.c == 0, "Carry should be clear"

    # LSR $0640,X (absolute,X)
    cpu.step()  # LDA #$20
    cpu.step()  # STA $0641
    cpu.step()  # LSR $0640,X
    assert mem[0x0641] == 0x10, "Memory at $0641 should be $10 after shift"
    assert cpu.c == 0, "Carry should be clear"


def test_ROR():
    program = [
        0xA9, 0x80,        # LDA #$80   (Load A with $80)
        0x6A,              # ROR A      (Rotate right in accumulator)

        0xA9, 0x01,        # LDA #$01   (Load A with $01)
        0x6A,              # ROR A      (Rotate right in accumulator, should set carry)

        0xA9, 0x04,        # LDA #$04   (Load A with $04)
        0x85, 0x10,        # STA $10    (Store in zero-page)
        0x66, 0x10,        # ROR $10    (Rotate right zero-page)

        0xA9, 0x08,        # LDA #$08   (Load A with $08)
        0x95, 0x20,        # STA $20,X  (Store at zero-page,X)
        0x76, 0x20,        # ROR $20,X  (Rotate right zero-page,X)

        0xA9, 0x10,        # LDA #$10   (Load A with $10)
        0x8D, 0x30, 0x06,  # STA $0630  (Store in absolute memory)
        0x6E, 0x30, 0x06,  # ROR $0630  (Rotate right absolute)

        0xA9, 0x20,        # LDA #$20   (Load A with $20)
        0x8D, 0x41, 0x06,  # STA $0641  (Store in absolute memory)
        0x7E, 0x40, 0x06   # ROR $0640,X (Rotate right absolute,X)
    ]

    mem = Memory([0xEA] * 0x600 + program + [0xEA] * (0x1000 - len(program)))
    bus = Bus(mem)
    cpu = CPU(bus)
    cpu.PC = 0x0600
    cpu.X = 0x01  # Set X register for indexed addressing

    # ROR A (accumulator)
    cpu.step()  # LDA #$80
    cpu.step()  # ROR A
    assert cpu.A == 0x40, "Accumulator should rotate right to $40"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 0, "Zero flag should be clear"

    cpu.step()  # LDA #$01
    cpu.step()  # ROR A
    assert cpu.A == 0x00, "Accumulator should rotate right to $00"
    assert cpu.c == 1, "Carry should be set"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 1, "Zero flag should be set"

    cpu.c = 0
    # ROR $10 (zero-page)
    cpu.step()  # LDA #$04
    cpu.step()  # STA $10
    cpu.step()  # ROR $10
    assert mem[0x0010] == 0x02, "Memory at $10 should be $02 after rotate"
    assert cpu.c == 0, "Carry should be clear"
    assert cpu.n == 0, "Negative flag should be clear"
    assert cpu.z == 0, "Zero flag should be clear"

    # ROR $20,X (zero-page,X)
    cpu.step()  # LDA #$08
    cpu.step()  # STA $20,X
    cpu.step()  # ROR $20,X
    assert mem[0x0021] == 0x04, "Memory at $0021 should be $04 after rotate"
    assert cpu.c == 0, "Carry should be clear"

    # ROR $0630 (absolute)
    cpu.step()  # LDA #$10
    cpu.step()  # STA $0630
    cpu.step()  # ROR $0630
    assert mem[0x0630] == 0x08, "Memory at $0630 should be $08 after rotate"
    assert cpu.c == 0, "Carry should be clear"

    # ROR $0640,X (absolute,X)
    cpu.step()  # LDA #$20
    cpu.step()  # STA $0641
    cpu.step()  # ROR $0640,X
    assert mem[0x0641] == 0x10, "Memory at $0641 should be $10 after rotate"
    assert cpu.c == 0, "Carry should be clear"

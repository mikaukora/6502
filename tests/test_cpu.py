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
    assert cpu.b == 0
    assert cpu.d == 0
    assert cpu.i == 0
    assert cpu.z == 0
    assert cpu.c == 0

    cpu.P = 0xFF
    assert cpu.n == 1
    assert cpu.v == 1
    assert cpu.b == 1
    assert cpu.d == 1
    assert cpu.i == 1
    assert cpu.z == 1
    assert cpu.c == 1

    cpu.P = 0x00
    cpu.n = 1
    assert cpu.P == 0x80
    cpu.v = 1
    assert cpu.P == 0xC0
    cpu.b = 1
    assert cpu.P == 0xD0
    cpu.d = 1
    assert cpu.P == 0xD8
    cpu.i = 1
    assert cpu.P == 0xDC
    cpu.z = 1
    assert cpu.P == 0xDE
    cpu.c = 1
    assert cpu.P == 0xDF

    cpu.P = 0xFF
    cpu.n = 0
    assert cpu.P == 0x7F
    cpu.v = 0
    assert cpu.P == 0x3F
    cpu.b = 0
    assert cpu.P == 0x2F  # unused bit (5) is set
    cpu.d = 0
    assert cpu.P == 0x27
    cpu.i = 0
    assert cpu.P == 0x23
    cpu.z = 0
    assert cpu.P == 0x21
    cpu.c = 0
    assert cpu.P == 0x20


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
    assert memory.data[0x08] == 0xEA

    cpu.step()
    assert memory.data[0x09] == 0xEA

    cpu.step()
    assert memory.data[0x0A] == 0xEA


def test_STY_ZPG():
    memory = Memory([0xA0, 0xEA, 0x84, 0x08, 0x84, 0x09, 0x84, 0x0A, 0x22, 0x22, 0x22])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.Y == 0xEA

    cpu.step()
    assert memory.data[0x08] == 0xEA

    cpu.step()
    assert memory.data[0x09] == 0xEA

    cpu.step()
    assert memory.data[0x0A] == 0xEA


def test_STX_ZPG():
    memory = Memory([0xA2, 0xEA, 0x86, 0x08, 0x86, 0x09, 0x86, 0x0A, 0x22, 0x22, 0x22])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0xEA

    cpu.step()
    assert memory.data[0x08] == 0xEA

    cpu.step()
    assert memory.data[0x09] == 0xEA

    cpu.step()
    assert memory.data[0x0A] == 0xEA


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
    assert memory.data[0x08] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x08] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x08] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x08] == 0x00
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
    assert memory.data[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory.data[(0x00 << 8) + 0x07] == 0xEA


def test_STX_ABS():
    memory = Memory([0x8E, 0x06, 0x00, 0x8E, 0x07, 0x00, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.X = 0xEA

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory.data[(0x00 << 8) + 0x07] == 0xEA


def test_STY_ABS():
    memory = Memory([0x8C, 0x06, 0x00, 0x8C, 0x07, 0x00, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.Y = 0xEA

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x06] == 0xEA
    cpu.step()
    assert memory.data[(0x00 << 8) + 0x07] == 0xEA


def test_DEC_INC_ABS():
    memory = Memory(
        [0xCE, 0x0C, 0x00, 0xCE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0x00]
    )
    bus = Bus(memory)
    cpu = CPU(bus)
    cpu.Y = 0

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x0C] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x0C] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x0C] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[(0x00 << 8) + 0x0C] == 0x00
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
    assert memory.data[0x08] == 0x55


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
    assert memory.data[0x08] == 0x55


def test_DEC_INC_ZPG_X():
    memory = Memory([0xA2, 0x0A, 0xD6, 0x00, 0xD6, 0x00, 0xF6, 0x00, 0xF6, 0x00, 0x00])
    bus = Bus(memory)
    cpu = CPU(bus)

    cpu.step()
    assert cpu.X == 0x0A

    cpu.step()
    assert memory.data[0x0A] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x0A] == 0xFE
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x0A] == 0xFF
    assert cpu.z == 0
    assert cpu.n == 1

    cpu.step()
    assert memory.data[0x0A] == 0x00
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
    assert memory.data[0x0C] == 0xEA

    cpu.step()
    assert cpu.Y == 0x0D

    cpu.step()
    assert memory.data[0x0D] == 0xEA

    cpu.step()
    assert cpu.Y == 0x0E

    cpu.step()
    assert memory.data[0x0E] == 0xEA


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
    assert memory.data[(0x01 << 8) + 0x00] == 0x00
    cpu.step()
    assert memory.data[(0x02 << 8) + 0x00] == 0x00
    cpu.step()
    assert memory.data[(0x01 << 8) + 0x0F] == 0x00
    cpu.step()
    assert memory.data[(0x02 << 8) + 0x0F] == 0x00


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
    memory.data[(0x01 << 8) + 0x00] = 0x0F
    memory.data[(0x01 << 8) + 0x01] = 0x0E
    memory.data[(0x01 << 8) + 0x02] = 0x10
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
    memory.data[(0x01 << 8) + 0x00] = 0x0F
    memory.data[(0x01 << 8) + 0x01] = 0x0E
    memory.data[(0x01 << 8) + 0x02] = 0x10
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

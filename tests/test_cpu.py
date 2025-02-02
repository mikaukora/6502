from src.main import CPU, Bus, Memory


def test_registers():
    cpu = CPU()

    cpu.P = 0x00
    assert cpu.P == 0

    cpu.P = 0xFFFF
    assert cpu.P == 0x7F

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
    assert cpu.P == 0x40
    cpu.v = 1
    assert cpu.P == 0x60
    cpu.b = 1
    assert cpu.P == 0x70
    cpu.d = 1
    assert cpu.P == 0x78
    cpu.i = 1
    assert cpu.P == 0x7C
    cpu.z = 1
    assert cpu.P == 0x7E
    cpu.c = 1
    assert cpu.P == 0x7F

    cpu.P = 0x7F
    cpu.n = 0
    assert cpu.P == 0x3F
    cpu.v = 0
    assert cpu.P == 0x1F
    cpu.b = 0
    assert cpu.P == 0x0F
    cpu.d = 0
    assert cpu.P == 0x07
    cpu.i = 0
    assert cpu.P == 0x03
    cpu.z = 0
    assert cpu.P == 0x01
    cpu.c = 0
    assert cpu.P == 0x00


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

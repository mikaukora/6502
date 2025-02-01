from instructions import decode_standard, i, m


def uint8(value: int) -> int:
    return value & 0xFF


def uint16(value: int) -> int:
    return value & 0xFFFF


def toUint16(high: int, low: int) -> int:
    return uint16(high << 8 + low)


def bit(value: int) -> int:
    return value & 0x01


class Memory:
    def __init__(self, data: bytearray):
        self.data = data

    def __str__(self):
        return str([f"{x:02x}" for x in self.data])

    def read(self, address):
        print(f"R {address:#06x}: {self.data[address]:x}")
        return self.data[address]

    def write(self, address, value):
        self.data[address] = value
        print(f"W {address:#06x}: {self.data[address]:x}")


class Bus:
    def __init__(self, memory):
        self.address = None
        self.data = None
        self.memory = memory

    def memory_read(self):
        self.data = self.memory.read(self.address)
        return self.data

    def memory_write(self, value):
        self.data = value
        self.memory.write(self.address, self.data)


class CPU:
    def __init__(self, bus=None):
        self._A = 0x00  # accumulator
        self._P = 0x00  # status register, 7-bit
        self._n = 0b0  # negative
        self._v = 0b0  # overflow
        self._b = 0b0  # break
        self._d = 0b0  # decimal
        self._i = 0b0  # interrupt disable
        self._z = 0b0  # zero
        self._c = 0b0  # carry
        self._PC = 0x0000  # program counter - 16-bit
        self._S = 0x00  # stack pointer
        self._X = 0x00  # index register X
        self._Y = 0x00  # index register Y
        self.bus = bus
        self.instruction = None
        self.addressing_mode = None

    def fetch(self):
        self.bus.address = self.PC
        self.data = self.bus.memory_read()
        self.PC += 1

    def write(self, address, value):
        self.bus.address = address
        self.bus.memory_write(value)

    def decode(self):
        self.instruction, self.addressing_mode = decode_standard(self.data)

    def calc_z(self, data):
        return 1 if data == 0 else 0

    def calc_n(self, data):
        return (data >> 7) & 1

    def execute(self):
        match self.instruction:
            case i.LDA:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.A = self.data
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.LDX:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.X = self.data
                    self.z = self.calc_z(self.X)
                    self.n = self.calc_n(self.X)
            case i.LDY:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.Y = self.data
                    self.z = self.calc_z(self.Y)
                    self.n = self.calc_n(self.Y)
            case i.STA:
                if self.addressing_mode == m.ZPG:
                    self.fetch()
                    self.write(self.data, self.A)
            case i.STX:
                if self.addressing_mode == m.ZPG:
                    self.fetch()
                    self.write(self.data, self.X)
            case i.STY:
                if self.addressing_mode == m.ZPG:
                    self.fetch()
                    self.write(self.data, self.Y)
            case i.TAX:
                if self.addressing_mode == m.IMPL:
                    self.X = self.A
                    self.z = self.calc_z(self.X)
                    self.n = self.calc_n(self.X)
            case i.TAY:
                if self.addressing_mode == m.IMPL:
                    self.Y = self.A
                    self.z = self.calc_z(self.Y)
                    self.n = self.calc_n(self.Y)
            case i.TSX:
                self.X = self.S
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.TXA:
                if self.addressing_mode == m.IMPL:
                    self.A = self.X
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.TXS:
                self.S = self.X
            case i.TYA:
                if self.addressing_mode == m.IMPL:
                    self.A = self.Y
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.NOP:
                return
            case i.CLC:
                if self.addressing_mode == m.IMPL:
                    self.c = 0

    """
        Starts from the address in PC.
    """

    def step(self, cycles=1):
        for _ in range(cycles):
            self.fetch()
            self.decode()
            self.execute()

    def reset(self):
        # TODO: start sequence, read reset vector, jump
        pass

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        self._A = uint8(value)

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        self._X = uint8(value)

    @property
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, value):
        self._Y = uint8(value)

    @property
    def PC(self):
        return self._PC

    @PC.setter
    def PC(self, value):
        self._PC = uint16(value)

    @property
    def S(self):
        return self._S

    @S.setter
    def S(self, value):
        self._S = uint8(value)

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, value):
        self._P = uint8(value) & 0x7F

    @property
    def n(self):
        return self._P >> 6 & 0x01

    @n.setter
    def n(self, value):
        self._P = self._P & ~(1 << 6) | bit(value) << 6

    @property
    def v(self):
        return self._P >> 5 & 0x01

    @v.setter
    def v(self, value):
        self._P = self._P & ~(1 << 5) | bit(value) << 5

    @property
    def b(self):
        return self._P >> 4 & 0x01

    @b.setter
    def b(self, value):
        self._P = self._P & ~(1 << 4) | bit(value) << 4

    @property
    def d(self):
        return self._P >> 3 & 0x01

    @d.setter
    def d(self, value):
        self._P = self._P & ~(1 << 3) | bit(value) << 3

    @property
    def i(self):
        return self._P >> 2 & 0x01

    @i.setter
    def i(self, value):
        self._P = self._P & ~(1 << 2) | bit(value) << 2

    @property
    def z(self):
        return self._P >> 1 & 0x01

    @z.setter
    def z(self, value):
        self._P = self._P & ~(1 << 1) | bit(value) << 1

    @property
    def c(self):
        return self._P & 0x01

    @c.setter
    def c(self, value):
        self._P = self._P & ~(1) | bit(value)

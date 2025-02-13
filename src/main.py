import sys
from instructions import decode_standard, i, m


def uint8(value: int) -> int:
    return value & 0xFF


def uint16(value: int) -> int:
    return value & 0xFFFF


def toUint16(high: int, low: int) -> int:
    return uint16((high << 8) + low)


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

    def dump(self):
        for index in range(0, len(self.data), 16):
            print(
                f"{index:04x}\t{' '.join(f'{x:02x}' for x in self.data[index : index + 16])}"
            )


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

    def __str__(self):
        GREEN = "\033[92m"
        RESET = "\033[0m"
        return (
            f"{GREEN}"
            f"A: {cpu.A:#04x}\tX: {cpu.X:#04x}\tY: {cpu.Y:#04x}\tS: {cpu.S:#04x}\n"
            f"P: {cpu.P:#04x}\t"
            f"Z: {cpu.z} "
            f"N: {cpu.n} "
            f"V: {cpu.v} "
            f"B: {cpu.b} "
            f"D: {cpu.d} "
            f"I: {cpu.i} "
            f"C: {cpu.c}\n"
            f"PC: {cpu.PC:#06x}"
            f"{RESET}"
        )

    def fetch(self):
        self.bus.address = self.PC
        self.data = self.bus.memory_read()
        self.PC += 1

    def read(self, address):
        self.bus.address = address
        return self.bus.memory_read()

    def write(self, address, value):
        self.bus.address = address
        self.bus.memory_write(value)

    def decode(self):
        self.instruction, self.addressing_mode = decode_standard(self.data)

    def calc_z(self, data):
        return 1 if data == 0 else 0

    def calc_n(self, data):
        return (data >> 7) & 1

    def get_data(self):
        self.fetch()
        if self.addressing_mode == m.IMM:
            return self.data
        elif self.addressing_mode == m.ZPG:
            return self.read(self.data)
        elif self.addressing_mode == m.ZPG_X:
            return self.read(uint8(self.data + self.X))
        elif self.addressing_mode == m.ZPG_Y:
            return self.read(uint8(self.data + self.Y))
        elif self.addressing_mode == m.ABS:
            ll = self.data
            self.fetch()
            hh = self.data
            return self.read(toUint16(hh, ll))
        elif self.addressing_mode == m.ABS_X:
            ll = self.data
            self.fetch()
            hh = self.data
            return self.read(toUint16(hh, ll) + self.X)
        elif self.addressing_mode == m.ABS_Y:
            ll = self.data
            self.fetch()
            hh = self.data
            return self.read(toUint16(hh, ll) + self.Y)

    def put_data(self):
        self.fetch()
        if self.addressing_mode == m.ZPG:
            return self.data
        elif self.addressing_mode == m.ABS:
            ll = self.data
            self.fetch()
            hh = self.data
            return toUint16(hh, ll)
        elif self.addressing_mode == m.ZPG_X:
            return uint8(self.data + self.X)
        elif self.addressing_mode == m.ZPG_Y:
            return uint8(self.data + self.Y)

    def execute(self):
        match self.instruction:
            case i.LDA:
                self.A = self.get_data()
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.LDX:
                self.X = self.get_data()
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.LDY:
                self.Y = self.get_data()
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.STA:
                self.write(self.put_data(), self.A)
            case i.STX:
                self.write(self.put_data(), self.X)
            case i.STY:
                self.write(self.put_data(), self.Y)
            case i.TAX:
                self.X = self.A
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.TAY:
                self.Y = self.A
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.TSX:
                self.X = self.S
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.TXA:
                self.A = self.X
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.TXS:
                self.S = self.X
            case i.TYA:
                self.A = self.Y
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.NOP:
                return
            case i.CLC:
                self.c = 0
            case i.CLD:
                self.d = 0
            case i.CLI:
                self.i = 0
            case i.CLV:
                self.v = 0
            case i.SEC:
                self.c = 1
            case i.SED:
                self.d = 1
            case i.SEI:
                self.i = 1
            case i.INX:
                self.X = (self.X + 1) % 0x100
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.INY:
                self.Y = (self.Y + 1) % 0x100
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.DEX:
                self.X = (self.X - 1) % 0x100
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.DEY:
                self.Y = (self.Y - 1) % 0x100
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.DEC:
                if self.addressing_mode == m.ZPG:
                    self.fetch()
                    dst = self.data
                    value = self.read(dst)
                    value = (value - 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
                elif self.addressing_mode == m.ABS:
                    self.fetch()
                    ll = self.data
                    self.fetch()
                    hh = self.data
                    value = self.read(toUint16(hh, ll))
                    value = (value - 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(toUint16(hh, ll), value)
                elif self.addressing_mode == m.ZPG_X:
                    self.fetch()
                    dst = (self.data + self.X) & 0xFF
                    value = self.read(dst)
                    value = (value - 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.INC:
                if self.addressing_mode == m.ZPG:
                    self.fetch()
                    dst = self.data
                    value = self.read(dst)
                    value = (value + 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
                elif self.addressing_mode == m.ABS:
                    self.fetch()
                    ll = self.data
                    self.fetch()
                    hh = self.data
                    value = self.read(toUint16(hh, ll))
                    value = (value + 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(toUint16(hh, ll), value)
                elif self.addressing_mode == m.ZPG_X:
                    self.fetch()
                    dst = (self.data + self.X) & 0xFF
                    value = self.read(dst)
                    value = (value + 1) % 0x100
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.CMP:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    value = self.data
                    result = self.A - value
                    self.c = 1 if self.A >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
            case i.CPX:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    value = self.data
                    result = self.X - value
                    self.c = 1 if self.X >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
                elif self.addressing_mode == m.ZPG:
                    self.fetch()
                    value = self.read(self.data)
                    result = self.X - value
                    self.c = 1 if self.X >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
                elif self.addressing_mode == m.ABS:
                    self.fetch()
                    ll = self.data
                    self.fetch()
                    hh = self.data
                    value = self.read(toUint16(hh, ll))
                    result = self.X - value
                    self.c = 1 if self.X >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
            case i.CPY:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    value = self.data
                    result = self.Y - value
                    self.c = 1 if self.Y >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
                elif self.addressing_mode == m.ZPG:
                    self.fetch()
                    value = self.read(self.data)
                    result = self.Y - value
                    self.c = 1 if self.Y >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
                elif self.addressing_mode == m.ABS:
                    self.fetch()
                    ll = self.data
                    self.fetch()
                    hh = self.data
                    value = self.read(toUint16(hh, ll))
                    result = self.Y - value
                    self.c = 1 if self.Y >= value else 0
                    self.z = self.calc_z(result)
                    self.n = self.calc_n(result)
            case i.JMP:
                if self.addressing_mode == m.ABS:
                    self.fetch()
                    ll = self.data
                    self.fetch()
                    hh = self.data
                    self.PC = toUint16(hh, ll)
            case i.BEQ:
                self.fetch()
                offset = self.data
                if self.z == 1:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.BNE:
                self.fetch()
                offset = self.data
                if self.z == 0:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.BMI:
                self.fetch()
                offset = self.data
                if self.n == 1:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.BPL:
                self.fetch()
                offset = self.data
                if self.n == 0:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.BCS:
                self.fetch()
                offset = self.data
                if self.c == 1:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.BCC:
                self.fetch()
                offset = self.data
                if self.c == 0:
                    self.PC = (self.PC + offset) & 0xFFFF
            case i.AND:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.A = self.A & self.data
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.ORA:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.A = self.A | self.data
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.EOR:
                if self.addressing_mode == m.IMM:
                    self.fetch()
                    self.A = self.A ^ self.data
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)

    """
        Starts from the address in PC.
    """

    def step(self, cycles=1):
        for _ in range(cycles):
            self.fetch()
            self.decode()
            self.execute()

    def run(self):
        mem_end = len(self.bus.memory.data)
        while self.PC < mem_end:
            self.fetch()
            self.decode()
            self.execute()
        print("End of program")

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
        self._P = uint8(value) & 0xFF

    @property
    def n(self):
        return (self._P >> 7) & 0x01

    @n.setter
    def n(self, value):
        self._P = self._P & ~(1 << 7) | bit(value) << 7

    @property
    def v(self):
        return (self._P >> 6) & 0x01

    @v.setter
    def v(self, value):
        self._P = self._P & ~(1 << 6) | bit(value) << 6

    @property
    def b(self):
        return (self._P >> 4) & 0x01

    @b.setter
    def b(self, value):
        self._P = self._P & ~(1 << 4) | bit(value) << 4

    @property
    def d(self):
        return (self._P >> 3) & 0x01

    @d.setter
    def d(self, value):
        self._P = self._P & ~(1 << 3) | bit(value) << 3

    @property
    def i(self):
        return (self._P >> 2) & 0x01

    @i.setter
    def i(self, value):
        self._P = self._P & ~(1 << 2) | bit(value) << 2

    @property
    def z(self):
        return (self._P >> 1) & 0x01

    @z.setter
    def z(self, value):
        self._P = self._P & ~(1 << 1) | bit(value) << 1

    @property
    def c(self):
        return self._P & 0x01

    @c.setter
    def c(self, value):
        self._P = self._P & ~(1) | bit(value)


if __name__ == "__main__":
    filename = len(sys.argv) > 1 and sys.argv[1] or None
    if not filename:
        print("Error: Missing filename")
        sys.exit(1)
    print(f"Using file {filename}")

    try:
        data = bytearray(open(filename, "rb").read())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    memory = Memory(bytearray(data))
    memory.dump()
    bus = Bus(memory)
    cpu = CPU(bus)
    print(cpu)
    cpu.run()
    print(cpu)
    memory.dump()

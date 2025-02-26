from src.instructions import decode_standard, i, m


def uint8(value: int) -> int:
    return value & 0xFF


def uint16(value: int) -> int:
    return value & 0xFFFF


def toUint16(high: int, low: int) -> int:
    return uint16((high << 8) + low)


def bit(value: int) -> int:
    return value & 0x01


def toInt8(value: int) -> int:
    # 0x80 (128) -> -128, 0xFF (256) -> -1
    return value if value < 0x80 else value - 0x100


class Memory:
    def __init__(self, data: bytearray):
        self.data = data

    def __str__(self):
        return str([f"{x:02x}" for x in self.data])

    def __setitem__(self, address, value):
        self.data[address] = value
        print(f"W {address:#06x}: {self.data[address]:x}")

    def __getitem__(self, address):
        print(f"R {address:#06x}: {self.data[address]:x}")
        return self.data[address]

    def dump(self, start=0, end=None):
        if end is None:
            end = len(self.data)

        for index in range(start, end, 16):
            print(
                f"{index:04x}\t{' '.join(f'{x:02x}' for x in self.data[index : index + 16])}"
            )


class Bus:
    def __init__(self, memory):
        self.address = None
        self.data = None
        self.memory = memory

    def memory_read(self):
        self.data = self.memory[self.address]
        return self.data

    def memory_write(self, value):
        self.data = value
        self.memory[self.address] = self.data


class CPU:
    def __init__(self, bus=None):
        self._A = 0x00  # accumulator
        self._P = 0x00  # status register, 7-bit
        self._n = 0b0  # negative
        self._v = 0b0  # overflow
        self._d = 0b0  # decimal
        self._i = 0b0  # interrupt disable
        self._z = 0b0  # zero
        self._c = 0b0  # carry
        self._PC = 0x0000  # program counter - 16-bit
        self._S = 0xFF  # stack pointer
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
            f"A: {self.A:#04x}\tX: {self.X:#04x}\tY: {self.Y:#04x}\tS: {self.S:#04x}\n"
            f"P: {self.P:#04x}\t"
            f"Z: {self.z} "
            f"N: {self.n} "
            f"V: {self.v} "
            f"D: {self.d} "
            f"I: {self.i} "
            f"C: {self.c}\n"
            f"PC: {self.PC:#06x}"
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

    """
        Fetches the data based on the addressing mode.
    """

    def get_data(self):
        self.fetch()
        if self.addressing_mode == m.IMM:
            return self.data
        elif self.addressing_mode == m.REL:
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
        elif self.addressing_mode == m.IND_X:
            ll = self.read(uint8(self.data + self.X))
            hh = self.read(uint8(self.data + self.X + 1))
            return self.read(toUint16(hh, ll))
        elif self.addressing_mode == m.IND_Y:
            ll = self.read(self.data)
            hh = self.read(uint8(self.data + 1))
            return self.read(toUint16(hh, ll) + self.Y)
        else:
            raise NotImplementedError("Unknown addressing mode")

    """
        Fetches the address based on the addressing mode.
    """

    def get_addr(self):
        self.fetch()
        if self.addressing_mode == m.ZPG:
            return self.data
        elif self.addressing_mode == m.ABS:
            ll = self.data
            self.fetch()
            hh = self.data
            return toUint16(hh, ll)
        elif self.addressing_mode == m.ABS_X:
            ll = self.data
            self.fetch()
            hh = self.data
            return toUint16(hh, ll) + self.X
        elif self.addressing_mode == m.ABS_Y:
            ll = self.data
            self.fetch()
            hh = self.data
            return toUint16(hh, ll) + self.Y
        elif self.addressing_mode == m.ZPG_X:
            return uint8(self.data + self.X)
        elif self.addressing_mode == m.ZPG_Y:
            return uint8(self.data + self.Y)
        elif self.addressing_mode == m.IND:
            ll = self.data
            self.fetch()
            hh = self.data
            target_ll = self.read(toUint16(hh, ll))
            # introduce a bug, hh is not incremented by the CPU
            target_hh = self.read(toUint16(hh, uint8(ll + 1)))
            return toUint16(target_hh, target_ll)
        elif self.addressing_mode == m.IND_X:
            ll = self.read(uint8(self.data + self.X))
            hh = self.read(uint8(self.data + self.X + 1))
            return toUint16(hh, ll)
        elif self.addressing_mode == m.IND_Y:
            ll = self.read(uint8(self.data))
            hh = self.read(uint8(self.data + 1))
            return toUint16(hh, ll) + self.Y
        else:
            raise NotImplementedError("Unknown addressing mode")

    def stack_push(self, value):
        self.write(0x0100 + self.S, value)
        self.S = uint8(self.S - 1)

    def stack_pop(self):
        self.S = uint8(self.S + 1)
        return self.read(0x0100 + self.S)

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
                self.write(self.get_addr(), self.A)
            case i.STX:
                self.write(self.get_addr(), self.X)
            case i.STY:
                self.write(self.get_addr(), self.Y)
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
                self.X = uint8(self.X + 1)
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.INY:
                self.Y = uint8(self.Y + 1)
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.DEX:
                self.X = uint8(self.X - 1)
                self.z = self.calc_z(self.X)
                self.n = self.calc_n(self.X)
            case i.DEY:
                self.Y = uint8(self.Y - 1)
                self.z = self.calc_z(self.Y)
                self.n = self.calc_n(self.Y)
            case i.DEC:
                dst = self.get_addr()
                value = self.read(dst)
                value = uint8(value - 1)
                self.z = self.calc_z(value)
                self.n = self.calc_n(value)
                self.write(dst, value)
            case i.INC:
                dst = self.get_addr()
                value = self.read(dst)
                value = uint8(value + 1)
                self.z = self.calc_z(value)
                self.n = self.calc_n(value)
                self.write(dst, value)
            case i.CMP:
                value = self.get_data()
                result = self.A - value
                self.c = 1 if self.A >= value else 0
                self.z = self.calc_z(result)
                self.n = self.calc_n(result)
            case i.CPX:
                value = self.get_data()
                result = self.X - value
                self.c = 1 if self.X >= value else 0
                self.z = self.calc_z(result)
                self.n = self.calc_n(result)
            case i.CPY:
                value = self.get_data()
                result = self.Y - value
                self.c = 1 if self.Y >= value else 0
                self.z = self.calc_z(result)
                self.n = self.calc_n(result)
            case i.JMP:
                self.PC = self.get_addr()
            case i.BEQ:
                offset = toInt8(self.get_data())
                if self.z == 1:
                    self.PC = uint16(self.PC + offset)
            case i.BNE:
                offset = toInt8(self.get_data())
                if self.z == 0:
                    self.PC = uint16(self.PC + offset)
            case i.BMI:
                offset = toInt8(self.get_data())
                if self.n == 1:
                    self.PC = uint16(self.PC + offset)
            case i.BPL:
                offset = toInt8(self.get_data())
                if self.n == 0:
                    self.PC = uint16(self.PC + offset)
            case i.BCS:
                offset = toInt8(self.get_data())
                if self.c == 1:
                    self.PC = uint16(self.PC + offset)
            case i.BCC:
                offset = toInt8(self.get_data())
                if self.c == 0:
                    self.PC = uint16(self.PC + offset)
            case i.BVC:
                offset = toInt8(self.get_data())
                if self.v == 0:
                    self.PC = uint16(self.PC + offset)
            case i.BVS:
                offset = toInt8(self.get_data())
                if self.v == 1:
                    self.PC = uint16(self.PC + offset)
            case i.AND:
                self.A = self.A & self.get_data()
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.ORA:
                self.A = self.A | self.get_data()
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.EOR:
                self.A = self.A ^ self.get_data()
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.PHA:
                self.stack_push(self.A)
            case i.PLA:
                self.A = self.stack_pop()
                self.z = self.calc_z(self.A)
                self.n = self.calc_n(self.A)
            case i.JSR:
                addr = uint16(self.PC + 2)
                self.stack_push(uint8(addr >> 8))
                self.stack_push(uint8(addr))
                self.PC = self.get_addr()
            case i.RTS:
                ll = self.stack_pop()
                hh = self.stack_pop()
                self.PC = toUint16(hh, ll)
            case i.PHP:
                self.stack_push(self.P | 0x18)
            case i.PLP:
                self.P = self.stack_pop() & ~(0x18)
            case i.BIT:
                value = self.get_data()
                self.n = (value >> 7) & 0x01
                self.v = (value >> 6) & 0x01
                self.z = (value & self.A) == 0
            case i.ASL:
                if self.addressing_mode == m.A:
                    self.c = (self.A >> 7) & 0x01
                    self.A = uint8(self.A << 1)
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    dst = self.get_addr()
                    value = self.read(dst)
                    self.c = (value >> 7) & 0x01
                    value = uint8(value << 1)
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.LSR:
                if self.addressing_mode == m.A:
                    self.c = self.A & 0x01
                    self.A = uint8(self.A >> 1)
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    dst = self.get_addr()
                    value = self.read(dst)
                    self.c = value & 0x01
                    value = uint8(value >> 1)
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.ROR:
                if self.addressing_mode == m.A:
                    lsb = self.A & 0x01
                    self.A = ((self.c & 0x01) << 7) | uint8(self.A >> 1)
                    self.c = lsb
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    dst = self.get_addr()
                    value = self.read(dst)
                    lsb = value & 0x01
                    value = ((self.c & 0x01) << 7) | uint8(value >> 1)
                    self.c = lsb
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.ROL:
                if self.addressing_mode == m.A:
                    msb = (self.A >> 7) & 0x01
                    self.A = uint8(self.A << 1) | (self.c & 0x01)
                    self.c = msb
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    dst = self.get_addr()
                    value = self.read(dst)
                    msb = (value >> 7) & 0x01
                    value = uint8(value << 1) | (self.c & 0x01)
                    self.c = msb
                    self.z = self.calc_z(value)
                    self.n = self.calc_n(value)
                    self.write(dst, value)
            case i.ADC:
                if self.d:
                    M = self.get_data()
                    ml = M & 0x0F
                    mh = M & 0xF0
                    al = self.A & 0x0F
                    ah = self.A & 0xF0
                    result = al + ml + self.c
                    if result > 0x09:
                        result += 0x06
                    result = result + ah + mh
                    if result > 0x99:
                        result += 0x60
                    self.v = ~((self.A ^ M) & 0x80) & ((self.A ^ result) & 0x80) != 0
                    self.c = 1 if result > 0xFF else 0
                    self.A = result
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    M = self.get_data()
                    result = self.A + M + self.c
                    # A and M have the same sign AND the result sign is different
                    self.v = ~((self.A ^ M) & 0x80) & ((self.A ^ result) & 0x80) != 0
                    self.c = 1 if result > 0xFF else 0
                    self.A = result
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.SBC:
                if self.d:
                    M = self.get_data()
                    ml = M & 0x0F
                    mh = M & 0xF0
                    al = self.A & 0x0F
                    ah = self.A & 0xF0
                    borrow = 1 - self.c

                    # Lower nibble
                    result_l = al - ml - borrow
                    if result_l < 0:
                        result_l = (result_l - 0x06) & 0x0F
                        borrow = 0x10
                    else:
                        borrow = 0

                    # Upper nibble
                    result_h = ah - mh - borrow
                    if result_h < 0:
                        result_h = (result_h - 0x60) & 0xF0
                        self.c = 0
                    else:
                        self.c = 1

                    result = (result_h | result_l) & 0xFF

                    self.v = ((self.A ^ M) & 0x80) & ((self.A ^ result) & 0x80) != 0

                    self.A = result
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
                else:
                    M = self.get_data()
                    result = self.A + ~(M) + self.c
                    # A and M have different sign AND the result sign is different
                    self.v = ((self.A ^ M) & 0x80) & ((self.A ^ result) & 0x80) != 0
                    self.c = 1 if result >= 0 else 0
                    self.A = result
                    self.z = self.calc_z(self.A)
                    self.n = self.calc_n(self.A)
            case i.BRK:
                # PC already incremented once, store "PC + 2"
                addr = uint16(self.PC + 1)
                self.stack_push(uint8(addr >> 8))
                self.stack_push(uint8(addr))
                self.stack_push(self.P | 0x18)
                # Jump to IRQ vector
                ll = self.read(0xFFFE)
                hh = self.read(0xFFFF)
                self.PC = toUint16(hh, ll)
            case i.RTI:
                self.P = self.stack_pop() & ~(0x18)
                ll = self.stack_pop()
                hh = self.stack_pop()
                self.PC = toUint16(hh, ll)
            case _:  # default
                raise NotImplementedError(
                    f"Instruction {self.instruction} not implemented"
                )

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

    def reset(self, ll=0xFFFC, hh=0xFFFD):
        # default reset vector at $FFFC, $FFFD
        ll_data = self.read(ll)
        hh_data = self.read(hh)
        self.PC = toUint16(hh_data, ll_data)

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

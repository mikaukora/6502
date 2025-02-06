# 6502 Emulator

A Python-based emulator designed to help learn and experiment with 6502 assembly and machine language. This project is a work in progress, with a focus on understanding the inner workings of the 6502 processor.

## Features

- Supports basic 6502 instructions and addressing modes.
- Implements a simple CPU, bus, and memory model.
- Can execute programs provided as raw binary files.
- Provides unit tests to verify instruction execution.

## Supported Instructions

The emulator currently supports the following 6502 instructions:

- **Transfer Instructions**
  - `LDA` – Load Accumulator
  - `LDX` – Load X Register
  - `LDY` – Load Y Register
  - `STA` – Store Accumulator
  - `STX` – Store X Register
  - `STY` – Store Y Register
  - `TAX` - Transfer accumulator to X
  - `TAY` - Transfer accumulator to Y
  - `TSX` - Transfer stack pointer to X
  - `TXA` - Transfer X to accumulator
  - `TXS` - Transfer X to stack pointer
  - `TYA` - Transfer Y accumulator
- **Decrements % Increments**
  - `DEC` - Decrement memory
  - `DEX` - Decrement X
  - `DEY` - Decrement Y
  - `INC` - Increment memory
  - `INX` - Increment X
  - `INY` - Increment Y
- **Flag Instructions**
  - `CLC` - Clear Carry
  - `CLD` - Clear Decimal (BCD arithmetics disabled)
  - `CLI` - Clear Interrupt Disable Bit
  - `CLV` - Clear Overflow Flag
  - `SEC` - Set Carry
  - `SED` - Set Decimal (BCD arithmetics disabled)
  - `SEI` - Set Interrupt Disable Bit
- **Other**
  - `NOP` - No Operation

Run ```./list_instructions.py``` for the full list.

## Supported Addressing Modes

- **Immediate** (`#$BB`)
- **Zero Page** (`$LL`)
- **Zero Page, X** (`$LL,X`)
- **Zero Page, Y** (`$LL,Y`)
- **Absolute** (`$LLHH`)
- **Absolute, X** (`$LLHH,X`)
- **Absolute, Y** (`$LLHH,Y`)
- **Implied**

## Running

### Compiling example programs

To compile the example programs into raw binary format, run:

```sh
pushd asm && make && popd
```

### Running the emulator with a binary file

You can run the emulator with a raw binary file by providing it as an argument:

```sh
python src/main.py asm/test.bin
```

This will output the status of the CPU after each instruction, such as:

```sh
Using file asm/test2.bin
Memory: ['a9', '01', 'aa', 'ca', 'ca']
 A: 0x00        : X: 0x00       Y: 0x00         S: 0x00
P: 0x00 Z: 0 N: 0 V: 0 B: 0 D: 0 I: 0 C: 0
PC: 0x0000
R 0x0000: a9
0xa9 LDA #
R 0x0001: 1
R 0x0002: aa
0xaa TAX impl
R 0x0003: ca
0xca DEX impl
R 0x0004: ca
0xca DEX impl
End of program
 A: 0x01        : X: 0xff       Y: 0x00         S: 0x00
P: 0x40 Z: 0 N: 1 V: 0 B: 0 D: 0 I: 0 C: 0
PC: 0x0005
```

## Running Tests

To run the unit tests, use:

```sh
uv run pytest
```

## References

[6502 instruction set](https://www.masswerk.at/6502/6502_instruction_set.html#STA)
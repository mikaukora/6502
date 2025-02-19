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
- **Stack Instructions**
  - `PHA` - Push Accumulator
  - `PLA` - Pull Accumulator
  - `PHP` - Push Status Register
  - `PLP` - Pull Status Register
- **Decrements & Increments**
  - `DEC` - Decrement memory
  - `DEX` - Decrement X
  - `DEY` - Decrement Y
  - `INC` - Increment memory
  - `INX` - Increment X
  - `INY` - Increment Y
- **Logical Operations**
  - `AND` - AND with Accumulator
  - `EOR` - XOR with Accumulator
  - `ORA` - OR with Accumulator
- **Shift & Rotate Instructions**
  - `ASL` - Arithmetic Shift Left
  - `LSR` - Logical Shift Right
  - `ROL` - Rotate Left
  - `ROR` - Rotate Right
- **Flag Instructions**
  - `CLC` - Clear Carry
  - `CLD` - Clear Decimal (BCD arithmetics disabled)
  - `CLI` - Clear Interrupt Disable Bit
  - `CLV` - Clear Overflow Flag
  - `SEC` - Set Carry
  - `SED` - Set Decimal (BCD arithmetics disabled)
  - `SEI` - Set Interrupt Disable Bit
- **Compare Instructions**
  - `CMP` - Compare accumulator and operand
  - `CPX` - Compare X and operand
  - `CPY` - Compare Y and operand
- **Conditional Branch Instructions**
  - `BEQ` - Branch on Equal (zero flag set)
  - `BNE` - Branch on Not Equal (zero flag clear)
  - `BMI` - Branch on Result Minus (negative flag set)
  - `BPL` - Branch on Result Plus (negative flag clear)
  - `BCC` - Branch on Carry Clear
  - `BCS` - Branch on Carry Set
- **Jumps & Subroutines**
  - `JMP` - Jump
  - `JSR` - Jump to Subroutine
  - `RTS` - Return from Subroutine
- **Other**
  - `BIT` - Bit Test (Memory & Accumulator)
  - `NOP` - No Operation

### List instructions

```./list_instructions.py``` shows up to date list of instructions.

For other options, see ```./list_instructions.py --help```

```sh
usage: list_instructions.py [-h] [-i INSTRUCTION] [-c CODE] [-m MODE]

List implemented 6502 instructions

options:
  -h, --help            show this help message and exit
  -i, --instruction INSTRUCTION
                        Search for a specific instruction (e.g. LDA)
  -c, --code CODE       Search for a specific op code (e.g. a5)
  -m, --mode MODE       Search for a specific addressing mode (e.g. abs)
```

## Supported Addressing Modes

- **Immediate** (`#$BB`)
- **Zero Page** (`$LL`)
- **Zero Page, X** (`$LL,X`)
- **Zero Page, Y** (`$LL,Y`)
- **Absolute** (`$LLHH`)
- **Absolute, X** (`$LLHH,X`)
- **Absolute, Y** (`$LLHH,Y`)
- **Implied**
- **X-indexed, indirect**
- **indirect, Y-indexed**

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

This will output the status of the CPU, memory reads/writes and instruction decoding, such as:

```sh
Using file asm/test2.bin
0000    a9 01 aa ca ca
A: 0x00 X: 0x00 Y: 0x00 S: 0x00
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
A: 0x01 X: 0xff Y: 0x00 S: 0x00
P: 0x80 Z: 0 N: 1 V: 0 B: 0 D: 0 I: 0 C: 0
PC: 0x0005
0000    a9 01 aa ca ca
```

## Running Tests

To run the unit tests, use:

```sh
uv run pytest
```

## References

[6502 instruction set](https://www.masswerk.at/6502/6502_instruction_set.html#STA)

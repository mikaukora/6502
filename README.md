# 6502 Emulator

A Python-based emulator for learning and experimenting with 6502 assembly and machine language. This project simulates a full 6502 CPU, providing tools for disassembly, execution, and debugging of raw binary programs.
It includes support for all standard 6502 instructions and addressing modes, a simple Apple I emulation with the Woz Monitor, and various utilities to inspect, modify, and execute machine code.


## Features

- Full 6502 CPU Emulation – Supports all standard 6502 instructions and addressing modes.
- Binary Execution – Run programs directly from raw binary files.
- Apple I Emulation – Includes a working Woz Monitor for interactive memory inspection and execution.
- Disassembler – Convert machine code into readable assembly with comments for better understanding.
- Instruction Listing Tool – Quickly look up implemented instructions and opcodes.

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
- **Arithmetic Operations**
  - `ADC` - Add with Carry
  - `SBC` - Subtract with Borrow
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
  - `BVC` - Branch on Overflow Clear
  - `BVS` - Branch on Overflow Set
- **Jumps & Subroutines**
  - `JMP` - Jump
  - `JSR` - Jump to Subroutine
  - `RTS` - Return from Subroutine
- **Interrupts**
  - `BRK` - Break / Software Interrupt
  - `RTI` - Return from Interrupt
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

### The Woz Monitor

To start 6502 emulation with the Woz Monitor, run:

```sh
./wozmon.py
```

The following prompt will be shown:

```sh
Starting the Woz Monitor
Press q to quit
\
```

To inspect memory, input the address (in capital letters):

```sh
EE

00EE: 00
```

Use dot to inpect a range:

```sh
24.2F

0024: 24 00 24 00
0028: 2F 00 03 00 00 00 00 00
```

It is also possible to change memory contents with ':'. The previous memory value is printed first:

```sh
30:EA

0030: 00
30

0030: EA
```

Run a program at given address with 'R':

```sh
0C00 R
```

### Disassembler

A simple disassembler is provided. It can be used to study opcodes and construct
commented Python code e.g. for unit tests.

```sh
./disasm.py --help
usage: disasm.py [-h] [--log LOG] infile

Disassembler for 6502

positional arguments:
  infile      Binary file to disassemble

options:
  -h, --help  show this help message and exit
  --log LOG   Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

Disassemble a file:

```sh
cat f.txt
0xCE, 0x0C, 0x00, 0xCE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0xEE, 0x0C, 0x00, 0x00

./disasm.py f.txt
0XCE, 0X0C,  0X00,  # DEC, ABS
0XCE, 0X0C,  0X00,  # DEC, ABS
0XEE, 0X0C,  0X00,  # INC, ABS
0XEE, 0X0C,  0X00,  # INC, ABS
0X00,               # BRK, IMPL
13 bytes
```

Disassemble from stdin:

```sh
echo "0xA0, 0x09, 0xB9, 0x00, 0x00, 0xC8, 0xB9, 0x00, 0x00, 0xCC, 0xDD" | ./disasm.py -
0XA0, 0X09,         # LDY, IMM
0XB9, 0X00,  0X00,  # LDA, ABS_Y
0XC8,               # INY, IMPL
0XB9, 0X00,  0X00,  # LDA, ABS_Y
0XCC,               # ???
0XDD,               # ???
11 bytes
```

### Compiling example programs

To compile the example programs into raw binary format, run:

```sh
pushd asm && make && popd
```

### Running the emulator with a binary file

You can run the emulator with a raw binary file by providing it as an argument:

```sh
./run_asm.py asm/test.bin
```

This will output the status of the CPU, memory reads/writes and instruction decoding, such as:

```sh
Using file asm/test2.bin
0000    a9 01 aa ca ca
A: 0x00 X: 0x00 Y: 0x00 S: 0xff
P: 0x00 Z: 0 N: 0 V: 0 D: 0 I: 0 C: 0
PC: 0x0000
R 0x0000: a9
R 0x0001: 1
R 0x0002: aa
R 0x0003: ca
R 0x0004: ca
End of program
A: 0x01 X: 0xff Y: 0x00 S: 0xff
P: 0x80 Z: 0 N: 1 V: 0 D: 0 I: 0 C: 0
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

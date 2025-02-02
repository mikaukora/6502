# 6502 Emulator

A Python-based emulator for the 8-bit MOS 6502 processor. This project is currently a work in progress.

## Features

- Supports basic 6502 instructions and addressing modes.
- Implements a simple CPU, bus, and memory model.
- Can execute multiple instructions sequentially.
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

## Supported Addressing Modes

- **Immediate** (`#value`)
- **Zero Page** (`$00 - $FF`)
- **Implied**

## Installation

At this stage, the emulator is under active development, and no standalone installation is provided. However, unit tests are available to verify functionality.

## Running Tests

To run the unit tests, use:

```sh
uv run pytest
```

## References

[6502 instruction set](https://www.masswerk.at/6502/6502_instruction_set.html#STA)
#!/usr/bin/env python

import sys
from src.model import CPU, Bus, Memory


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

#!/usr/bin/env python

from src.instructions import standard

for i, row in enumerate(standard):
    for j, instruction in enumerate(row):
        if instruction:
            print(f'{i:x}{j:x} {instruction[0].value} {instruction[1].value}')
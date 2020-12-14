#!/usr/bin/env python3

from collections import defaultdict
import re

def get_desc():
    return 14, 'Day 14: Docking Data'

def int_to_bits(mask, val):
    if isinstance(val, str):
        val = int(val)
    from grid import Grid
    val = bin(val)[2:]
    val = "0" * mask.width() + val
    val = val[-mask.width():]
    return Grid.from_row(val)

def bits_to_int(val):
    return int("".join([val[x] for x in val.x_range()]), 2)

def calc(log, values, mode):
    from grid import Grid
    memory = defaultdict(int)
    mask = Grid()
    floating_bits = []
    floating_max = 0
    for cur in values:
        if cur.startswith("mask = "):
            mask = Grid.from_row(cur[7:])
            floating_bits = [mask.width() - i for i in mask.x_range() if mask[i] == "X"]
            floating_max = 1 << len(floating_bits)
        else:
            m = re.search(r"mem\[(\d+)\] = (\d+)", cur)
            register, val = int(m.group(1)), int_to_bits(mask, m.group(2))
            if mode == 1:
                [val.set(mask[i], i) for i in mask.x_range() if mask[i] != "X"]
                memory[register] = bits_to_int(val)
            else:
                val = bits_to_int(val)
                register = int_to_bits(mask, register)
                [register.set(mask[i], i) for i in mask.x_range() if mask[i] in {"X", "1"}]
                [register.set("0", i) for i in mask.x_range() if mask[i] == "X"]
                register = bits_to_int(register)
                for bits in range(floating_max):
                    for bit in floating_bits:
                        register |= 1 << (bit - 1)
                        if bits & 1 == 0:
                            register ^= 1 << (bit - 1)
                        bits >>= 1
                    memory[register] = val

    return sum(memory.values())

def test(log):
    values = log.decode_values("""
        mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
        mem[8] = 11
        mem[7] = 101
        mem[8] = 0
    """)

    log.test(calc(log, values, 1), 165)

    values = log.decode_values("""
        mask = 000000000000000000000000000000X1001X
        mem[42] = 100
        mask = 00000000000000000000000000000000X0XX
        mem[26] = 1
    """)

    log.test(calc(log, values, 2), 208)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

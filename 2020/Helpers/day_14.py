#!/usr/bin/env python3

from collections import defaultdict
import re

def get_desc():
    return 14, 'Day 14: Docking Data'

def to_bits(mask, val):
    val = bin(val)[2:]
    val = "0" * len(mask) + val
    val = val[-len(mask):]
    return val

def calc(log, values, mode):
    memory = defaultdict(int)
    mask = ""
    for cur in values:
        if cur.startswith("mask = "):
            mask = cur[7:]
        else:
            m = re.search(r"mem\[(\d+)\] = (\d+)", cur)
            register, val = int(m.group(1)), int(m.group(2))
            val = to_bits(mask, val)
            if mode == 1:
                val = "".join([val[i] if mask[i] == "X" else mask[i] for i in range(len(mask))])
                memory[register] = int(val, 2)
            else:
                register = to_bits(mask, register)
                temp = []
                for i in range(len(mask)):
                    if mask[i] == "0":
                        temp.append(register[i])
                    elif mask[i] == "1":
                        temp.append("1")
                    else:
                        temp.append("X")

                max = 1 << len([x for x in temp if x == "X"])
                for bits in range(max):
                    copy = temp[:]
                    for i in range(len(copy)):
                        if copy[i] == "X":
                            copy[i] = str(bits & 1)
                            bits >>= 1
                    copy = int("".join(copy), 2)
                    memory[copy] = int(val, 2)

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

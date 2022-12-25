#!/usr/bin/env python3

from collections import defaultdict
import re

DAY_NUM = 14
DAY_DESC = 'Day 14: Docking Data'

def int_to_bits(mask, val):
    if isinstance(val, str):
        val = int(val)
    from grid import Grid
    val = bin(val)[2:]
    val = "0" * mask.width() + val
    val = val[-mask.width():]
    return Grid.from_text(val, axis=1)

def bits_to_int(val):
    return int("".join([val[x] for x in val.x_range()]), 2)

def calc(log, values, mode, save_state=False):
    from grid import Grid
    memory = defaultdict(int)
    mask = Grid()
    floating_bits = []
    floating_max = 0
    patterns = {}

    for cur in values:
        if save_state:
            log(cur)
        if cur.startswith("mask = "):
            mask = Grid.from_text(cur[7:], axis=1)
            floating_bits = tuple([1 << ((mask.width() - i) - 1) for i in mask.x_range() if mask[i] == "X"])
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
                combinations = patterns.get(floating_bits, None)
                if combinations is None:
                    combinations = []
                    for bits in range(floating_max):
                        temp = 0
                        for bit in floating_bits:
                            if bits & 1 == 0:
                                temp |= bit
                            bits >>= 1
                        combinations.append(temp)
                    patterns[floating_bits] = combinations
                for bits in combinations:
                    memory[register | bits] = val
            if save_state:
                log("memory_sum = " + str(sum(memory.values())))

    return sum(memory.values())

def other_save_state(describe, values):
    if describe:
        return "Save the state from part 2"
    else:
        from dummylog import DummyLog
        import os
        fn = os.path.join("Puzzles", "day_14_state.txt")
        log = DummyLog(fn)
        calc(log, values, 2, save_state=True)
        print("Done, created " + fn)

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

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: Opening the Turing Lock'

def calc(values, reg_a):
    offset = 0
    regs = {"a": reg_a, "b": 0}

    while True:
        if offset >= len(values):
            return regs["b"]

        ins = values[offset]
        if ins.startswith("hlf "):
            regs[ins[4:]] /= 2
            offset += 1
        elif ins.startswith("tpl "):
            regs[ins[4:]] *= 3
            offset += 1
        elif ins.startswith("inc "):
            regs[ins[4:]] += 1
            offset += 1
        elif ins.startswith("jmp "):
            offset += int(ins[4:])
        elif ins.startswith("jie "):
            if regs[ins[4:5]] % 2 == 0:
                offset += int(ins[6:])
            else:
                offset += 1
        elif ins.startswith("jio "):
            if regs[ins[4:5]] == 1:
                offset += int(ins[6:])
            else:
                offset += 1
        else:
            return regs["b"]

def test(log):
    values = [
        "inc b",
        "jio b, +2",
        "tpl b",
        "inc b",
    ]

    if calc(values, 0) == 2:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(values, 0),))
    log("Part 2: %d" % (calc(values, 1),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

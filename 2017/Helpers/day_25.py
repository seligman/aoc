#!/usr/bin/env python3

import re

DAY_NUM = 25
DAY_DESC = 'Day 25: The Halting Problem'


class Infinity:
    def __init__(self, default="."):
        self.default = default
        self.grid = [[default]]
        self.x = 0
        self.y = 0

    def get(self, x, y=0):
        x += self.x
        y += self.y
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            return self.default
        else:
            return self.grid[y][x]

    def set(self, value, x, y=0):
        x += self.x
        y += self.y

        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            while x < 0:
                for i in range(len(self.grid)):
                    self.grid[i] = [self.default] + self.grid[i]
                x += 1
                self.x += 1
            while y < 0:
                self.grid.insert(0, [self.default] * len(self.grid[0]))
                y += 1
                self.y += 1
            while x >= len(self.grid[0]):
                for i in range(len(self.grid)):
                    self.grid[i].append(self.default)
            while y >= len(self.grid):
                self.grid.append([self.default] * len(self.grid[0]))

        self.grid[y][x] = value

    def show(self, log):
        for row in self.get_rows():
            log(row)

    def get_rows(self):
        ret = []
        for row in self.grid:
            ret.append("".join(row))
        return ret


def calc(log, values):
    state = None
    diag = 0
    tape = Infinity(0)
    values.append("")

    for cur in values:
        m = re.search("Begin in state ([A-Z]+)", cur)
        if m:
            state = m.group(1)
        m = re.search("Perform a diagnostic checksum after ([0-9]+) steps", cur)
        if m:
            diag = int(m.group(1))


    ins = {}
    ins_temp = None
    ins_temp2 = None
    for i in range(len(values)):
        if len(values[i]) > 0:
            found = False
            if not found:
                m = re.search("Begin in state", values[i])
                if m:
                    found = True
            if not found:
                m = re.search("Perform a diagnostic", values[i])
                if m:
                    found = True
            if not found:
                m = re.search("In state ([A-Z]+)", values[i])
                if m:
                    found = True
                    ins_temp = [None, None]
                    ins[m.group(1)] = ins_temp
            if not found:
                m = re.search("If the current value is ([0-9]+)", values[i])
                if m:
                    found = True
                    ins_temp2 = [None, None, None]
                    ins_temp[int(m.group(1))] = ins_temp2
            if not found:
                m = re.search("Write the value ([0-9]+)", values[i])
                if m:
                    found = True
                    ins_temp2[0] = int(m.group(1))
            if not found:
                m = re.search("Move one slot to the (left|right)", values[i])
                if m:
                    found = True
                    ins_temp2[1] = -1 if m.group(1) == "left" else 1
            if not found:
                m = re.search("Continue with state ([A-Z]+)", values[i])
                if m:
                    found = True
                    ins_temp2[2] = m.group(1)
            if not found:
                raise Exception(values[i])

    pos = 0
    todo = 0
    while todo < diag:
        todo += 1
        temp = ins[state][tape.get(pos)]
        tape.set(temp[0], pos)
        pos += temp[1]
        state = temp[2]

    return sum(tape.grid[0])


def test(log):
    values = [
        "Begin in state A.",
        "Perform a diagnostic checksum after 6 steps.",
        "",
        "In state A:",
        "  If the current value is 0:",
        "    - Write the value 1.",
        "    - Move one slot to the right.",
        "    - Continue with state B.",
        "  If the current value is 1:",
        "    - Write the value 0.",
        "    - Move one slot to the left.",
        "    - Continue with state B.",
        "",
        "In state B:",
        "  If the current value is 0:",
        "    - Write the value 1.",
        "    - Move one slot to the left.",
        "    - Continue with state A.",
        "  If the current value is 1:",
        "    - Write the value 1.",
        "    - Move one slot to the right.",
        "    - Continue with state A.",
    ]

    if calc(log, values) == 3:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values))

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

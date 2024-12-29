#!/usr/bin/env python3

from collections import defaultdict, deque

DAY_NUM = 23
DAY_DESC = 'Day 23: Coprocessor Conflagration'

def deref(r, value):
    if len(value) == 1 and value >= 'a' and value <= 'z':
        return r[value]
    else:
        return int(value)

def calc(log, values, show_heat, mode, bail=None):
    values = [x.split(' ') for x in values]
    heat = [0] * len(values)
    ret = 0
    r = defaultdict(int)
    ip = 0

    if mode == 1:
        r["a"] = 1

    if show_heat:
        log("Initial registers:")
        log(", ".join("%s=%d" % (x, r[x]) for x in sorted(r)))

    while ip < len(values):
        if bail is not None and bail == ip:
            return r
        cur = values[ip]
        new_ip = ip + 1
        if not cur[0].startswith("#"):
            heat[ip] += 1
            if cur[0] == "set":
                r[cur[1]] = deref(r, cur[2])
            elif cur[0] == "sub":
                r[cur[1]] -= deref(r, cur[2])
            elif cur[0] == "mul":
                ret += 1
                r[cur[1]] *= deref(r, cur[2])
            elif cur[0] == "jnz":
                if deref(r, cur[1]) != 0:
                    new_ip = ip + deref(r, cur[2])
            else:
                raise Exception()
        ip = new_ip

    if show_heat:
        for i in range(len(values)):
            raw = " ".join(values[i])
            if values[i][0].startswith("#"):
                easy = "comment"
            elif values[i][0] == "set":
                easy = "%s = %s" % (values[i][1], values[i][2])
            elif values[i][0] == "sub":
                easy = "%s -= %s" % (values[i][1], values[i][2])
            elif values[i][0] == "mul":
                easy = "%s *= %s" % (values[i][1], values[i][2])
            elif values[i][0] == "jnz":
                easy = "if %s != 0 then skip(%s)" % (values[i][1], values[i][2])
            else:
                raise Exception()
            log("%3d: %5d: %-20s %s" % (i, heat[i], raw, easy))

        log("Final registers:")
        log(", ".join("%s=%d" % (x, r[x]) for x in sorted(r)))

    if mode == 0:
        return ret
    else:
        return r["h"]

def test(log):
    return True

def run(log, values):
    log("Part 1: %d" % (calc(log, values, False, 0),))
    r = calc(log, values, False, 1, 9)

    h = 0
    for x in range(r["b"],r["c"] + 1, 17):
        for i in range(2,x):
            if x % i == 0:
                h += 1
                break
    log("Part 2: %d" % (h,))

class DummyLog:
    def __init__(self):
        pass
    def __call__(self, value):
        self.show(value)
    def show(self, value):
        print(value)

def other_heat(describe, values):
    if describe:
        return "Show heat map of program"

    calc(DummyLog(), values, True, 0)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

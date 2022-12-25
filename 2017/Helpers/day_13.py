#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Packet Scanners'


def calc(log, values, bail):
    layers = {}
    for cur in values:
        cur = [int(x) for x in cur.split(": ")]
        layers[cur[0]] = [cur[1], 0, 1]

    if bail:
        offset = 0
        layers = [[x, layers[x][0]] for x in layers]
        layers.sort(key=lambda x:x[1])
        while True:
            bad = False
            for key, value in layers:
                cycle = (value - 2) * 2 + 2
                if ((key + offset) % cycle) == 0:
                    bad = True
                    offset += 1
                    break
            if not bad:
                return offset

    ret = 0
    for x in range(max(layers)+1):
        if x in layers:
            if layers[x][1] == 0:
                ret += x * layers[x][0]
                if bail:
                    return ret + 1

        for value in layers.values():
            if value[0] > 1:
                value[1] += value[2]
                if value[1] == value[0]:
                    value[2] = -1
                    value[1] = value[0] - 2
                elif value[1] == -1:
                    value[1] = 1
                    value[2] = 1

    return ret


def test(log):
    values = [
        "0: 3",
        "1: 2",
        "4: 4",
        "6: 4",
    ]

    if calc(log, values, False) == 24:
        if calc(log, values, True) == 10:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values, False))
    log(calc(log, values, True))

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

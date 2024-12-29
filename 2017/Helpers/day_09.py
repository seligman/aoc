#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Stream Processing'

def parse_garb(value, i, removed):
    escape = False
    while True:
        i[0] += 1
        if escape:
            escape = False
        else:
            if value[i[0]] == "!":
                escape = True
            elif value[i[0]] == ">":
                return
            else:
                removed[0] += 1

def parse(value, i, level, removed):
    ret = level
    while i[0] < len(value):
        i[0] += 1
        if value[i[0]] == "{":
            ret += parse(value, i, level + 1, removed)
        elif value[i[0]] == "<":
            parse_garb(value, i, removed)
        elif value[i[0]] == "}":
            return ret

def calc(log, values):
    removed = [0]
    ret = parse(values[0], [0], 1, removed)
    log("Part 2: " + str(removed[0]))
    return ret

def test(log):
    values = [
        "{{<!!>},{<!!>},{<!!>},{<!!>}}",
    ]

    if calc(log, values) == 9:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values),))

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

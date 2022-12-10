#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'Day 10: Knot Hash'


def calc(log, values, elements):
    values = [int(x) for x in values[0].split(",")]
    i = 0
    skip = 0
    elements = list(range(elements))

    for cur in values:
        for x in range(cur // 2):
            a, b = (i + x) % len(elements), (i + (cur-1) - x) % len(elements)
            elements[a], elements[b] = elements[b], elements[a]
        i = (i + skip + cur) % len(elements)
        skip += 1

    return elements[0] * elements[1]


def calc2(log, values):
    values = [ord(x) for x in list(values[0])] + [17, 31, 73, 47, 23]
    i = 0
    skip = 0
    elements = list(range(256))

    for _ in range(64):
        for cur in values:
            for x in range(cur // 2):
                a, b = (i + x) % len(elements), (i + (cur-1) - x) % len(elements)
                elements[a], elements[b] = elements[b], elements[a]
            i = (i + skip + cur) % len(elements)
            skip += 1

    ret = ""
    for i in range(0, 256, 16):
        temp = 0
        for j in range(16):
            temp ^= elements[i+j]
        ret += "%02x" % (temp,)

    return ret


def test(log):
    values = [
        "3,4,1,5",
    ]

    if calc(log, values, 5) == 12:
        if calc2(log, ["AoC 2017"]) == "33efeb34ea91902bb2f59c9920caa6cd":
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    log(calc(log, values, 256))
    log(calc2(log, values))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

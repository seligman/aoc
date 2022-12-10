#!/usr/bin/env python3

from collections import deque

DAY_NUM = 16
DAY_DESC = 'Day 16: Permutation Promenade'


def calc(log, values, dance):
    dance = list(dance)

    for cur in values[0].split(','):
        if cur[0] == "s":
            dance = deque(dance)
            dance.rotate(int(cur[1:]))
            dance = list(dance)
        elif cur[0] == "x":
            cur = [int(x) for x in cur[1:].split("/")]
            dance[cur[0]], dance[cur[1]] = dance[cur[1]], dance[cur[0]]
        elif cur[0] == "p":
            cur = [dance.index(x) for x in cur[1:].split("/")]
            dance[cur[0]], dance[cur[1]] = dance[cur[1]], dance[cur[0]]
        else:
            raise Exception()

    return "".join(dance)


def calc2(log, values, dance):
    seen = {}
    i = 0
    left = 1000000000
    while left > 0:
        seen[dance] = i
        dance = calc(log, values, dance)
        i += 1
        left -= 1
        if dance in seen:
            left -= (left // (i - seen[dance])) * (i - seen[dance])
            seen = {}
    return dance


def test(log):
    values = [
        "s1,x3/4,pe/b",
    ]

    if calc(log, values, "abcde") == "baedc":
        return True
    else:
        return False


def run(log, values):
    log(calc(log, values, 'abcdefghijklmnop'))
    log(calc2(log, values, 'abcdefghijklmnop'))

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

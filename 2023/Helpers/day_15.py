#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Lens Library'

from collections import defaultdict

def calc(log, values, mode):
    ret = 0

    boxes = defaultdict(dict)

    for cur in values[0].split(","):
        x = 0
        for dig in cur:
            if dig in "-=":
                target = x
            x += ord(dig)
            x *= 17
            x %= 256
        ret += x

        if cur.endswith("-"):
            label = cur[:-1]
            if label in boxes[target]:
                del boxes[target][label]
        else:
            label, focus = cur.split("=")
            boxes[target][label] = int(focus)

    if mode == 2:
        ret = 0
        for box_num, box in boxes.items():
            for lens_num, (label, focus) in enumerate(box.items()):
                ret += (box_num + 1) * (lens_num + 1) * focus

    return ret

def test(log):
    values = log.decode_values("""
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    """)

    log.test(calc(log, values, 1), '1320')
    log.test(calc(log, values, 2), '145')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

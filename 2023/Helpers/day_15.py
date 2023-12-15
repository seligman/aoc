#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Lens Library'

def calc(log, values, mode):
    # TODO: Delete or use these
    # from parsers import get_ints, get_floats
    # from grid import Grid, Point
    # grid = Grid.from_text(values)
    # from program import Program
    # program = Program(values)

    ret = 0

    boxes = {}

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
            boxes[target] = [x for x in boxes.get(target, []) if x.split("=")[0] != cur[:-1]]
        else:
            temp = boxes.get(target, [])
            if cur.split("=")[0] in [x.split("=")[0] for x in temp]:
                boxes[target] = [cur if x.split("=")[0] == cur.split("=")[0] else x for x in temp]
            else:
                boxes[target] = temp + [cur]

    if mode == 2:
        ret = 0
        for i, box in boxes.items():
            for j, cur in enumerate(box):
                ret += (i + 1) * (j + 1) * int(cur.split("=")[1])

    return ret

def test(log):
    values = log.decode_values("""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    """)

    log.test(calc(log, values, 1), '1320')
    log.test(calc(log, values, 2), '145')

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

#!/usr/bin/env python3

DAY_NUM = 5
DAY_DESC = 'Day 5: Supply Stacks'

def calc(log, values, mode, draw=False, max_height=0, get_max_height=False):
    if draw:
        from grid import Grid
        animated = Grid()

    stacks = []
    values = [x.lstrip(".") for x in values]
    while True:
        row = values.pop(0)
        if row.strip().startswith("1"):
            break
        for i, val in enumerate(row):
            if 'A' <= val <= 'Z':
                i = int((i - 1) / 4)
                while len(stacks) <= i:
                    stacks.append([])
                stacks[i].append(val)

    for i in range(len(stacks)):
        stacks[i] = stacks[i][::-1]

    if draw:
        for x in range(len(stacks)):
            for y in range(max_height):
                animated[(x, max_height-y)] = " " if y >= len(stacks[x]) else stacks[x][y]
        animated.save_frame()

    import re
    for row in values:
        m = re.search("move ([0-9]+) from ([0-9]+) to ([0-9]+)", row)
        if m is not None:
            steps = list(map(int, m.groups()))
            if mode == 1:
                for _ in range(steps[0]):
                    stacks[steps[2]-1].append(stacks[steps[1]-1].pop())
                    if get_max_height:
                        max_height = max(max_height, max(len(x) for x in stacks))
                    if draw:
                        for x in range(len(stacks)):
                            for y in range(max_height):
                                animated[(x, max_height-y)] = " " if y >= len(stacks[x]) else stacks[x][y]
                        animated.save_frame()
            else:
                temp = []
                for _ in range(steps[0]):
                    temp.append(stacks[steps[1]-1].pop())
                stacks[steps[2]-1] += temp[::-1]

    ret = ""
    for cur in stacks:
        ret += cur[-1]

    if draw:
        animated.draw_frames(cell_size=(15, 15))

    if get_max_height:
        return max_height

    return ret

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    max_height = calc(DummyLog(), values, 1, dget_max_height=True)
    calc(DummyLog(), values, 1, draw=True, max_height=max_height)
    animate.create_mp4(DAY_NUM, rate=10, final_secs=5)

def test(log):
    values = log.decode_values("""
        .    [D]    
        .[N] [C]    
        .[Z] [M] [P]
        . 1   2   3 
        .
        .move 1 from 2 to 1
        .move 3 from 1 to 3
        .move 2 from 2 to 1
        .move 1 from 1 to 2
    """)

    log.test(calc(log, values, 1), 'CMZ')
    log.test(calc(log, values, 2), 'MCD')

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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip() for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Rope Bridge'

def calc(log, values, mode):
    rope = []
    for _ in range(2 if mode == 1 else 10):
        rope.append([0, 0])

    def move(head, dir):
        if dir == "U":
            head[1] -= 1
        if dir == "D":
            head[1] += 1
        if dir == "R":
            head[0] += 1
        if dir == "L":
            head[0] -= 1
    def fix(head, tail):
        if tail[1] > head[1] + 1:
            tail[1] -= 1
            if tail[0] > head[0]:
                tail[0] -= 1
            elif tail[0] < head[0]:
                tail[0] += 1
        elif tail[1] < head[1] - 1:
            tail[1] += 1
            if tail[0] > head[0]:
                tail[0] -= 1
            elif tail[0] < head[0]:
                tail[0] += 1
        elif tail[0] > head[0] + 1:
            tail[0] -= 1
            if tail[1] > head[1]:
                tail[1] -= 1
            elif tail[1] < head[1]:
                tail[1] += 1
        elif tail[0] < head[0] - 1:
            tail[0] += 1
            if tail[1] > head[1]:
                tail[1] -= 1
            elif tail[1] < head[1]:
                tail[1] += 1
            
    seen = set()
    seen.add((rope[-1][0], rope[-1][1]))
    for row in values:
        dir, val = row.split(" ")
        for _ in range(int(val)):
            move(rope[0], dir)
            for i in range(len(rope)-1):
                fix(rope[i], rope[i+1])
            seen.add((rope[-1][0], rope[-1][1]))

    # from grid import Grid
    # grid = Grid()
    # for x, y in seen:
    #     grid[(x, y)] = "#"
    # grid.show_grid(log)

    return len(seen)

def test(log):
    values = log.decode_values("""
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
    """)

    log.test(calc(log, values, 1), 13)

    values = log.decode_values("""
        R 5
        U 8
        L 8
        D 3
        R 17
        D 10
        L 25
        U 20
    """)
    log.test(calc(log, values, 2), 36)

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

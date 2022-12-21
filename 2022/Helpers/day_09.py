#!/usr/bin/env python3

# Animation: https://youtu.be/zTpJBzVDktk

DAY_NUM = 9
DAY_DESC = 'Day 9: Rope Bridge'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    rope = []
    for _ in range(2 if mode == 1 else 10):
        rope.append(Point())

    def move(head, dir):
        if dir == "U": return head + (0, -1)
        if dir == "D": return head + (0, 1)
        if dir == "L": return head + (-1, 0)
        if dir == "R": return head + (1, 0)

    def sign(val):
        if val < 0: return -1
        elif val > 0: return 1
        else: return 0

    def fix(head, tail):
        diff = tail - head
        if abs(diff.y) > 1 or abs(diff.x) > 1:
            return tail + (-sign(diff.x), -sign(diff.y))
        else:
            return tail

    if draw:            
        grid = Grid()

    seen = set()
    frame_no = 0
    seen.add(rope[-1].copy())
    last_rope = []

    for row in values:
        dir, val = row.split(" ")
        for _ in range(int(val)):
            rope[0] = move(rope[0], dir)
            for i in range(len(rope)-1):
                rope[i+1] = fix(rope[i], rope[i+1])
            seen.add(rope[-1].copy())
            if draw:
                frame_no += 1
                if (frame_no % 5) == 1:
                    for pt in last_rope: grid[pt] = "."
                    last_rope = [x.copy() for x in rope]
                    for pt in seen: grid[pt] = "star"
                    for pt in rope: grid[pt] = "#"
                    grid.save_frame()
    if draw:
        for pt in last_rope: grid[pt] = "."
        for pt in seen: grid[pt] = "star"
        for pt in rope: grid[pt] = "#"
        grid.save_frame()
        grid.draw_frames()

    return len(seen)

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

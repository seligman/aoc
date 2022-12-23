#!/usr/bin/env python3

# Animation: https://youtu.be/s3xn8bOo6pA

DAY_NUM = 23
DAY_DESC = 'Day 23: Unstable Diffusion'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    checks = [
        [( 0,-1), [( 0, -1), ( 1, -1), (-1, -1)]],
        [( 0, 1), [( 0,  1), ( 1,  1), (-1,  1)]],
        [(-1, 0), [(-1,  0), (-1,  1), (-1, -1)]],
        [( 1, 0), [( 1,  0), ( 1,  1), ( 1, -1)]],
    ]

    round = 1
    while True:
        elves = []
        any_moved = 0
        for x, y in grid.grid.keys():
            if grid[(x, y)] == "#":
                elves.append({
                    "pt": Point(x,y),
                    "move": None,
                })
        for elf in elves:
            others = 0
            for pt in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                if grid[elf["pt"] + pt] == "#":
                    others += 1
            elf["can_move"] = others > 0

        from collections import defaultdict
        counts = defaultdict(int)
        if draw:
            moved = set()

        for elf in elves:
            for target, check in checks:
                if elf["can_move"]:
                    any_elves = False
                    for test in check:
                        if grid[elf["pt"] + test] == "#":
                            any_elves = True
                            break
                    if not any_elves:
                        elf["move"] = elf["pt"] + target
                        counts[elf["move"].tuple] += 1
                        break
        for elf in elves:
            if elf["move"] is not None:
                if counts[elf["move"].tuple] == 1:
                    grid[elf["pt"]] = 0
                    grid[elf["move"]] = "#"
                    if draw:
                        moved.add(elf["move"].tuple)
                    any_moved += 1
        
        checks.append(checks.pop(0))
        if mode == 1:
            if round == 10:
                break
        else:
            if draw:
                for pt in grid.grid.keys():
                    if grid[pt] == "#":
                        if pt not in moved:
                            grid[pt] = "star"
                grid.save_frame()
                for pt in grid.grid.keys():
                    if grid[pt] == "star":
                        grid[pt] = "#"
            if any_moved == 0:
                if draw:
                    grid.draw_frames()
                return round 
        round += 1


    clean = Grid()
    for x, y in grid.grid.keys():
        if grid[(x, y)] == "#":
            clean[(x, y)] = "#"

    count = 0
    for x in clean.x_range():
        for y in clean.y_range():
            if clean[(x, y)] != "#":
                count += 1

    return count

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def test(log):
    values = log.decode_values("""
        ....#..
        ..###.#
        #...#.#
        .#...##
        #.###..
        ##.#.##
        .#..#..
    """)

    log.test(calc(log, values, 1), '110')
    log.test(calc(log, values, 2), '20')

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

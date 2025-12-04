#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 4
DAY_DESC = 'Day 4: Printing Department'

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    counts = {}
    to_decrease = defaultdict(list)

    # Note the location of all paper rolls, and
    # also track the items near it that will
    # have one less item if they're removed
    for xy in grid.xy_range(as_point=True):
        if grid[xy] == "@":
            counts[xy] = 0
            for oxy in Grid.get_dirs(2, as_point=True):
                if grid[xy + oxy] == "@":
                    counts[xy] += 1
                    to_decrease[xy].append(xy + oxy)

    ret = 0
    while True:
        to_remove = []
        if draw:
            grid.save_frame()

        # Find how many we could remove
        for xy, count in counts.items():
            if count < 4:
                ret += 1
                to_remove.append(xy)

        if mode == 1 or len(to_remove) == 0:
            break

        if draw:
            for xy in to_remove:
                grid[xy] = "*"
            grid.save_frame()

        for xy in to_remove:
            if draw:
                grid[xy] = "."
            # For each item we removed, decrease the count
            # from all of its neighbors, and remove it
            for oxy in to_decrease[xy]:
                if oxy in counts:
                    counts[oxy] -= 1
            del counts[xy]

    if draw:
        grid.draw_frames(repeat_final=30)

    return ret

def test(log):
    values = log.decode_values("""
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
    """)

    log.test(calc(log, values, 1), '13')
    log.test(calc(log, values, 2), '43')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))
    log("Part 2")
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Transparent Origami'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid()
    for cur in values:
        if "," in cur:
            cur = tuple(int(x) for x in cur.split(","))
            grid[cur] = "#"
        elif cur.startswith("fold along"):
            axis = {"x": 0, "y": 1}[cur[11]]
            cur = int(cur[13:])
            for xy in list(grid.grid):
                if xy[axis] >= cur:
                    if axis == 0:
                        dest = (cur - (xy[0] - cur), xy[1])
                    else:
                        dest = (xy[0], cur - (xy[1] - cur))
                    grid[dest] = "#"
                    del grid.grid[xy]
            if mode == 1:
                break

    if mode == 2:
        grid.show_grid(log)
        return grid.decode_grid(log)

    return len(grid.grid)

def test(log):
    values = log.decode_values("""
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0

        fold along y=7
        fold along x=5
    """)

    log.test(calc(log, values, 1), 17)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)

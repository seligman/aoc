#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Resonant Collinearity'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values, default="-")

    nodes = {}
    for xy in grid.xy_range():
        if grid[xy] != ".":
            if grid[xy] not in nodes:
                nodes[grid[xy]] = []
            nodes[grid[xy]].append(xy)
    
    anti = set()
    if mode == 2:
        anti = set(xy for xy in grid.xy_range() if grid[xy] != ".")
    for val, items in nodes.items():
        for a in items:
            for b in items:
                if a != b:
                    xy = b[0] + b[0] - a[0], b[1] + b[1] - a[1]
                    while True:
                        if grid[xy] != "-":
                            anti.add(xy)
                            if mode == 1:
                                break
                            xy = xy[0] + b[0] - a[0], xy[1] + b[1] - a[1]
                        else:
                            break
                    xy = a[0] + a[0] - b[0], a[1] + a[1] - b[1]
                    while True:
                        if grid[xy] != "-":
                            anti.add(xy)
                            if mode == 1:
                                break
                            xy = xy[0] + a[0] - b[0], xy[1] + a[1] - b[1]
                        else:
                            break
    
    return len(anti)

def test(log):
    values = log.decode_values("""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
    """)

    log.test(calc(log, values, 1), '14')
    log.test(calc(log, values, 2), '34')

def run(log, values):
    log(calc(log, values, 1))
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

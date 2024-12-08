#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Resonant Collinearity'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values, default="-")

    if draw:
        shadow = grid.copy()
        shadow.default = None
        for xy in grid.xy_range():
            if grid[xy] != ".":
                shadow[xy] = "#"

    nodes = {}
    anti = set()

    for xy in grid.xy_range():
        if grid[xy] != ".":
            if grid[xy] not in nodes:
                nodes[grid[xy]] = []
            temp = Point(xy)
            nodes[grid[xy]].append(temp)
            if mode == 2:
                anti.add(temp)
    
    for val, items in nodes.items():
        for a in items:
            for b in items:
                if a != b:
                    if draw:
                        shadow[a] = "Star"
                        shadow[b] = "Star"
                        before = len(anti)
                        shadow.save_frame()
                    for xy, to_add in (b, (b - a)), (a, (a - b)):
                        xy += to_add
                        while grid[xy] != "-":
                            if grid[xy] != val:
                                anti.add(xy)
                                if draw:
                                    shadow[xy] = "target"
                            if mode == 1:
                                break
                            xy += to_add
                    if draw:
                        shadow[a] = "#"
                        shadow[b] = "#"
                        if len(anti) > before:
                            shadow.save_frame()
                        else:
                            shadow.remove_last_frame()
    
    if draw:
        shadow.save_frame()
        shadow.draw_frames(show_lines=False)
    return len(anti)

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

#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: The Floor Will Be Lava'

def calc(log, values, mode):
    from grid import Grid, Point
    from collections import deque
    grid = Grid.from_text(values)

    def get_starts():
        for y in grid.y_range():
            yield deque([(0, y, 1, 0)])
            if mode == 1: return
            yield deque([(grid.axis_max(0), y, -1, 0)])
        for x in grid.x_range():
            yield deque([(x, 0, 0, 1)])
            yield deque([(x, grid.axis_max(1), 0, -1)])

    best = 0

    for todo in get_starts():
        energy = set()
        seen = set()

        def add_if_new(*key):
            if key not in seen:
                seen.add(key)
                todo.append(key)

        max_x = grid.axis_max(0)
        max_y = grid.axis_max(1)
        mirrors = {}
        for pt, val in grid.grid.items():
            if val in "-|\\/":
                mirrors[pt] = val

        while len(todo) > 0:
            x, y, ox, oy = todo.pop()
            energy.add((x, y))
            while True:
                x, y = x + ox, y + oy
                if 0 <= x <= max_x and 0 <= y <= max_y:
                    val = mirrors.get((x, y), "")
                    if (val == "|" and oy == 0) or (val == "-" and ox == 0):
                        add_if_new(x, y, abs(oy), abs(ox))
                        add_if_new(x, y, -abs(oy), -abs(ox))
                        break
                    else:
                        if val == "/":
                            add_if_new(x, y, -oy, -ox)
                            break
                        elif val == "\\":
                            add_if_new(x, y, oy, ox)
                            break
                        else:
                            energy.add((x, y))
                else:
                    break 
        best = max(best, len(energy))

    return best

def test(log):
    values = log.decode_values(r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
    """)

    log.test(calc(log, values, 1), '46')
    log.test(calc(log, values, 2), '51')

    values = log.decode_values(r"""
.....
./-\.
.|.|.
.\-/.
.....
    """)
    log.test(calc(log, values, 2), '9')

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

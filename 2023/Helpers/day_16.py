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
            if mode == 1:
                break
            yield deque([(grid.axis_max(0), y, -1, 0)])
        if mode == 2:
            for x in grid.x_range():
                yield deque([(x, 0, 0, 1)])
                yield deque([(x, grid.axis_max(1), 0, -1)])

    best = 0
    for todo in get_starts():
        seen = set()
        energy = set()
        energy.add((todo[0][0], todo[0][1]))
        while len(todo) > 0:
            x, y, ox, oy = todo.pop()
            if (x, y, ox, oy) not in seen:
                seen.add((x, y, ox, oy))
                x += ox
                y += oy
                if 0 <= x <= grid.axis_max(0) and 0 <= y <= grid.axis_max(1):
                    energy.add((x, y))
                    if grid[x, y] == "|" and oy == 0:
                        todo.append((x, y, 0, 1))
                        todo.append((x, y, 0, -1))
                    elif grid[x, y] == "-" and ox == 0:
                        todo.append((x, y, 1, 0))
                        todo.append((x, y, -1, 0))
                    else:
                        if grid[x, y] == "/":
                            if (ox, oy) == (1, 0): ox, oy = 0, -1
                            elif (ox, oy) == (-1, 0): ox, oy = 0, 1
                            elif (ox, oy) == (0, -1): ox, oy = 1, 0
                            elif (ox, oy) == (0, 1): ox, oy = -1, 0
                        elif grid[x, y] == "\\":
                            if (ox, oy) == (1, 0): ox, oy = 0, 1
                            elif (ox, oy) == (-1, 0): ox, oy = 0, -1
                            elif (ox, oy) == (0, -1): ox, oy = -1, 0
                            elif (ox, oy) == (0, 1): ox, oy = 1, 0
                        todo.append((x, y, ox, oy))
    
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

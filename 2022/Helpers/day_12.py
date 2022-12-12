#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Hill Climbing Algorithm'

from collections import deque

def enum_start(values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    for x in grid.x_range():
        for y in grid.y_range():
            if grid[(x, y)] == "S":
                start = Point(x, y)
                grid[start] = 'a'

    yield start, grid

    if mode == 2:
        grid = Grid.from_text(values)
        grid[start] = 'a'
        for x in grid.x_range():
            for y in grid.y_range():
                pt = Point(x, y)
                if pt != start and grid[pt] == 'a':
                    yield Point(x, y), grid.copy()

def calc(log, values, mode):
    best = None

    will_use = set()
    for start, grid in enum_start(values, mode):
        will_use.add(start)

    for start, grid in enum_start(values, mode):
        visited = set()
        todo = deque([(start, 0)])
        while len(todo) > 0:
            last_step, steps = todo.popleft()
            for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_step = last_step + d
                if next_step not in visited:
                    if next_step in grid:
                        if grid[next_step] == "E" and grid[last_step] == "z":
                            if best is None or steps < best:
                                best = steps
                                todo = []
                        else:
                            change = ord(grid[next_step]) - ord(grid[last_step])
                            if change <= 1 and grid[next_step] != "E" and next_step not in will_use:
                                use = True
                                visited.add(next_step)
                                if best is not None:
                                    if steps >= best:
                                        use = False
                                if use:
                                    todo.append((next_step, steps + 1))

    return best + 1

def test(log):
    values = log.decode_values("""
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
    """)

    log.test(calc(log, values, 1), 31)
    log.test(calc(log, values, 2), 29)

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
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

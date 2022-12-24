#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Blizzard Basin'

from collections import deque

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    from_x = grid.axis_min(0) + 1
    to_x = grid.axis_max(0) - 1
    from_y = grid.axis_min(1) + 1
    to_y = grid.axis_max(1) - 1

    blizzards = {}
    for x in range(from_x, to_x + 1):
        for y in range(from_y, to_y + 1):
            if grid[(x, y)] in "<>^v":
                blizzards[(x, y)] = [grid[(x, y)]]

    dirs = {
        "<": (-1, 0),
        ">": (1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }

    seen = {}
    used = set()

    best = 1

    todo = deque([((1, 0), blizzards, [], [])])
    while len(todo) > 0:
        pt, blizzards, steps, hits = todo.popleft()

        if pt == (from_x, from_y - 1):
            if len(hits) == 0 or hits[-1] != "S":
                hits = hits + ["S"]
        elif pt == (to_x, to_y + 1):
            if len(hits) == 0 or hits[-1] != "E":
                hits = hits + ["E"]
        
        if len(hits) >= best:
            best = len(hits)
        else:
            continue

        if mode == 1:
            if tuple(hits) == ("S", "E"):
                return len(steps)
        else:
            if tuple(hits) == ("S", "E", "S", "E"):
                return len(steps)

        if len(steps) not in seen:
            next_grid = {}
            for (x, y), vals in blizzards.items():
                for val in vals:
                    dir = dirs[val]
                    new_x = ((x + dir[0] - from_x) % (to_x - from_x + 1)) + from_x
                    new_y = ((y + dir[1] - from_y) % (to_y - from_y + 1)) + from_y
                    if (new_x, new_y) not in next_grid:
                        next_grid[(new_x, new_y)] = []
                    next_grid[(new_x, new_y)].append(val)
            seen[len(steps)] = next_grid
        else:
            next_grid = seen[len(steps)]

        def is_valid_pos(x, y):
            if (len(steps), x, y) in used:
                return False
            if x == from_x and y == from_y - 1:
                return True
            elif x == to_x and y == to_y + 1:
                return True
            if from_x <= x <= to_x and from_y <= y <= to_y:
                if (x, y) not in next_grid:
                    return True
            return False

        if is_valid_pos(pt[0], pt[1]):
            todo.append((pt, next_grid, steps + [pt], hits))
            used.add((len(steps), pt[0], pt[1]))
        
        for dir in dirs.values():
            x, y = pt[0] + dir[0], pt[1] + dir[1]
            if is_valid_pos(x, y):
                todo.append(((x, y), next_grid, steps + [pt], hits))
                used.add((len(steps), x, y))

    return 0

def test(log):
    values = log.decode_values("""
        #.######
        #>>.<^<#
        #.<..<<#
        #>v.><>#
        #<^v^^>#
        ######.#
    """)

    log.test(calc(log, values, 1), '18')
    log.test(calc(log, values, 2), '54')

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

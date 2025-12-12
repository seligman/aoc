#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Christmas Tree Farm'

def calc(log, values, mode):
    from grid import Grid, Point
    import re

    shapes = {}
    cur = None
    temp = []
    sizes = []

    for row in values:
        if len(row) == 0:
            shapes[cur] = Grid.from_text(temp)
            temp = []
            cur = None
        elif re.search("^[.#]+$", row):
            temp.append(row)
        else:
            m = re.search("^(?P<i>[0-9]+):", row)
            if m != None:
                cur = int(m['i'])
            else:
                size, vals = row.split(": ")
                width, height = [int(x) for x in size.split("x")]
                vals = [int(x) for x in vals.split(' ')]
                sizes.append((width, height, vals))

    steps = []
    for flip_x in [False, True]:
        for flip_y in [False, True]:
            for rotate in [0, 1, 2, 3]:
                steps.append((flip_x, flip_y, rotate))

    def get_matches(width, height, vals, target):
        for i in range(len(vals)):
            if vals[i] > 0:
                shape = shapes[i]
                for x in range(width):
                    for y in range(height):
                        for shape_temp in shape.enum_rotates():
                            if shape_temp.axis_min(0) >= 0 and shape_temp.axis_min(1) >= 0:
                                if shape_temp.axis_max(0) + x < width and shape_temp.axis_max(1) + y < height:
                                    good = True
                                    for ox, oy in shape_temp.xy_range():
                                        if shape_temp[ox, oy] == "#":
                                            if target[ox + x, oy + y] == "#":
                                                good = False
                                                break
                                    if good:
                                        target_temp = target.copy()
                                        for ox, oy in shape_temp.xy_range():
                                            if shape_temp[ox, oy] == "#":
                                                target_temp[ox + x, oy + y] = "#"
                                        vals_temp = vals[:]
                                        vals_temp[i] -= 1
                                        yield vals_temp, target_temp

    ret = 0
    maybe = 0
    for width, height, vals in sizes:
        if sum(vals) <= (width//3) * (height//3):
            ret += 1
        else:
            total_grid = 0
            for i in range(len(vals)):
                count = sum(1 if x == '#' else 0 for x in shapes[i].dump_grid())
                total_grid += count * vals[i]
            if total_grid <= width * height:
                maybe += 1

    if maybe == 0:
        return ret

    ret = 0
    for width, height, vals in sizes:
        target = Grid()
        todo = [(vals, target)]
        seen = set()
        while len(todo) > 0:
            vals, target = todo.pop(0)
            check = target.dump_grid()
            if check not in seen:
                seen.add(check)
                if sum(vals) == 0:
                    ret += 1
                    break

                for next_val, next_target in get_matches(width, height, vals, target):
                    todo.append((next_val, next_target))

    return ret
    
def test(log):
    values = log.decode_values("""
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
    """)

    log.test(calc(log, values, 1), '2')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1))

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

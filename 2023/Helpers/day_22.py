#!/usr/bin/env python3

DAY_NUM = 22
DAY_DESC = 'Day 22: Sand Slabs'

def brick_range(a, b):
    if b > a:
        return range(a, b+1)
    else:
        return range(a, b-1, -1)

def drop_bricks(grid, bricks):
    dropped = set()
    while True:
        found = False
        for i, val in list(bricks.items()):
            can_drop = 1
            while True:
                below = set(grid[x, y, z-can_drop] for x, y, z in val)
                if len(below - {0, i}) == 0:
                    can_drop += 1
                else:
                    can_drop -= 1
                    break
            if can_drop > 0:
                dropped.add(i)
                found = True
                for x, y, z in val:
                    grid[x, y, z] = 0
                for x, y, z in val:
                    grid[x, y, z - can_drop] = i
                bricks[i] = [(x, y, z-can_drop) for x, y, z in val]
        if not found:
            break
    return dropped

def show_side(log, grid):
    for z in reversed(grid.axis_range(2)):
        l = ""
        for x in grid.axis_range(0):
            cell = set()
            for y in grid.axis_range(1):
                if grid[x, y, z] != 0:
                    cell.add(grid[x, y, z])
            if len(cell) == 0:
                l += "."
            elif len(cell) > 1:
                l += "?"
            else:
                l += str(list(cell)[0])
        log(l)

cache = {}
def calc(log, values, mode):
    from grid import Grid, Point

    grid = Grid()
    bricks = {}

    for i, row in enumerate(values):
        a, b = row.split("~")
        x1, y1, z1 = list(map(int, a.split(",")))
        x2, y2, z2 = list(map(int, b.split(",")))

        bricks[i+1] = []

        for x in brick_range(x1, x2):
            for y in brick_range(y1, y2):
                for z in brick_range(z1, z2):
                    bricks[i+1].append((x, y, z))
                    grid[x, y, z] = i + 1
        
        # Add a floor
        for x in grid.axis_range(0):
            for y in grid.axis_range(1):
                grid[x, y, -1] = -1

    drop_bricks(grid, bricks)

    ret = 0
    for i in list(bricks):
        if i not in cache:
            bricks_c, grid_c = bricks.copy(), grid.copy()
            for x, y, z in bricks[i]:
                grid_c[x, y, z] = 0
            del bricks_c[i]
            cache[i] = drop_bricks(grid_c, bricks_c)

        dropped = cache[i]

        if mode == 1:
            if len(dropped) == 0:
                ret += 1
        else:
            ret += len(dropped)

    return ret

def test(log):
    values = log.decode_values("""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
    """)

    log.test(calc(log, values, 1), '5')
    log.test(calc(log, values, 2), '7')

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

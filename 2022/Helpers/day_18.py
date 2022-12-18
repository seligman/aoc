#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Boiling Boulders'

def calc(log, values, mode):
    from parsers import get_ints
    from grid import Grid

    seen = []
    grid = Grid()

    for cur in values:
        x, y, z = get_ints(cur)
        sides = 6

        for i in range(len(seen)):
            ox, oy, oz, osides = seen[i]
            touch = False
            if abs(ox - x) == 1 and oy == y and oz == z:
                touch = True
            if abs(oy - y) == 1 and ox == x and oz == z:
                touch = True
            if abs(oz - z) == 1 and oy == y and ox == x:
                touch = True
            if touch:
                sides -= 1
                osides -= 1
            seen[i] = (ox, oy, oz, osides)

        seen.append((x, y, z, sides))
        grid[(x, y, z)] = "#"

    if mode == 2:
        ret = 0
        for ax, ay, az, q in seen:
            for ox, oy, oz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                todo = [(ax+ox, ay+oy, az+oz)]
                if grid[todo[-1]] == 0:
                    hit_end = False
                    used = set()
                    while len(todo) > 0:
                        x, y, z = todo.pop(0)
                        for ox, oy, oz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                                tx = ox + x
                                ty = oy + y
                                tz = oz + z
                                use = False
                                if tx >= 0 and ty >= 0 and tz >= 0:
                                    if tx <= grid.axis_max(0) and ty <= grid.axis_max(1) and tz <= grid.axis_max(2):
                                        use = True
                                
                                if use:
                                    if (tx, ty, tz) not in used:
                                        used.add((tx, ty, tz))
                                        if grid[(tx, ty, tz)] == 0:
                                            todo.append((tx, ty, tz))
                                else:
                                    hit_end = True
                                    todo = []
                                    break
                    if hit_end:
                        ret += 1

        return ret

    return sum(x[3] for x in seen)

def test(log):
    values = log.decode_values("""
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
    """)

    log.test(calc(log, values, 1), 64)
    log.test(calc(log, values, 2), 58)

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

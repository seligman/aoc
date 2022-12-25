#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Crossed Wires'


def calc(log, values, steps):
    grids = [{}, {}]
    dirs = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    for i in range(2):
        row = values[i]
        x, y = 0, 0
        count = 0
        for cur in row.split(','):
            for _ in range(int(cur[1:])):
                x += dirs[cur[0]][0]
                y += dirs[cur[0]][1]

                count += 1
                if (x, y) not in grids[i]:
                    grids[i][(x, y)] = count

    points = set(grids[0]) & set(grids[1])
    if steps:
        best = min([grids[0][x] + grids[1][x] for x in points])
    else:
        best = min([abs(x[0]) + abs(x[1]) for x in points])
    return best


def test(log):
    values = log.decode_values("""
        R75,D30,R83,U83,L12,D49,R71,U7,L72
        U62,R66,U55,R34,D71,R55,D58,R83
    """)

    ret, expected = calc(log, values, False), 159
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    ret, expected = calc(log, values, True), 610
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Manhattan distance: " + str(calc(log, values, False)))
    log("Fewest steps: " + str(calc(log, values, True)))

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

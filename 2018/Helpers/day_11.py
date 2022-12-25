#!/usr/bin/env python3

DAY_NUM = 11
DAY_DESC = 'Day 11: Chronal Charge'


def get_fuel(x, y, grid):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += grid
    power_level *= rack_id
    power_level //= 100
    power_level %= 10
    power_level -= 5
    return power_level


def calc(log, values):
    grid = [[0] * 300 for x in range(300)]
    for x in range(300):
        for y in range(300):
            grid[x][y] = get_fuel(x, y, values)

    overall_best_val = 0
    overall_best_msg = None
    ret = 0

    for size in range(1, 301):
        grid2 = [[0] * 300 for x in range(300)]
        for x in range(0, 300 - (size - 1)):
            for y in range(300):
                for i in range(size):
                    grid2[x][y] += grid[x+i][y]

        grid3 = [[0] * 300 for x in range(300)]
        for x in range(1, 300 - (size - 1)):
            for y in range(1, 300 - (size - 1)):
                for i in range(size):
                    grid3[x][y] += grid2[x][y+i]

        best_loc = None
        best_val = 0

        for x in range(1, 300 - (size - 1)):
            for y in range(1, 300 - (size - 1)):
                if best_loc is None or grid3[x][y] > best_val:
                    best_val = grid3[x][y]
                    best_loc = (x, y)

        msg = "Size: %d, Location: %d x %d, Value: %d" % (size, best_loc[0], best_loc[1], best_val)
        if size == 3:
            log(msg)
            ret = best_val
        if best_val >= overall_best_val:
            overall_best_val = best_val
            overall_best_msg = msg
        else:
            log(overall_best_msg)
            break

    return ret


def test(log):
    if calc(log, 18) == 29:
        return True
    else:
        return False


def run(log, values):
    log(calc(log, 5535))

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

#!/usr/bin/env python

def get_desc():
    return 11, 'Day 11: Chronal Charge'


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
            log.show(msg)
            ret = best_val
        if best_val >= overall_best_val:
            overall_best_val = best_val
            overall_best_msg = msg
        else:
            log.show(overall_best_msg)
            break

    return ret


def test(log):
    if calc(log, 18) == 29:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, 5535))

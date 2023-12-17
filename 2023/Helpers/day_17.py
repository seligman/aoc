#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Clumsy Crucible'

from heapq import heappop, heappush

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    min_dist, max_dist = (1, 3) if mode == 1 else (4, 10)

    todo = [(0, 0, 0, -1)]
    costs = {}
    while len(todo) > 0:
        cost, x, y, cur_dir = heappop(todo)
        if (x, y) == (grid.axis_max(0), grid.axis_max(1)):
            return cost
        for new_dir in range(4) if cur_dir == -1 else [(cur_dir + 1) % 4, (cur_dir + 3) % 4]:
            ox, oy = dirs[new_dir]
            added_cost = 0
            for steps in range(1, max_dist + 1):
                nx, ny = x + ox * steps, y + oy * steps
                if (nx, ny) in grid.grid:
                    added_cost += int(grid[nx, ny])
                    if steps >= min_dist:
                        if (nx, ny, new_dir) not in costs or costs[(nx, ny, new_dir)] > cost + added_cost:
                            costs[(nx, ny, new_dir)] = cost + added_cost
                            heappush(todo, (cost + added_cost, nx, ny, new_dir))
                else:
                    break

    return 0

def test(log):
    values = log.decode_values("""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
    """)

    log.test(calc(log, values, 1), '102')
    log.test(calc(log, values, 2), '94')

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

#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Toboggan Trajectory'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)
    ret = []

    if mode == 1:
        passes = [[3,1]]
    else:
        passes = [[1,1],[3,1],[5,1],[7,1],[1,2]]
    for step_x, step_y in passes:
        ret.append(0)
        x, y = 0, 0 
        while True:
            x += step_x
            y += step_y
            x = x % grid.width()
            if y >= grid.height():
                break
            if grid[x, y] == "#":
                ret[-1] += 1

    value = 1
    for x in ret:
        value *= x

    return value

def test(log):
    values = log.decode_values("""
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#
    """)

    log.test(calc(log, values, 1), 7)
    log.test(calc(log, values, 2), 336)

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

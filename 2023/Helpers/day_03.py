#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Gear Ratios'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    ret = 0
    digits = set("1234567890")
    part_numbers = []
    parts = []
    gears = []

    table = {}
    for (x, y), val in grid.grid.items():
        if val in digits:
            temp = table.get((x - 1, y), None)
            if temp is None:
                temp = {"val": 0, "pts": set()}
                part_numbers.append(temp)
            temp['val'] = temp['val'] * 10 + int(val)
            temp['pts'].add((x, y))
            table[(x, y)] = temp
        elif val != '.':
            parts.append((x, y))
            if val == "*":
                gears.append((x, y))

    if mode == 1:
        possible = set()
        for pt in parts:
            possible |= set(grid.get_dirs(2, pt))
        for pt in part_numbers:
            if len(pt['pts'] & possible):
                ret += pt['val']
    else:
        for pt in gears:
            neighbors = set(grid.get_dirs(2, pt))
            neighbors = [x for x in part_numbers if len(x['pts'] & neighbors)]
            if len(neighbors) == 2:
                ret += neighbors[0]['val'] * neighbors[1]['val']

    return ret

def test(log):
    values = log.decode_values("""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
    """)

    log.test(calc(log, values, 1), '4361')
    log.test(calc(log, values, 2), '467835')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

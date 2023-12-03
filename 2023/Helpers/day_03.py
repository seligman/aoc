#!/usr/bin/env python3

DAY_NUM = 3
DAY_DESC = 'Day 3: Gear Ratios'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)
    grid.default = "."

    nums = set("1234567890")
    ret = 0
    valid = set()
    for x in grid.x_range():
        for y in grid.y_range():
            if grid[x, y] in nums and grid[x - 1, y] not in nums:
                temp = ""
                x2 = x
                part_no = False
                maybe = []
                while grid[x2, y] in nums:
                    temp += grid[x2, y]
                    maybe.append((x2, y))
                    for pt in grid.get_dirs(2, (x2, y)):
                        if grid[pt] not in {".", 0} | nums:
                            part_no = True
                    x2 += 1
                if part_no:
                    ret += int(temp)
                    for cur in maybe:
                        valid.add(cur)
    if mode != 1:
        ret = 0
        for x in grid.x_range():
            for y in grid.y_range():
                if grid[x, y] == "*":
                    hits = []
                    for pt in grid.get_dirs(2, (x, y)):
                        if grid[pt] in nums:
                            hits.append(pt)

                    used = set()
                    vals = []
                    for ox, oy in hits:
                        temp = ""
                        if (ox, oy) not in used:
                            while grid[ox - 1, oy] in nums:
                                ox -= 1
                            while grid[ox, oy] in nums:
                                used.add((ox, oy))
                                temp += grid[ox, oy]
                                ox += 1
                            if len(temp) > 0:
                                vals.append(temp)
                    if len(vals) == 2:
                        vals[0] = int(vals[0])
                        vals[1] = int(vals[1])
                        ret += int(vals[0]) * int(vals[1])

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
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

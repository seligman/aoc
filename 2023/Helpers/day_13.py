#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Point of Incidence'

def calc(log, values, mode):
    from grid import Grid, Point

    ret = 0
    temp = []
    for row in values + [""]:
        if len(row) == 0:
            grid = Grid.from_text(temp)

            hit = False
            for x in range(1, grid.axis_max(0)+1):
                a = tuple(grid.column(i) for i in range(x - 1, -1, -1))
                b = tuple(grid.column(i) for i in range(x, grid.axis_max(0) + 1))
                target = min(len(a), len(b))
                a = "".join(a[:target])
                b = "".join(b[:target])
                diffs = sum(0 if a == b else 1 for a, b in zip(a, b))
                if diffs == (0 if mode == 1 else 1):
                    ret += x
                    hit = True
                    break

            if not hit:
                for y in range(1, grid.axis_max(1)+1):
                    a = tuple(grid.row(i) for i in range(y - 1, -1, -1))
                    b = tuple(grid.row(i) for i in range(y, grid.axis_max(1) + 1))
                    target = min(len(a), len(b))
                    a = "".join(a[:target])
                    b = "".join(b[:target])
                    diffs = sum(0 if a == b else 1 for a, b in zip(a, b))
                    if diffs == (0 if mode == 1 else 1):
                        ret += y * 100
                        hit = True
                        break

            if not hit:
                print(temp)
                raise Exception()

            temp = []
        else:
            temp.append(row)


    # TODO
    return ret

def test(log):
    values = log.decode_values("""
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
    """)

    log.test(calc(log, values, 1), '405')
    log.test(calc(log, values, 2), '400')

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

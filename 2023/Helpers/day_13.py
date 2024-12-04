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
            for side in [0, 1]:
                for off in range(1, grid.axis_max(side)+1):
                    target = min(off, grid.axis_max(side) - off + 1)
                    a = "".join(grid.side(side, i) for i in range(off - 1, -1, -1))
                    b = "".join(grid.side(side, i) for i in range(off, off + target))
                    diffs = sum(0 if a == b else 1 for a, b in zip(a, b))
                    if diffs == (0 if mode == 1 else 1):
                        ret += off * (1 if side == 0 else 100)
                        hit = True
                        break
                if hit:
                    break

            if not hit:
                log(str(temp))
                raise Exception()

            temp = []
        else:
            temp.append(row)

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
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

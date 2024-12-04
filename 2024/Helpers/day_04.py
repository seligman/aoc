#!/usr/bin/env python3

DAY_NUM = 4
DAY_DESC = 'Day 4: Ceres Search'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values, default=".")

    ret = 0
    if mode == 1:
        for x, y in grid.xy_range():
            if grid[x, y] == "X":
                for ox, oy in Grid.get_dirs(2, diagonal=True):
                    good = True
                    for i in range(4):
                        if grid[x + ox * i, y + oy * i] != "XMAS"[i]:
                            good = False
                            break
                    if good:
                        ret += 1
    else:
        for x, y in grid.xy_range():
            if grid[x,y] == "A":
                if grid[x-1,y-1] + grid[x+1,y+1] in {"MS", "SM"}:
                    if grid[x-1,y+1] + grid[x+1,y-1] in {"MS", "SM"}:
                        ret += 1

    return ret

def test(log):
    values = log.decode_values("""
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
    """)

    log.test(calc(log, values, 1), '18')
    log.test(calc(log, values, 2), '9')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

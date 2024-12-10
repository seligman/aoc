#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'TODO'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    starts = set()
    for xy in grid.xy_range():
        if grid[xy] == "0":
            starts.add(xy)
    
    ret = 0
    for start in starts:
        todo = [(start, 1)]
        scores = set()
        scores2 = 0
        while len(todo) > 0:
            (x, y), height = todo.pop(0)
            if height == 10:
                scores.add((x, y))
                scores2 += 1
            for ox, oy in Grid.get_dirs(2, diagonal=False):
                xy = x + ox, y + oy
                if grid[xy] == str(height):
                    # print(xy)
                    todo.append((xy, height + 1))
        if mode == 1:
            ret += len(scores)
        else:
            ret += scores2
    return ret

def test(log):
    values = log.decode_values("""
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
    """)

    log.test(calc(log, values, 1), '36')
    log.test(calc(log, values, 2), '81')

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

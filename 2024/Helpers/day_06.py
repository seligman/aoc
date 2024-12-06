#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Guard Gallivant'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values, default="X")

    rots = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    rot = 0

    for x, y in grid.xy_range():
        if grid[x, y] == "^":
            pos_x, pos_y = x, y
            start_x, start_y = x, y
            break
    
    seen = set()
    while True:
        nx, ny = pos_x + rots[rot % 4][0], pos_y + rots[rot % 4][1]
        if grid[nx, ny] == "#":
            rot += 1
        elif grid[nx, ny] in {".", "^"}:
            seen.add((nx, ny))
            pos_x, pos_y = nx, ny
        elif grid[nx, ny] == "X":
            break

    if mode == 1:
        return len(seen)
    
    ret = 0
    for test_x, test_y in seen:
        grid[test_x, test_y] = "#"
        rot = 0

        pos_x, pos_y = start_x, start_y

        loop = set()

        while True:
            nx, ny = pos_x + rots[rot % 4][0], pos_y + rots[rot % 4][1]
            if grid[nx, ny] == "#":
                rot += 1
            elif grid[nx, ny] in {".", "^"}:
                key = (nx, ny, rots[rot % 4][0], rots[rot % 4][1])
                if key in loop:
                    ret += 1
                    break
                loop.add(key)
                pos_x, pos_y = nx, ny
            elif grid[nx, ny] == "X":
                break
        grid[test_x, test_y] = "."
    return ret

    return 0

def test(log):
    values = log.decode_values("""
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """)

    log.test(calc(log, values, 1), '41')
    log.test(calc(log, values, 2), '6')

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

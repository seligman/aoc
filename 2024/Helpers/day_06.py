#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Guard Gallivant'

def calc(log, values, mode):
    # TODO: Delete or use these
    # from parsers import get_ints, get_floats
    from grid import Grid, Point
    grid = Grid.from_text(values, default="X")

    rots = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    temp = rots.pop(0)
    dir_x, dir_y = temp
    rots.append(temp)
    for x, y in grid.xy_range():
        if grid[x, y] == "^":
            pos_x, pos_y = x, y
            start_x, start_y = x, y
            break
    
    seen = set()
    while True:
        nx, ny = pos_x + dir_x, pos_y + dir_y
        if grid[nx, ny] == "#":
            temp = rots.pop(0)
            dir_x, dir_y = temp
            rots.append(temp)
        elif grid[nx, ny] in {".", "^"}:
            seen.add((nx, ny))
            pos_x, pos_y = nx, ny
        elif grid[nx, ny] == "X":
            break
        # grid.show_grid(log, {".": ".", "^": "^", "#": "#"})

    if mode == 1:
        return len(seen)
    
    ret = 0
    for test_x, test_y in seen:
        # test_x, test_y = start_x - 1, start_y
        grid[test_x, test_y] = "#"
        rots = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        temp = rots.pop(0)
        dir_x, dir_y = temp
        rots.append(temp)

        pos_x, pos_y = start_x, start_y


        loop = set()

        while True:
            nx, ny = pos_x + dir_x, pos_y + dir_y
            # grid[pos_x, pos_y] = "^"
            # grid.show_grid(log, {".": ".", "^": "^", "#": "#"})
            if grid[nx, ny] == "#":
                temp = rots.pop(0)
                dir_x, dir_y = temp
                rots.append(temp)
            elif grid[nx, ny] in {".", "^"}:
                if (nx, ny, dir_x, dir_y) in loop:
                    ret += 1
                    break
                loop.add((nx, ny, dir_x, dir_y))
                pos_x, pos_y = nx, ny
            elif grid[nx, ny] == "X":
                break
        # print(len(loop))
        grid[test_x, test_y] = "."
        # break
    return ret

    # from program import Program
    # program = Program(values)

    # TODO
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
    log.test(calc(log, values, 2), 'TODO')

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

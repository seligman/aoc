#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Garden Groups'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    areas = []

    for xy in grid.xy_range():
        if grid[xy] != "#":
            temp = grid[xy]
            grid[xy] = "#"
            areas.append(set([xy]))
            todo = [xy]
            while len(todo) > 0:
                xy = todo.pop(0)
                for oxy in grid.get_dirs(axis_count=2, diagonal=False, offset=xy):
                    if grid[oxy] == temp:
                        grid[oxy] = "#"
                        todo.append(oxy)
                        areas[-1].add(oxy)
    ret =  0
    for area in areas:
        border_count = 0
        side_count = 0
        for xy in area:
            for oxy in grid.get_dirs(axis_count=2, diagonal=False, offset=xy):
                if oxy not in area:
                    border_count += 1


        for oxy in (0, 1), (0, -1), (1, 0), (-1, 0):
            side = set()
            for xy in area:
                temp = xy[0] + oxy[0], xy[1] + oxy[1]
                if temp not in area:
                    side.add(temp)
            to_remove = set()
            for xy in side:
                temp = xy[0] + oxy[1], xy[1] + oxy[0]
                while temp in side:
                    to_remove.add(temp)
                    temp = temp[0] + oxy[1], temp[1] + oxy[0]
            side_count += len(side) - len(to_remove)

        if mode == 1:
            ret += len(area) * border_count
        else:
            ret += len(area) * side_count
    return ret

def test(log):
    values = log.decode_values("""
        RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE
    """)

    log.test(calc(log, values, 1), '1930')
    log.test(calc(log, values, 2), '1206')

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

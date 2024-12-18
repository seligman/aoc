#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: RAM Run'

def calc(log, values, mode, limit, size):
    from grid import Grid, Point
    size += 1

    if mode == 1:
        target = (limit, limit + 1, 1)
    else:
        target = (0, len(values) + 1, 1024)

    while True:
        last_true = None
        not_true = None
        for i in range(*target):
            grid = Grid()
            for row in values[:i]:
                row = row.split(",")
                grid[int(row[0]), int(row[1])] = "#"

            todo = [(Point(0,0), 0)]
            end = Point(size - 1, size - 1)
            seen = set()
            found = False
            while len(todo) > 0:
                xy, steps = todo.pop(0)
                if xy == end:
                    if mode == 1:
                        return steps
                    else:
                        found = True
                        todo = []
                        break
                for o in grid.get_dirs(2, diagonal=False):
                    o = xy + Point(o)
                    if o.x >= 0 and o.y >= 0 and o.x < size and o.y < size:
                        if o not in seen:
                            seen.add(o)
                            if grid[o] != "#":
                                todo.append((o, steps + 1))

            if found:
                last_true = i
            else:
                not_true = i
                break
        
        if last_true is not None and not_true is not None:
            if target[2] == 1:
                return values[last_true]
            target = (last_true, not_true + 1, target[2] // 2)
        else:
            target = (target[0], target[1], target[2] // 2)

    return 0

def test(log):
    values = log.decode_values("""
        5,4
        4,2
        4,5
        3,0
        2,1
        6,3
        2,4
        1,5
        0,6
        3,3
        2,6
        5,1
        1,2
        5,5
        2,5
        6,5
        1,4
        0,4
        6,4
        1,1
        6,1
        1,0
        0,5
        1,6
        2,0
    """)

    log.test(calc(log, values, 1, 12, 6), '22')
    log.test(calc(log, values, 2, 12, 6), '6,1')

def run(log, values):
    log(calc(log, values, 1, 1024, 70))
    log(calc(log, values, 2, 1024, 70))

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

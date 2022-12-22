#!/usr/bin/env python3

DAY_NUM = 22
DAY_DESC = 'Day 22: Monkey Map'

# I give up
def paper_box_coords(pt, cur_dir):
    if cur_dir == (1, 0):
        if pt.x == 149: return (99, 149 - pt.y), (-1, 0)
        if pt.x == 99:
            if 50 <= pt.y <= 99: return (99 + (pt.y - 49), 49), (0, -1)
            if 100 <= pt.y <= 149: return (149, 50 - (pt.y - 99)), (-1, 0)
        if pt.x == 49: return (49 + (pt.y - 149), 149), (0, -1)
    elif cur_dir == (0, 1):
        if pt.y == 49: return (99, pt.x - 50), (-1, 0)
        if pt.y == 149: return (49, pt.x + 100), (-1, 0)
        if pt.y == 199: return (pt.x + 100, 0), (0, 1)
    elif cur_dir == (-1, 0):
        if pt.x == 50:
            if 0 <= pt.y <= 49: return (0, 149 - pt.y), (1, 0)
            if 50 <= pt.y <= 99: return (pt.y - 50, 100), (0, 1)
        if pt.x == 0:
            if 100 <= pt.y <= 149: return (50, 149 - pt.y), (1, 0)
            if 150 <= pt.y <= 199: return (pt.y - 149 + 49, 0), (0, 1)
    elif cur_dir == (0, -1):
        if pt.y == 0:
            if 50 <= pt.x <= 99: return (0, pt.x + 100), (1, 0)
            if 100 <= pt.x <= 149: return (pt.x - 100, 199), (0, -1)
        if pt.y == 100: return (50, pt.x+50), (1, 0)

def calc(log, values, mode, is_test=False):
    values = [x.replace("] ", "") for x in values]
    from grid import Grid, Point
    grid = Grid.from_text(values[:-2])
    pattern = values[-1]

    for x in grid.x_range():
        if grid[(x, 0)] == ".":
            pt = Point(x, 0)
    
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    cur_dir = 0

    pattern = pattern.replace("L", " L ")
    pattern = pattern.replace("R", " R ")
    pattern = pattern.strip().split(" ")

    extra = 0
    for cur in pattern:
        if cur == "R":
            cur_dir = (cur_dir + 1) % 4
        elif cur == "L":
            cur_dir = (cur_dir - 1) % 4
        else:
            cur = int(cur)
            for _ in range(cur):
                if mode == 1:
                    next_pt = pt + dirs[(cur_dir + extra) % 4]
                    next_extra = extra
                else:
                    next_extra = extra
                    if mode == 2 and not is_test:
                        next_pt = pt + dirs[(cur_dir + extra) % 4]
                        if grid[next_pt] not in {".", "#"}:
                            temp_pt, temp_dir = paper_box_coords(pt, dirs[(cur_dir + extra) % 4])
                            while dirs[(cur_dir + next_extra) % 4] != temp_dir:
                                next_extra += 1
                            next_pt = Point(*temp_pt)
                if mode == 1:
                    while grid[next_pt] not in {".", "#"}:
                        if mode == 1:
                            next_pt += dirs[(cur_dir + extra) % 4]
                            next_pt = Point(next_pt.x % (grid.axis_max(0) + 1), next_pt.y % (grid.axis_max(1) + 1))

                if grid[next_pt] == "#":
                    break
                pt = next_pt
                extra = next_extra
    return (pt.y + 1) * 1000 + (pt.x + 1) * 4 + ((cur_dir + extra) % 4)

def test(log):
    values = log.decode_values("""
        ]         ...#
        ]         .#..
        ]         #...
        ]         ....
        ] ...#.......#
        ] ........#...
        ] ..#....#....
        ] ..........#.
        ]         ...#....
        ]         .....#..
        ]         .#......
        ]         ......#.
        ] 
        ] 10R5L5R10L4R5L5        
    """)

    log.test(calc(log, values, 1, is_test=True), '6032')
    # log.test(calc(log, values, 2, is_test=True), '5031')

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

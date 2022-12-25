#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Planet of Discord'


def calc(log, values):
    from grid import Grid
    
    cur = Grid.from_text(values)

    seen = set()
    while True:
        value = 0
        for y in cur.y_range():
            for x in cur.x_range():
                if cur.get(x, y) == "#":
                    value += 2 ** (x + y * 5)

        if value in seen:
            return value
        
        seen.add(value)

        n = Grid()
        for x in range(5):
            for y in range(5):
                count = 0
                for xo, yo in [[0,1],[0,-1],[1,0],[-1,0]]:
                    count += 1 if cur.get(x + xo, y + yo) == "#" else 0
                if cur.get(x, y) == "#":
                    if count == 1:
                        n.set("#", x, y)
                else:
                    if count == 1 or count == 2:
                        n.set("#", x, y)

        cur = n


def calc_ndimension(log, values, animate=False):
    from grid import Grid
    from collections import defaultdict

    levels = defaultdict(int)
    temp = Grid.from_text(values)
    for x in temp.x_range():
        for y in temp.y_range():
            if temp.get(x, y) == "#":
                levels[(0, x, y)] = 1

    show = Grid()

    for shown in range(201):
        if animate:
            show.grid.clear()
            for x in range(16):
                for y in range(15*6+1):
                    show.set("#", x*6, y)
            for y in range(16):
                for x in range(15*6+1):
                    show.set("#", x, y*6)
            for x in range(15):
                for y in range(15):
                    show.set("DarkGray", x * 6 + 1 + 2, y * 6 + 1 + 2)
            bugs = 0
            for d in range(-100, 101):
                for x in range(5):
                    for y in range(5):
                        if levels[(d, x, y)] == 1:
                            show.set("Gray", ((d + 112) % 15) * 6 + 1 + x, (d + 112) // 15 * 6 + 1 + y)
                            bugs += 1
            for i in range(5):
                show.draw_grid(extra_text=[
                    "Minutes: %03d   Bugs: %05d" % (shown, bugs)
                ], font_size=20)
        if shown == 200:
            break

        next_levels = defaultdict(int)
        for d in range(-(shown // 2 + 3), shown // 2 + 4):
            for y in range(5):
                for x in range(5):
                    if (x, y) != (2, 2):
                        cells = []
                        if (x, y) == (2, 1):
                            for i in range(5):
                                cells.append((1, i, 0))
                        if (x, y) == (2, 3):
                            for i in range(5):
                                cells.append((1, i, 4))
                        if (x, y) == (1, 2):
                            for i in range(5):
                                cells.append((1, 0, i))
                        if (x, y) == (3, 2):
                            for i in range(5):
                                cells.append((1, 4, i))

                        if x == 0:
                            cells.append((-1, 1, 2))
                        if y == 0:
                            cells.append((-1, 2, 1))
                        if x == 4:
                            cells.append((-1, 3, 2))
                        if y == 4:
                            cells.append((-1, 2, 3))

                        for xo, yo in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                            xo += x
                            yo += y
                            if (xo, yo) != (2, 2) and xo >= 0 and xo <= 4 and yo >= 0 and yo <= 4:
                                cells.append((0, xo, yo))

                        count = 0

                        for do, xo, yo in cells:
                            do += d
                            if levels[(do, xo, yo)] == 1:
                                count += 1

                        val = 0
                        if levels[(d, x, y)] == 1:
                            if count == 1:
                                val = 1
                        else:
                            if count == 1 or count == 2:
                                val = 1

                        if val == 1:
                            next_levels[(d, x, y)] = 1
        
        levels = next_levels                    

    return len(levels)


def test(log):
    values = log.decode_values("""
        ....#
        #..#.
        #..##
        ..#..
        #....
    """)

    ret, expected = calc(log, values), 2129920
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def other_animate(describe, values):
    if describe:
        return "Animate the work"
    from dummylog import DummyLog
    from grid import Grid
    Grid.clear_frames()
    calc_ndimension(DummyLog, values, animate=True)
    Grid.make_animation(file_format="mp4", output_name="animation_%02d" % (get_desc()[0],))
    print("Done, created animation...")


def run(log, values):
    log("Diversity value: " + str(calc(log, values)))
    log("Number of multi-dimensional bugs: " + str(calc_ndimension(log, values)))

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

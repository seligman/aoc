#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Donut Maze'


def calc(log, values, iterate, animate=False):
    from grid import Grid
    grid = Grid.from_text(values)
    grid.default = " "

    warps = {}
    levels = {}
    portals = {}
    reverse = {}

    for x in grid.x_range():
        for y in grid.y_range():
            for xo, yo, name in [
                (x - 1, y, grid.get(x, y) + grid.get(x + 1, y)),
                (x + 2, y, grid.get(x, y) + grid.get(x + 1, y)),
                (x, y - 1, grid.get(x, y) + grid.get(x, y + 1)),
                (x, y + 2, grid.get(x, y) + grid.get(x, y + 1)),
            ]:
                outer = x == 0 or x == grid.axis_max(0) - 1 or y == 0 or y == grid.axis_max(1) - 1
                if grid.get(xo, yo) == "." and name.isalpha():
                    if name not in warps:
                        warps[name] = []
                    warps[name].append((xo, yo))
                    levels[(xo, yo)] = outer

    for name in list(warps):
        if len(warps[name]) == 2:
            portals[warps[name][0]] = warps[name][1]
            portals[warps[name][1]] = warps[name][0]
            reverse[warps[name][1]] = name
        reverse[warps[name][0]] = name

    paths = {}
    trails = {}

    from collections import deque
    
    for start in list(portals) + warps["AA"]:
        if start in paths:
            raise Exception()
        paths[start] = []
        trails[start] = {}
        todo = deque()
        todo.append((start[0], start[1], 0, []))
        done = set([start])

        while len(todo) > 0:
            x, y, steps, trail = todo.popleft()
            for xo, yo in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                if (x + xo, y + yo) not in done:
                    done.add((x + xo, y + yo))
                    if grid.get(x + xo, y + yo) == ".":
                        todo.appendleft((x + xo, y + yo, steps + 1, trail + [(x + xo, y + yo)]))
                        if (x + xo, y + yo) in portals:
                            paths[start].append(((x + xo, y + yo), steps + 1))
                            trails[start][(x + xo, y + yo)] = trail[:]
                        elif (x + xo, y + yo) == warps["ZZ"][0]:
                            paths[start].append(((x + xo, y + yo), steps))
                            trails[start][(x + xo, y + yo)] = trail[:]

    clean_grid = grid.grid.copy()
    shown = 0
    total_shown = -1

    todo.append((warps["AA"][0], 0, 0, set(), []))
    while len(todo) > 0:
        start, level, steps, used, trail = todo.pop()
        if start in portals:
            if iterate:
                level += 1 if levels[start] else -1
            start = portals[start]

        if level <= 0:
            if start == warps["ZZ"][0]:
                if level == 0:
                    if animate:
                        Grid.clear_frames()
                        for start, dest, level in trail:
                            print(start, dest, level)
                            dots = trails[start][dest]
                            total_shown += 2
                            for x, y in dots:
                                grid.set("Target", x, y)
                                shown += 1
                                total_shown += 1
                                if shown == 15:
                                    shown = 0
                                    grid.draw_grid(extra_text=["Steps: | %06d" % (total_shown,), "Inception Level: | %02d" % (-level,)], text_xy=(500, 900))
                                    grid.grid = clean_grid.copy()
                        for _ in range(10):
                            grid.draw_grid(extra_text=["Steps: | %06d" % (total_shown,), "Inception Level: | %02d" % (-level,)], text_xy=(500, 900))
                        Grid.make_animation(file_format="mp4", output_name="animation_%02d" % (get_desc()[0],))
                    return steps
            else:
                for dest, next_steps in paths.get(start, []):
                    if (dest, level) not in used:
                        todo.appendleft((
                            dest, 
                            level, 
                            steps + next_steps + 1, 
                            used | set([(dest, level),]), 
                            trail + [(start, dest, level),],
                        ))

    raise Exception()


def test(log):
    values = log.decode_values("""
        =                  A               
        =                  A               
        = #################.#############  
        = #.#...#...................#.#.#  
        = #.#.#.###.###.###.#########.#.#  
        = #.#.#.......#...#.....#.#.#...#  
        = #.#########.###.#####.#.#.###.#  
        = #.............#.#.....#.......#  
        = ###.###########.###.#####.#.#.#  
        = #.....#        A   C    #.#.#.#  
        = #######        S   P    #####.#  
        = #.#...#                 #......VT
        = #.#.#.#                 #.#####  
        = #...#.#               YN....#.#  
        = #.###.#                 #####.#  
        DI....#.#                 #.....#  
        = #####.#                 #.###.#  
        ZZ......#               QG....#..AS
        = ###.###                 #######  
        JO..#.#.#                 #.....#  
        = #.#.#.#                 ###.#.#  
        = #...#..DI             BU....#..LF
        = #####.#                 #.#####  
        YN......#               VT..#....QG
        = #.###.#                 #.###.#  
        = #.#...#                 #.....#  
        = ###.###    J L     J    #.#.###  
        = #.....#    O F     P    #.#...#  
        = #.###.#####.#.#####.#####.###.#  
        = #...#.#.#...#.....#.....#.#...#  
        = #.#####.###.###.#.#.#########.#  
        = #...#.#.....#...#.#.#.#.....#.#  
        = #.###.#####.###.###.#.#.#######  
        = #.#.........#...#.............#  
        = #########.###.###.#############  
        =          B   J   C               
        =          U   P   P               
    """)

    ret, expected = calc(log, values, False), 58
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False


    values = log.decode_values("""
        =            Z L X W       C                 
        =            Z P Q B       K                 
        = ###########.#.#.#.#######.###############  
        = #...#.......#.#.......#.#.......#.#.#...#  
        = ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
        = #.#...#.#.#...#.#.#...#...#...#.#.......#  
        = #.###.#######.###.###.#.###.###.#.#######  
        = #...#.......#.#...#...#.............#...#  
        = #.#########.#######.#.#######.#######.###  
        = #...#.#    F       R I       Z    #.#.#.#  
        = #.###.#    D       E C       H    #.#.#.#  
        = #.#...#                           #...#.#  
        = #.###.#                           #.###.#  
        = #.#....OA                       WB..#.#..ZH
        = #.###.#                           #.#.#.#  
        CJ......#                           #.....#  
        = #######                           #######  
        = #.#....CK                         #......IC
        = #.###.#                           #.###.#  
        = #.....#                           #...#.#  
        = ###.###                           #.#.#.#  
        XF....#.#                         RF..#.#.#  
        = #####.#                           #######  
        = #......CJ                       NM..#...#  
        = ###.#.#                           #.###.#  
        RE....#.#                           #......RF
        = ###.###        X   X       L      #.#.#.#  
        = #.....#        F   Q       P      #.#.#.#  
        = ###.###########.###.#######.#########.###  
        = #.....#...#.....#.......#...#.....#.#...#  
        = #####.#.###.#######.#######.###.###.#.#.#  
        = #.......#.......#.#.#.#.#...#...#...#.#.#  
        = #####.###.#####.#.#.#.#.###.###.#.###.###  
        = #.......#.....#.#...#...............#...#  
        = #############.#.#.###.###################  
        =              A O F   N                     
        =              A A D   M                     
    """)

    ret, expected = calc(log, values, True), 396
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def other_animate(describe, values):
    if describe:
        return "Animate the work"
    from dummylog import DummyLog
    calc(DummyLog(), values, True, animate=True)
    print("Done, created animation...")


def run(log, values):
    log("One Level: " + str(calc(log, values, False)))
    log("Many Levels: " + str(calc(log, values, True)))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

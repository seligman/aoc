#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Many-Worlds Interpretation'

def calc(log, values, mode, animate=False):
    from grid import Grid, DEFAULT_COLOR_MAP
    from collections import deque

    DEFAULT_COLOR_MAP["Target"] = (255, 64, 64)
    DEFAULT_COLOR_MAP["Region"] = (0, 0, 128)

    grid = Grid()

    doors = set()
    keys = set()
    y = 0
    for row in values:
        x = 0
        for cur in row:
            grid.set(cur, x, y)
            if cur == "@":
                start_x, start_y = x, y
            if cur in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                doors.add(cur)
            if cur in "abcdefghijklmnopqrstuvwxyz":
                keys.add(cur)
            x += 1
        y += 1

    if mode == 1:
        temp = Grid.from_text([x.strip() for x in """
            @#@
            ###
            @#@
        """.strip().split("\n")])

        for x in range(3):
            for y in range(3):
                grid.set(temp.get(x, y), start_x - 1 + x, start_y - 1 + y)

    skip = False
    if animate:
        import os
        import json
        if os.path.isfile("dump_18.json"):
            with open("dump_18.json") as f:
                best_moves = json.load(f)
                skip = True

    if not skip:
        trails = {}
        robots = 0
        for start_x in grid.x_range():
            for start_y in grid.y_range():
                cell = grid.get(start_x, start_y)
                if cell == "@" or cell in keys:
                    if cell == "@":
                        cell = robots
                        robots += 1

                    if cell not in trails:
                        trails[cell] = []

                    todo = deque()
                    todo.append((start_x, start_y, set(), 0, [], ""))
                    used = set([start_x, start_y])
                    while len(todo) > 0:
                        x, y, needed_doors, steps, moves, sub = todo.popleft()
                        if sub in keys:
                            trails[cell].append((steps, sub, needed_doors, moves))
                        if sub in doors:
                            needed_doors = needed_doors | set([sub.lower()])
                        for xo, yo in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            if (x + xo, y + yo)  not in used:
                                used.add((x + xo, y + yo))
                                sub = grid.get(x + xo, y + yo)
                                if sub != "#":
                                    todo.append((x + xo, y + yo, needed_doors, steps + 1, moves + [(x + xo, y + yo)], sub))

        todo = deque()
        all_robots = list(range(robots))
        todo.append((all_robots, set(), 0, []))
        used = {}
        best = None
        while len(todo) > 0:
            pos, haves, steps, my_moves = todo.popleft()
            if len(haves) == len(keys):
                if best is None or steps < best:
                    best = steps
                    best_moves = my_moves[:]
            else:
                for i in all_robots:
                    for extra_steps, dest, needed_doors, moves in trails[pos[i]]:
                        if dest not in haves and needed_doors.issubset(haves):
                            temp = pos[:]
                            temp[i] = dest
                            a = tuple(temp) + tuple(sorted(haves))
                            if a not in used or used[a] > steps + extra_steps:
                                used[a] = steps + extra_steps
                                if animate:
                                    temp_moves = my_moves + [i] + moves
                                else:
                                    temp_moves = my_moves
                                todo.append((temp, haves | set(dest), steps + extra_steps, temp_moves))

        if animate:
            import json
            with open("dump_18.json", "w") as f:
                json.dump(best_moves, f)

    if animate:
        Grid.clear_frames()

        steps = 0
        grid.draw_grid(extra_text=["Steps: | %06d" % (steps,), "Keys: ", "Doors:"])
        passed_keys = set()
        passed_doors = set()
        lasts = {}
        i = 0
        for desc in best_moves:
            if isinstance(desc, int):
                i = desc
                for x in grid.x_range():
                    for y in grid.y_range():
                        # Region
                        in_region = False
                        if i == 0:
                            in_region = x < grid.axis_max(0) / 2 and y < grid.axis_max(1) / 2
                        elif i == 1:
                            in_region = x < grid.axis_max(0) / 2 and y >= grid.axis_max(1) / 2
                        elif i == 2:
                            in_region = x >= grid.axis_max(0) / 2 and y < grid.axis_max(1) / 2
                        elif i == 3:
                            in_region = x >= grid.axis_max(0) / 2 and y >= grid.axis_max(1) / 2

                        if grid.get(x, y) in {".", "Region"}:
                            grid.set("Region" if in_region else ".", x, y)
            else:
                x, y = desc
                if steps % 5 == 0:
                    log("Frame: " + str(steps))
                if grid.get(x, y) in keys:
                    passed_keys.add(grid.get(x, y))
                if grid.get(x, y) in doors:
                    passed_doors.add(grid.get(x, y))
                skip = False
                if i in lasts:
                    if (lasts[i][0], lasts[i][1]) == (x, y):
                        skip = True
                    else:
                        grid.set(lasts[i][2], lasts[i][0], lasts[i][1])
                if not skip:
                    steps += 1
                    lasts[i] = (x, y, grid.get(x, y))
                    grid.set("Target", x, y)
                    grid.draw_grid(extra_text=[
                        "Steps: | %06d" % (steps,), 
                        "Keys: " + "".join(sorted(passed_keys)), 
                        "Doors: " + "".join(sorted(passed_doors)),
                    ])

        for _ in range(30):
            grid.draw_grid(extra_text=[
                "Steps: | %06d" % (steps,), 
                "Keys: " + "".join(sorted(passed_keys)), 
                "Doors: " + "".join(sorted(passed_doors)),
            ])

        Grid.make_animation(file_format="mp4", output_name="animation_%02d" % (get_desc()[0],))        

    return best

def test(log):
    values = log.decode_values("""
        ########################
        #@..............ac.GI.b#
        ###d#e#f################
        ###A#B#C################
        ###g#h#i################
        ########################
    """)

    ret, expected = calc(log, values, 0), 81
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True

def other_animate(describe, values):
    if describe:
        return "Animate the work"
    from dummylog import DummyLog
    calc(DummyLog(), values, 1, animate=True)
    print("Done, created animation...")

def run(log, values):
    log("Part 1: " + str(calc(log, values, 0)))
    log("Part 2: " + str(calc(log, values, 1)))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

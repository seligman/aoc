#!/usr/bin/env python3

# Animation: https://youtu.be/bcK-ThfHx9o

DAY_NUM = 23
DAY_DESC = 'Day 23: A Long Walk'

from collections import defaultdict, deque

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    for x in grid.x_range():
        if grid[x, grid.height() - 1] == ".":
            final = (x, grid.height() - 1)
        if grid[x, 0] == ".":
            start = (x, 0)

    if draw:
        # Simplify the drawing a bit
        for xy, val in list(grid.grid.items()):
            if val in {"<", ">", "v", "^"}:
                grid[xy] = "."
        grid.save_frame()

    # Find all the points in the maze where a choice needs to be made
    to_check = deque([(start, (0, 1))])
    trails = defaultdict(list)
    trail_steps = defaultdict(list)
    while len(to_check) > 0:
        cur_cell, cur_dir = to_check.popleft()
        x, y = cur_cell[0] + cur_dir[0], cur_cell[1] + cur_dir[1]
        todo = deque([(x, y, 1, [(x, y)])])
        seen = set([cur_cell])
        while len(todo) > 0:
            x, y, steps, cells = todo.popleft()
            if (x, y) not in seen:
                seen.add((x, y))
                possible = []
                for ox, oy, od in [(1, 0, ">"), (-1, 0, "<"), (0, -1, "^"), (0, 1, "v")]:
                    if (x+ox, y+oy) not in seen:
                        if (mode == 1 and grid[x+ox, y+oy] in {".", od}) or (mode == 2 and grid[x+ox, y+oy] in {".", "<", ">", "^", "v"}):
                            possible.append((ox, oy))
                if len(possible) > 1:
                    for ox, oy in possible:
                        if (x, y, steps) not in trails[cur_cell]:
                            trails[cur_cell].append((x, y, steps))
                            trail_steps[cur_cell].append(cells)
                        if (x, y) not in trails:
                            to_check.append(((x, y), (ox, oy)))
                elif len(possible) == 1:
                    todo.append((possible[0][0] + x, possible[0][1] + y, steps + 1, cells + [(possible[0][0] + x, possible[0][1] + y)]))
                else:
                    if (x, y, steps) not in trails[cur_cell]:
                        trails[cur_cell].append((x, y, steps))
                        trail_steps[cur_cell].append(cells)

    # Flatten all the points to a unique ID to remove any hashmap lookups
    to_id = {}
    for xy in trails:
        to_id[xy] = len(to_id)
    if final not in to_id:
        to_id[final] = len(to_id)
    start_id, final_id = to_id[start], to_id[final]
    trails_id = {}
    step_cache = {}
    for xy in trails:
        trail = trails[xy]
        cells = trail_steps[xy]
        temp = []
        for (x, y, steps), (step_cells) in zip(trail, cells):
            cache_id = len(step_cache)
            step_cache[cache_id] = step_cells
            temp.append((to_id[(x, y)], steps, cache_id))
        trails_id[to_id[xy]] = temp
    trails_id = [trails_id[key] for key in sorted(trails_id)]

    seen = [False for _ in to_id]
    found = []
    possible_found = [0]

    def dfs(cur_id, steps, cells):
        if seen[cur_id]: return 0
        if cur_id == final_id: 
            if draw:
                possible_found[0] += 1
                if True: # len(found) < 1000:
                    if len(found) % 1000 == 0:
                        print(f"Found {len(found):,} {len(cells)}")
                    found.append(cells)
                else:
                    if possible_found[0] % 1000 == 0:
                        print(f"Possible {possible_found[0]:,}")
            return steps

        seen[cur_id] = True
        ret = 0
        for other_id, to_add, new_cells in trails_id[cur_id]:
            ret = max(ret, dfs(other_id, steps + to_add, cells + [new_cells] if draw else None))
        seen[cur_id] = False
        return ret

    ret = dfs(start_id, 0, [])

    if draw:
        found = [
            {
                "cache": x,
                "temp": [],
                "i": 0,
                "best": False,
                "len": sum(len(step_cache[y]) for y in x),
            } for x in found
        ]
        found.sort(key=lambda x: x["len"], reverse=True)
        found[0]['best'] = True

        steps = []
        while True:
            hit, best_set, all_set = False, set(), set()
            for cur in found:
                if cur["i"] >= len(cur["temp"]) and len(cur["cache"]) > 0:
                    cur["temp"] = step_cache[cur["cache"].pop(0)]
                    cur["i"] = 0
                if cur["i"] < len(cur["temp"]):
                    if not hit:
                        hit = True
                        best_set, all_set = set(), set()
                        steps.append([best_set, all_set])
                        print(f"Adding step {len(steps):,}")
                    pt = cur["temp"][cur["i"]]
                    cur["i"] += 1
                    if cur["best"]:
                        best_set.add(pt)
                    all_set.add(pt)
            if not hit:
                break

        grid.save_frame()
        bad_route = set()
        good_route = set()
        for i, (step_best, step_bad) in enumerate(steps):
            print(f"Prep frame {i}:")
            if True: # i % 10 == 0 or i == len(found[0]) - 1:
                good_route |= step_best
                bad_route |= step_bad
                todo = step_bad

                for pt in bad_route:
                    grid[pt] = ("*" if pt in todo else None, (255, 0, 0) if pt in good_route else (128, 0, 0))

                grid.save_frame()
                for pt in bad_route:
                    grid[pt] = "."
            else:
                for trail_num, cur in enumerate(found):
                    if i < len(cur):
                        if trail_num == 0:
                            good_route.add(cur[i])
                        bad_route.add(cur[i])
        grid.draw_frames()

    return ret

def test(log):
    values = log.decode_values("""
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
    """)

    log.test(calc(log, values, 1), '94')
    log.test(calc(log, values, 2), '154')

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=60, final_secs=5)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

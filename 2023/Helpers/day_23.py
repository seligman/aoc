#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: A Long Walk'

from collections import defaultdict, deque

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    for x in grid.x_range():
        if grid[x, grid.height() - 1] == ".":
            final = (x, grid.height() - 1)
        if grid[x, 0] == ".":
            start = (x, 0)

    # Find all the points in the maze where a choice needs to be made
    to_check = deque([(start, (0, 1))])
    trails = defaultdict(list)
    while len(to_check) > 0:
        cur_cell, cur_dir = to_check.popleft()
        todo = deque([(cur_cell[0] + cur_dir[0], cur_cell[1] + cur_dir[1], 1)])
        seen = set([cur_cell])
        while len(todo) > 0:
            x, y, steps = todo.popleft()
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
                        if (x, y) not in trails:
                            to_check.append(((x, y), (ox, oy)))
                elif len(possible) == 1:
                    todo.append((possible[0][0] + x, possible[0][1] + y, steps + 1))
                else:
                    if (x, y, steps) not in trails[cur_cell]:
                        trails[cur_cell].append((x, y, steps))

    # Flatten all the points to a unique ID to remove any hashmap lookups
    to_id = {}
    for xy in trails:
        to_id[xy] = len(to_id)
    if final not in to_id:
        to_id[final] = len(to_id)
    start_id, final_id = to_id[start], to_id[final]
    trails_id = {}
    for xy, trail in trails.items():
        temp = []
        for x, y, steps in trail:
            temp.append((to_id[(x, y)], steps))
        trails_id[to_id[xy]] = temp
    trails_id = [trails_id[key] for key in sorted(trails_id)]

    seen = [False for _ in to_id]
    def dfs(cur_id, steps):
        if seen[cur_id]: return 0
        if cur_id == final_id: return steps
        seen[cur_id] = True
        ret = 0
        for other_id, to_add in trails_id[cur_id]:
            ret = max(ret, dfs(other_id, steps + to_add))
        seen[cur_id] = False
        return ret

    return dfs(start_id, 0)

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

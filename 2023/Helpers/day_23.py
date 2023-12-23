#!/usr/bin/env python3

DAY_NUM = 23
DAY_DESC = 'Day 23: A Long Walk'

from collections import deque

def calc(log, values, mode):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    for x in grid.x_range():
        if grid[x, grid.height() - 1] == ".":
            final = (x, grid.height() - 1)
        if grid[x, 0] == ".":
            start = (x, 0)

    if mode == 1:
        todo = [start + (set(),)]
        best = 0
        while len(todo) > 0:
            x, y, steps = todo.pop(0)
            if (x, y) == final:
                best = max(best, len(steps))
            for ox, oy, od in [(1, 0, ">"), (-1, 0, "<"), (0, -1, "^"), (0, 1, "v")]:
                if grid[x+ox, y+oy] != 0:
                    if grid[x+ox, y+oy] in {".", od}:
                        if (x+ox, y+oy) not in steps:
                            todo.append((x+ox, y+oy, steps | set([(x, y)])))
        return best

    V = set()
    R = grid.height() 
    C = grid.width() 
    for r in range(R):
        for c in range(C):
            nbr = 0
            for ch,dr,dc in [['^',-1,0],['v', 1,0],['<', 0,-1],['>',0,1]]:
                if (0<=r+dr<R and 0<=c+dc<C and grid[c+dc,r+dr]!='#'):
                    nbr += 1
            if nbr > 2 and grid[c, r] != '#':
                V.add((r, c))

    for c in range(C):
        if grid[c,0] == '.':
            V.add((0, c))
            start = (0, c)
        if grid[c, R-1] == '.':
            V.add((R-1, c))
            end = (R-1, c)

    E = {}
    for (rv, cv) in V:
        E[(rv, cv)] = []
        Q = deque([(rv, cv, 0)])
        SEEN = set()
        while Q:
            r, c, d = Q.popleft()
            if (r, c) in SEEN:
                continue
            SEEN.add((r, c))
            if (r, c) in V and (r, c) != (rv, cv):
                E[(rv, cv)].append(((r, c), d))
                continue
            for ch, dr, dc in [['^', -1, 0], ['v', 1, 0], ['<', 0, -1], ['>', 0, 1]]:
                if (0 <= r+dr < R and 0 <= c+dc < C and grid[c+dc, r+dr] != '#'):
                    Q.append((r+dr, c+dc, d+1))

    count = 0
    ans = 0
    SEEN = [[False for _ in range(C)] for _ in range(R)]
    seen = set()

    def dfs(v, d):
        nonlocal count
        nonlocal ans
        count += 1
        r, c = v
        if SEEN[r][c]:
            return
        SEEN[r][c] = True
        if r == R-1:
            ans = max(ans, d)
        for (y, yd) in E[v]:
            dfs(y, d+yd)
        SEEN[r][c] = False
    dfs(start, 0)

    return ans

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

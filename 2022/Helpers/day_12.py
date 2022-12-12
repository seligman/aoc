#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Hill Climbing Algorithm'

from collections import deque

def enum_start(values, mode, use_start=None):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    for x in grid.x_range():
        for y in grid.y_range():
            if grid[(x, y)] == "S":
                start = Point(x, y)
                grid[start] = 'a'

    if use_start is not None:
        yield use_start, grid
    else:
        yield start, grid

        if mode == 2:
            grid = Grid.from_text(values)
            grid[start] = 'a'
            for x in grid.x_range():
                for y in grid.y_range():
                    pt = Point(x, y)
                    if pt != start and grid[pt] == 'a':
                        yield Point(x, y), grid.copy()

def create_color_map():
    colors = [
        [0, 24, 168],
        [99, 0, 228],
        [220, 20, 60],
        [255, 117, 56],
        [238, 210, 20],
    ]
    map = {}
    for i in range(26):
        x = (i / 25) * (len(colors) - 1)
        if x == int(x):
            rgb = tuple(colors[int(x)])
        else:
            a = int(x)
            b = int(x+1)
            c = x - int(x)
            rgb = (
                int((1 - c) * colors[a][0] + c * colors[b][0]),
                int((1 - c) * colors[a][1] + c * colors[b][1]),
                int((1 - c) * colors[a][2] + c * colors[b][2]),
            )
        map[chr(ord('a') + i)] = rgb
    map["E"] = (255, 255, 255)
    map["*"] = (255, 255, 32)
    map["#"] = (128, 32, 32)
    return map

def calc(log, values, mode, draw=False, start_pt=False, use_start=None):
    best = None
    best_start = None

    will_use = set()
    for start, grid in enum_start(values, mode):
        will_use.add(start)

    for start, grid in enum_start(values, mode, use_start):
        visited = set([start])
        todo = deque([(start, [(list(visited), start)])])
        while len(todo) > 0:
            last_step, steps = todo.popleft()
            for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_step = last_step + d
                if next_step not in visited:
                    if next_step in grid:
                        if grid[next_step] == "E" and grid[last_step] == "z":
                            if best is None or len(steps) < best:
                                best = len(steps)
                                best_start = start
                                todo = []
                        else:
                            change = ord(grid[next_step]) - ord(grid[last_step])
                            if change <= 1 and grid[next_step] != "E" and next_step not in will_use:
                                use = True
                                visited.add(next_step)
                                if best is not None:
                                    if len(steps) >= best:
                                        use = False
                                if use:
                                    todo.append((next_step, steps + [(list(visited), next_step)]))

    if start_pt:
        return best_start

    if draw:
        for visited, pt in steps:
            grid[pt] = "*"
            for pt in visited:
                if grid[pt] != "*":
                    grid[pt] = "#"
            grid.save_frame()
        grid.draw_frames(color_map=create_color_map())

    return best

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    start = calc(DummyLog(), values, 2, start_pt=True)
    calc(DummyLog(), values, 2, draw=True, use_start=start)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def test(log):
    values = log.decode_values("""
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
    """)

    log.test(calc(log, values, 1), 31)
    log.test(calc(log, values, 2), 29)

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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

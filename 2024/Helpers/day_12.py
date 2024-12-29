#!/usr/bin/env python3

DAY_NUM = 12
DAY_DESC = 'Day 12: Garden Groups'

import random
from collections import deque

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    areas = []

    if draw:
        colors = []
        for _ in range(32):
            colors.append((random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))
        shadow = Grid.from_text(values, default=".")
        shadow.ensure_ratio(16/9)
        shadow.pad(2)
        for xy in grid.xy_range():
            shadow[xy] = [" ", colors[ord(grid[xy]) % len(colors)]]

    seen = set()
    for xy, key in grid.grid.items():
        if xy not in seen:
            seen.add(xy)
            cur = set([xy])
            areas.append(cur)
            todo = deque(cur)
            while len(todo) > 0:
                xy = todo.popleft()
                for oxy in grid.get_dirs(axis_count=2, diagonal=False, offset=xy):
                    if oxy not in seen and grid[oxy] == key:
                        seen.add(oxy)
                        todo.append(oxy)
                        cur.add(oxy)

    if draw:
        to_paint = {}
        for area in areas:
            border_count = 0
            border = set()

            for xy in area:
                for oxy in grid.get_dirs(axis_count=2, diagonal=True, offset=xy):
                    if oxy not in area:
                        border.add(oxy)
                        border_count += 1

            start = list(border)[0]
            path = [start]
            todo = deque(path)
            while len(todo) > 0:
                xy = todo.popleft()
                for oxy in grid.get_dirs(axis_count=2, diagonal=False, offset=xy):
                    if oxy in border and oxy not in path:
                        path.append(oxy)
                        todo.append(oxy)
                if len(todo) == 0 and len(border) - len(path) != 0:
                    path.append(list(border - set(path))[0])
                    todo.append(path[-1])
            temp = {
                "len": len(path), 
                "path": path, 
                "area": area, 
                "border_count": border_count,
            }
            if temp['len'] not in to_paint:
                to_paint[temp['len']] = []
            to_paint[temp['len']].append(temp)

        msg = ["Gardens: 0", "Score: 0"]
        shadow.save_frame(msg)

        gardens = 0
        cur_score = 0

        for i, cur in enumerate(sorted(to_paint, reverse=True)):
            batch = to_paint[cur]
            log(f"Working on #{i+1} of {len(to_paint)}, size of {batch[0]['len']}, with {len(batch)} areas")
            old = []
            for i in range(batch[0]['len']):
                for cur in batch:
                    xy = cur['path'][i]
                    if xy not in set(x[0] for x in old):
                        old.append([xy, shadow[xy]])
                        shadow[xy] = [" ", (255, 255, 255)]
                shadow.save_frame(msg)
            
            for cur in batch:
                gardens += 1
                cur_score += len(cur['area']) * cur['border_count']

            for xy, val in old:
                shadow[xy] = val
            for cur in batch:
                temp = None
                for xy in cur['area']:
                    if temp is None:
                        temp = shadow[xy][1]
                        temp = [" ", (int((temp[0] * 0.3 + 64 * 0.7)), int((temp[1] * 0.3 + 64 * 0.7)), int((temp[2] * 0.3 + 64 * 0.7)))]
                    shadow[xy] = temp
            msg = [f"Gardens: {gardens:,}", f"Score: {cur_score:,}"]
            shadow.save_frame(msg)
        
        shadow.ease_frames(15, 60)
        shadow.draw_frames(show_lines=False, text_xy=(40, 20), font_size=20)

    ret =  0
    for area in areas:
        if mode == 1:
            border_count = 0
            for xy in area:
                for oxy in grid.get_dirs(axis_count=2, diagonal=False, offset=xy):
                    if oxy not in area:
                        border_count += 1
            ret += len(area) * border_count
        else:
            border = set()
            for x, y in area:
                for ox, oy in grid.get_dirs(axis_count=2, diagonal=False):
                    if (x + ox, y + oy) not in area:
                        border.add((x * 3 + ox, y * 3 + oy))
            start = set()
            seen = set()
            for xy in border:
                if xy not in seen:
                    start.add(xy)
                    todo = deque([xy])
                    while len(todo):
                        x, y = todo.popleft()
                        seen.add((x, y))
                        for ox, oy in grid.get_dirs(axis_count=2, diagonal=False):
                            oxy = x + ox * 3, y + oy * 3
                            if oxy in border and oxy not in seen:
                                todo.append(oxy)
            ret += len(area) * len(start)
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
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

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

#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: RAM Run'

from collections import deque
from functools import cache
from multiprocessing import Pool

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, 1024, 70, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

_values = None
@cache
def get_steps(i, size, return_path=False):
    from grid import Grid, Point
    grid = Grid()
    for row in _values[:i]:
        row = row.split(",")
        grid[int(row[0]), int(row[1])] = "#"

    todo = deque([(Point(0,0), 0, [(0, 0)])])
    end = Point(size - 1, size - 1)
    seen = set()
    while len(todo) > 0:
        xy, steps, path = todo.popleft()
        if xy == end:
            if return_path:
                return path
            else:
                return steps
        for o in grid.get_dirs(2, diagonal=False):
            o = xy + Point(o)
            if o.x >= 0 and o.y >= 0 and o.x < size and o.y < size:
                if o not in seen:
                    seen.add(o)
                    if grid[o] != "#":
                        todo.append((o, steps + 1, path + [o.tuple]))
    return None

_size = None
def init_worker(values, size):
    global _values, _size
    _values = values
    _size = size

def worker(i):
    from grid import Grid, Point
    grid = Grid()
    for x in range(_size):
        for y in range(_size):
            grid[x, y] = "."
    for i in range(0, i + 1):
        grid[int(_values[i].split(",")[0]), int(_values[i].split(",")[1])] = "#"
    grid.ensure_ratio(16/9)
    grid.pad(4)

    for x in range(-1, _size + 1):
        grid[x, -1] = [" ", (128, 128, 128)]
        grid[x, _size] = [" ", (128, 128, 128)]
    for y in range(-1, _size + 1):
        grid[-1, y] = [" ", (128, 128, 128)]
        grid[_size, y] = [" ", (128, 128, 128)]

    path = get_steps(i, _size, return_path=True)
    if path is None:
        return i, grid, None
    else:
        for xy in path:
            grid[xy] = [" ", (128, 128, 255)]
        grid.save_frame()
        return i, grid.frames[0], path

def calc(log, values, mode, limit, size, draw=False):
    from grid import Grid, Point
    global _values
    _values = values
    size += 1

    if mode == 1:
        return get_steps(limit, size)
    else:
        target = (0, len(values) + 1, 1024)
        while True:
            start_at, stop_at = None, None
            for i in range(*target):
                if get_steps(i, size) is None:
                    stop_at = i
                    break
                else:
                    start_at = i

            if target[2] == 1:
                ret = start_at
                break
            elif start_at is not None and stop_at is not None:
                target = (start_at, stop_at + 1, target[2] // 2)
            else:
                target = (target[0], target[1], target[2] // 2)

    if draw:
        grid = Grid()
        grid[0, 0] = "."
        grid[size-1, size-1] = "."
        grid.ensure_ratio(16/9)
        grid.pad(4)
        with Pool(initializer=init_worker, initargs=(_values, size)) as pool:
            last_path = None
            for i, frame, path in pool.imap(worker, range(ret + 2)):
                if path is None:
                    for xy in last_path:
                        if frame[xy] == ".":
                            frame[xy] = [" ", (128, 128, 255)]
                        else:
                            break
                    frame.save_frame()
                    grid.frames.append(frame.frames[0])
                else:
                    last_path = path
                    grid.frames.append(frame)
                    if i % 150 == 0:
                        print(f"Got frame {i} of {ret + 2}")
            
        grid.ease_frames(rate=15, secs=30)
        grid.draw_frames()

    return values[ret]

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
    log(f"Part 1: {calc(log, values, 1, 1024, 70)}")
    log(f"Part 2: {calc(log, values, 2, 1024, 70)}")

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

#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Step Counter'

from collections import deque
from functools import cache

width, height, tiles = None, None, None

@cache
def find_depths(r,c):
    ret = {}
    todo = deque([(0,0,r,c,0)])
    while todo:
        tr,tc,r,c,d = todo.popleft()
        if r<0:
            tr -= 1
            r += height
        if r>=height:
            tr += 1
            r -= height
        if c<0:
            tc -= 1
            c += width
        if c>=width:
            tc += 1
            c -= width
        if not (0<=r<height and 0<=c<width and (c, r) not in tiles):
            continue
        if (tr,tc,r,c) in ret:
            continue
        if abs(tr)>4 or abs(tc)>4:
            continue
        ret[(tr,tc,r,c)] = d
        for dr,dc in [[-1,0],[0,1],[1,0],[0,-1]]:
            todo.append((tr,tc,r+dr, c+dc, d+1))
    return ret

@cache
def solve(d,v,L):
    amt = (L-d)//height
    ret = 0
    for x in range(1,amt+1):
        if d+height*x<=L and (d+height*x)%2==(L%2):
            ret += ((x+1) if v==2 else 1)
    return ret

def calc(log, values, mode, target_steps):
    from grid import Grid, Point
    grid = Grid.from_text(values)

    global tiles
    tiles = set()

    for xy, val in grid.grid.items():
        if val == "S":
            start = xy
        elif val == "#":
            tiles.add(xy)

    global width, height
    width = grid.width()
    height = grid.height()

    depths = find_depths(*start)
    offsets = []
    if mode == 1:
        offsets.append((0, 0))
    else:
        for tr in range(-3, 4):
            for tc in range(-3, 4):
                offsets.append((tr, tc))

    ans = 0
    for c in range(width):
        for r in range(height):
            if (0,0,r,c) in depths:
                for tr, tc in offsets:
                    d = depths[(tr,tc,r,c)]
                    if d%2==target_steps%2 and d<=target_steps:
                        ans += 1
                    if tr in {-3,3} and tc in {-3,3}:
                        ans += solve(d,2,target_steps)
                    elif tr in {-3,3} or tc in {-3,3}:
                        ans += solve(d,1,target_steps)

    return ans

def test(log):
    values = log.decode_values("""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """)

    log.test(calc(log, values, 1, 6), '16')
    log.test(calc(log, values, 2, 100), '6536')

def run(log, values):
    log(calc(log, values, 1, 64))
    log(calc(log, values, 2, 26501365))

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

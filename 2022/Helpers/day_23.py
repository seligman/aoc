#!/usr/bin/env python3

# Animation: https://youtu.be/s3xn8bOo6pA
#            https://youtu.be/yPZwSp3Te_M (Smoothed version)

from collections import defaultdict

DAY_NUM = 23
DAY_DESC = 'Day 23: Unstable Diffusion'

class Elf:
    __slots__ = ['at', 'move', 'can_move', 'moved']
    def __init__(self, at):
        self.at = at
        self.move = None
        self.can_move = False
        self.moved = False

def calc(log, values, mode, draw=False):
    elves = []

    from grid import Grid, Point
    if draw:
        grid = Grid()
        trail = {}

    for y, row in enumerate(values):
        for x, cell in enumerate(row):
            if cell == "#":
                elves.append(Elf(Point(x, y)))

    checks = [
        [( 0,-1), [( 0, -1), ( 1, -1), (-1, -1)]],
        [( 0, 1), [( 0,  1), ( 1,  1), (-1,  1)]],
        [(-1, 0), [(-1,  0), (-1,  1), (-1, -1)]],
        [( 1, 0), [( 1,  0), ( 1,  1), ( 1, -1)]],
    ]
    dirs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for check in checks:
        for i in range(len(check[1])):
            check[1][i] = dirs.index(check[1][i])

    round = 1
    positions = set(x.at.tuple for x in elves)
    while True:
        wants_to_move_to = defaultdict(int)

        for elf in elves:
            elf.moved = False
            elf.move = None

            has_elf = [((elf.at + pt).tuple in positions) for pt in dirs]
            if any(has_elf):
                for target, check in checks:
                    if not any(has_elf[i] for i in check):
                        elf.move = (elf.at + target)
                        wants_to_move_to[elf.move.tuple] += 1
                        break

        any_moved = 0
        for elf in elves:
            if elf.move is not None:
                if wants_to_move_to[elf.move.tuple] == 1:
                    positions.remove(elf.at.tuple)
                    positions.add(elf.move.tuple)
                    elf.at = elf.move
                    elf.moved = True
                    any_moved += 1
        
        checks.append(checks.pop(0))
        if mode == 1:
            if round == 10:
                min_x = min(x.at.x for x in elves)
                min_y = min(x.at.y for x in elves)
                max_x = max(x.at.x for x in elves) + 1
                max_y = max(x.at.y for x in elves) + 1
                return ((max_x - min_x) * (max_y - min_y)) - len(elves)
        else:
            if draw:
                active = set(x.at.tuple for x in elves)
                for key in trail:
                    trail[key] = max(10 if key in active else 0, trail[key] - 1)
                for elf in elves:
                    if trail.get(elf.at.tuple, 0) < 10:
                        trail[elf.at.tuple] = 12
                
                for key, value in trail.items():
                    rgb = {12: 128, 11: 192, 10: 255}.get(value, int((value / 10) * 192))
                    grid[key] = [None, (rgb, rgb, rgb)]
                grid.save_frame()
            if any_moved == 0:
                if draw:
                    while True:
                        found = False
                        for key in trail:
                            if trail[key] != 10 and trail[key] > 0:
                                trail[key] = max(0, trail[key] - 1)
                                found = True
                        if not found:
                            break
                        for key, value in trail.items():
                            rgb = {12: 128, 11: 192, 10: 255}.get(value, int((value / 10) * 192))
                            grid[key] = [None, (rgb, rgb, rgb)]
                        grid.save_frame()

                    grid.draw_frames()
                return round
        round += 1

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def test(log):
    values = log.decode_values("""
        ....#..
        ..###.#
        #...#.#
        .#...##
        #.###..
        ##.#.##
        .#..#..
    """)

    log.test(calc(log, values, 1), '110')
    log.test(calc(log, values, 2), '20')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

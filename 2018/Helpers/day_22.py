#!/usr/bin/env python3

import heapq

DAY_NUM = 22
DAY_DESC = 'Day 22: Mode Maze'


class Infinity:
    def __init__(self, default="#"):
        self.default = default
        self.grid = [[default] * 800 for _ in range(800)]
        self.x = 0
        self.y = 0

    def get(self, x, y):
        x += self.x
        y += self.y
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            return self.default
        else:
            return self.grid[y][x]

    def set(self, x, y, value):
        x += self.x
        y += self.y
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            while x < 0:
                for i in range(len(self.grid)):
                    self.grid[i] = [self.default] + self.grid[i]
                x += 1
                self.x += 1
            while y < 0:
                self.grid.insert(0, [self.default] * len(self.grid[0]))
                y += 1
                self.y += 1
            while x >= len(self.grid[0]):
                for i in range(len(self.grid)):
                    self.grid[i].append(self.default)
            while y >= len(self.grid):
                self.grid.append([self.default] * len(self.grid[0]))

        self.grid[y][x] = value

    def show(self, log):
        for row in self.get_rows():
            log(row)

    def get_rows(self):
        ret = []
        ret.append(self.default * (len(self.grid[0]) + 2))
        for row in self.grid:
            ret.append(self.default + "".join(row) + self.default)
        ret.append(self.default * (len(self.grid[0]) + 2))
        return ret

    def erosion(self, x, y, depth):
        ret = self.get(x, y)
        if ret is not None:
            return ret

        geo = None
        if y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = self.erosion(x-1, y, depth) * self.erosion(x, y-1, depth)

        ret = (geo + depth) % 20183
        self.set(x, y, ret)

        return ret

    def risk(self, x, y, depth):
        return self.erosion(x, y, depth) % 3


def calc(log, depth, target_x, target_y):
    grid = Infinity(None)
    grid.set(0, 0, 0)
    grid.set(target_x, target_y, 0)

    total_risk = sum([grid.risk(x, y, depth) for x in range(target_x + 1) for y in range(target_y + 1)])
    log("Risk: " + str(total_risk))

    todo = [(0, 0, 0, 1)]
    # todo.append((0, 0, 0, 1))
    best = {}
    target = (target_x, target_y, 1)

    while len(todo) > 0:
        time, x, y, invalid = heapq.heappop(todo)
        best_key = (x, y, invalid)

        if best_key in best and best[best_key] <= time:
            continue

        best[best_key] = time
        if best_key == target:
            log("Best minutes: " + str(time))
            break

        for i in range(3):
            if i != invalid and i != grid.risk(x, y, depth):
                todo.append((time + 7, x, y, i))

        for off_x, off_y in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            new_x, new_y = off_x + x, off_y + y
            if new_x >= 0 and new_y >= 0:
                if grid.risk(new_x, new_y, depth) != invalid:
                    todo.append((time + 1, new_x, new_y, invalid))

    return total_risk


def test(log):
    if calc(log, 510, 10, 10) == 114:
        return True
    else:
        return False


def run(log, values):
    depth = int(values[0].split(' ')[1])
    x, y = int(values[1].split(' ')[1].split(",")[0]), int(values[1].split(' ')[1].split(",")[1])
    log(calc(log, depth, x, y))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

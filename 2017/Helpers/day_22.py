#!/usr/bin/env python3

DAY_NUM = 22
DAY_DESC = 'Day 22: Sporifica Virus'

class Infinity:
    def __init__(self, default="."):
        self.default = default
        self.grid = [[default]]
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
        for row in self.grid:
            ret.append("".join(row))
        return ret

def calc(log, values, iters, mode):
    grid = Infinity()
    ox = (len(values[0]) - 1) // 2
    oy = (len(values) - 1) // 2

    for y in range(len(values)):
        for x in range(len(values[0])):
            grid.set(x-ox, y-oy, values[y][x])

    x, y = 0, 0
    dx, dy = 0, -1

    new_dirs = {
        (0, -1): {".": (-1, 0), "#": (1, 0), "w": (0, -1), "f": (0, 1)},
        (-1, 0): {".": (0, 1), "#": (0, -1), "w": (-1, 0), "f": (1, 0)},
        (0, 1): {".": (1, 0), "#": (-1, 0), "w": (0, 1), "f": (0, -1)},
        (1, 0): {".": (0, -1), "#": (0, 1), "w": (1, 0), "f": (-1, 0)},
    }

    ret = 0
    if mode == 0:
        states = {"#": ".", ".": "#"}
    else:
        states = {".": "w", "w": "#", "#": "f", "f": "."}
    while iters > 0:
        iters -= 1
        cur = grid.get(x, y)
        dx, dy = new_dirs[(dx, dy)][cur]
        new_state = states[cur]
        if new_state == "#":
            ret += 1
        grid.set(x, y, new_state)
        x, y = x + dx, y + dy

    return ret

def test(log):
    values = [
        "..#",
        "#..",
        "...",
    ]

    if calc(log, values, 10000, 0) == 5587:
        log("Pass 1 worked")
        if calc(log, values, 10000000, 1) == 2511944:
            log("Pass 2 worked")
            return True
        else:
            return False
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 10000, 0),))
    log("Part 2: %d" % (calc(log, values, 10000000, 1),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2017/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

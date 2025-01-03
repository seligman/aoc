#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Fractal Art'

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

def enum_layout(grid, x, y, skip):
    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+ox, y+oy)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+(skip-1)-ox, y+oy)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+ox, y+(skip-1)-oy)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+(skip-1)-ox, y+(skip-1)-oy)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+oy, y+ox)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+oy, y+(skip-1)-ox)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+(skip-1)-oy, y+ox)
    yield ret[1:]

    ret = ""
    for oy in range(skip):
        ret += "/"
        for ox in range(skip):
            ret += grid.get(x+(skip-1)-oy, y+(skip-1)-ox)
    yield ret[1:]

def calc(log, values, iters):
    values = [x.split(" => ") for x in values]
    mapping = {}

    for a, b in values:
        mapping[a] = b

    grid = Infinity()
    grid.set(1, 0, "#")
    grid.set(2, 1, "#")
    grid.set(0, 2, "#")
    grid.set(1, 2, "#")
    grid.set(2, 2, "#")

    for cur_iter in range(iters):
        new_grid = Infinity()
        skip = 2 if len(grid.grid) % 2 == 0 else 3
        for x in range(0, len(grid.grid), skip):
            for y in range(0, len(grid.grid), skip):
                found = False
                for layout in enum_layout(grid, x, y, skip):
                    if layout in mapping:
                        found = True
                        temp = mapping[layout].split("/")
                        for oy in range(len(temp)):
                            for ox in range(len(temp[0])):
                                new_grid.set((x//skip)*len(temp)+ox, (y//skip)*len(temp)+oy, temp[oy][ox:ox+1])
                        break
                if not found:
                    for layout in enum_layout(grid, x, y, skip):
                        log("Couldn't find %d: %s" % (cur_iter, layout,))
        grid = new_grid

    ret = 0
    for row in grid.grid:
        for cell in row:
            if cell == "#":
                ret += 1

    return ret

def test(log):
    values = [
        "../.# => ##./#../...",
        ".#./..#/### => #..#/..../..../#..#",
    ]

    if calc(log, values, 2) == 12:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 5),))
    log("Part 2: %d" % (calc(log, values, 18),))

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

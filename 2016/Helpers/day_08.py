#!/usr/bin/env python3

import re

DAY_NUM = 8
DAY_DESC = 'Day 8: Two-Factor Authentication'

def calc(log, values, width, height, show):
    grid = [["."] * width for _ in range(height)]
    for cur in values:
        m = re.search("rect ([0-9]+)x([0-9]+)", cur)
        if m:
            for x in range(int(m.group(1))):
                for y in range(int(m.group(2))):
                    grid[y][x] = "#"

        m = re.search("rotate column x=([0-9]+) by ([0-9]+)", cur)
        if m:
            shift = int(m.group(2))
            x = int(m.group(1))
            vals = [grid[y][x] for y in range(height)]
            for y in range(height):
                grid[(y + shift) % height][x] = vals[y]

        m = re.search("rotate row y=([0-9]+) by ([0-9]+)", cur)
        if m:
            shift = int(m.group(2))
            y = int(m.group(1))
            vals = [grid[y][x] for x in range(width)]
            for x in range(width):
                grid[y][(x + shift) % width] = vals[x]

    ret = 0

    for row in grid:
        for cell in row:
            if cell == "#":
                ret += 1

    if show:
        for row in grid:
            log("".join(row))
        if len(grid[0]) > 10:
            from hashlib import sha256
            import json
            chars = {
                "638609db86": ("U", "#..#.\n#..#.\n#..#.\n#..#.\n#..#.\n.##..\n"),
                "ef1ef34499": ("P", "###..\n#..#.\n#..#.\n###..\n#....\n#....\n"),
                "b2761e8e9c": ("O", ".##..\n#..#.\n#..#.\n#..#.\n#..#.\n.##..\n"),
                "857c29d234": ("J", "..##.\n...#.\n...#.\n...#.\n#..#.\n.##..\n"),
                "2c9b34b8e7": ("F", "####.\n#....\n###..\n#....\n#....\n#....\n"),
                "f9bec04ba8": ("B", "###..\n#..#.\n###..\n#..#.\n#..#.\n###..\n"),
                "4ac981b6ad": ("C", ".##..\n#..#.\n#....\n#....\n#..#.\n.##..\n"),
                "73f1d147de": ("E", "####.\n#....\n###..\n#....\n#....\n####.\n"),
                "ea1ff1ce86": ("Z", "####.\n...#.\n..#..\n.#...\n#....\n####.\n"),
                "a596a3c4db": ("L", "#....\n#....\n#....\n#....\n#....\n####.\n"),
            }
            decoded = ""
            problems = 0
            for off in range(0, len(grid[0]), 5):
                temp = ""
                for y in range(len(grid)):
                    for x in range(off, off + 5):
                        temp += grid[y][x]
                    temp += "\n"
                code = sha256(temp.encode("utf-8")).hexdigest()[:10]
                if code not in chars:
                    print("ERROR: Unknown code:")
                    print(temp)
                    print('                "%s": ("NEEDED", %s),' % (code, json.dumps(temp)))
                    problems += 1
                    chars[code] = [".", ""]
                decoded += chars[code][0]
            if problems > 0:
                exit(1)
            log("Part 2: %s" % (decoded,))
    return ret

def test(log):
    values = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1",
    ]

    if calc(log, values, 7, 3, True) == 6:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 50, 6, True),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2016/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

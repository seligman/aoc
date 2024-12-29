#!/usr/bin/env python3

import re

DAY_NUM = 10
DAY_DESC = 'Day 10: The Stars Align'

class Point:
    def __init__(self, values):
        self.x = int(values[0])
        self.y = int(values[1])
        self.vel_x = int(values[2])
        self.vel_y = int(values[3])

    def tick(self):
        self.x += self.vel_x
        self.y += self.vel_y

def decode(value, log):
    from hashlib import sha256
    import json
    digits = {
        "f8d34ce88d": ("A", "........\n...##...\n..#..#..\n.#....#.\n.#....#.\n.#....#.\n.######.\n.#....#.\n.#....#.\n.#....#.\n.#....#.\n........\n"),
        "1f4862a54d": ("B", "........\n.#####..\n.#....#.\n.#....#.\n.#....#.\n.#####..\n.#....#.\n.#....#.\n.#....#.\n.#....#.\n.#####..\n........\n"),
        "2fdd4ff722": ("C", "........\n..####..\n.#....#.\n.#......\n.#......\n.#......\n.#......\n.#......\n.#......\n.#....#.\n..####..\n........\n"),
        "3c1678c8af": ("F", "........\n.######.\n.#......\n.#......\n.#......\n.#####..\n.#......\n.#......\n.#......\n.#......\n.#......\n........\n"),
        "9fac395c92": ("G", "........\n..####..\n.#....#.\n.#......\n.#......\n.#......\n.#..###.\n.#....#.\n.#....#.\n.#...##.\n..###.#.\n........\n"),
        "a00a2cd54c": ("H", "........\n.#....#.\n.#....#.\n.#....#.\n.#....#.\n.######.\n.#....#.\n.#....#.\n.#....#.\n.#....#.\n.#....#.\n........\n"),
        "0bbaf43040": ("K", "........\n.#....#.\n.#...#..\n.#..#...\n.#.#....\n.##.....\n.##.....\n.#.#....\n.#..#...\n.#...#..\n.#....#.\n........\n"),
        "f9ecff4196": ("L", "........\n.#......\n.#......\n.#......\n.#......\n.#......\n.#......\n.#......\n.#......\n.#......\n.######.\n........\n"),
        "efbd2adb35": ("N", "........\n.#....#.\n.##...#.\n.##...#.\n.#.#..#.\n.#.#..#.\n.#..#.#.\n.#..#.#.\n.#...##.\n.#...##.\n.#....#.\n........\n"),
        "c20dd6bb7f": ("P", "........\n.#####..\n.#....#.\n.#....#.\n.#....#.\n.#####..\n.#......\n.#......\n.#......\n.#......\n.#......\n........\n"),
        "d1bc303382": ("R", "........\n.#####..\n.#....#.\n.#....#.\n.#....#.\n.#####..\n.#..#...\n.#...#..\n.#...#..\n.#....#.\n.#....#.\n........\n"),
        "bc99d5d8b7": ("Z", "........\n.######.\n......#.\n......#.\n.....#..\n....#...\n...#....\n..#.....\n.#......\n.#......\n.######.\n........\n"),
    }
    value = value.split("\n")
    ret = ""
    for off in range(len(value[0])//8):
        dig = ""
        for y in range(len(value)):
            for x in range(off * 8, off * 8 + 8):
                dig += value[y][x]
            dig += "\n"
        code = sha256(dig.encode("utf-8")).hexdigest()[:10]
        if code in digits:
            ret += digits[code][0]
        else:
            log("ERROR!!")
            log('        "' + code + '": ("NEEDED", ' + json.dumps(dig) + '),')
            log(dig)
    return ret

def calc(log, values, test_mode):
    r = re.compile("position=< *([-0-9]+), *([-0-9]+)> velocity=< *([-0-9]+), *([-0-9]+)>")
    pts = []
    for cur in values:
        m = r.search(cur)
        if m:
            pts.append(Point(m.groups()))

    best_size = None
    best_output = None
    best_seconds = 0
    seconds = 0

    while True:
        width = max([x.x for x in pts]) + 1
        height = max([x.y for x in pts]) + 1
        min_x = min([x.x for x in pts])
        min_y = min([x.y for x in pts])

        test_width = width - min_x
        test_height = height - min_y

        if test_width < 100 and test_height < 100 and min_x >= 0 and min_y >= 0:
            output = [["."] * ((width - min_x) + 2) for x in range((height - min_y) + 2)]
            for pt in pts:
                output[pt.y+1-min_y][pt.x+1-min_x] = "#"
            output = "\n".join(["".join(x) for x in output])

            size = test_width * test_height

            if best_size is None or size < best_size:
                best_output = output
                best_size = size
                best_seconds = seconds
                if test_mode:
                    log(best_output)
                    log(best_seconds)
                    break
            else:
                log(best_output)
                log("Part 1: " + decode(best_output, log))
                log("Part 2: " + str(best_seconds))
                break

        for pt in pts:
            pt.tick()
        seconds += 1

    return 0

def test(log):
    values = [
        "position=< 9,  1> velocity=< 0,  2>",
        "position=< 7,  0> velocity=<-1,  0>",
        "position=< 3, -2> velocity=<-1,  1>",
        "position=< 6, 10> velocity=<-2, -1>",
        "position=< 2, -4> velocity=< 2,  2>",
        "position=<-6, 10> velocity=< 2, -2>",
        "position=< 1,  8> velocity=< 1, -1>",
        "position=< 1,  7> velocity=< 1,  0>",
        "position=<-3, 11> velocity=< 1, -2>",
        "position=< 7,  6> velocity=<-1, -1>",
        "position=<-2,  3> velocity=< 1,  0>",
        "position=<-4,  3> velocity=< 2,  0>",
        "position=<10, -3> velocity=<-1,  1>",
        "position=< 5, 11> velocity=< 1, -2>",
        "position=< 4,  7> velocity=< 0, -1>",
        "position=< 8, -2> velocity=< 0,  1>",
        "position=<15,  0> velocity=<-2,  0>",
        "position=< 1,  6> velocity=< 1,  0>",
        "position=< 8,  9> velocity=< 0, -1>",
        "position=< 3,  3> velocity=<-1,  1>",
        "position=< 0,  5> velocity=< 0, -1>",
        "position=<-2,  2> velocity=< 2,  0>",
        "position=< 5, -2> velocity=< 1,  2>",
        "position=< 1,  4> velocity=< 2,  1>",
        "position=<-2,  7> velocity=< 2, -2>",
        "position=< 3,  6> velocity=<-1, -1>",
        "position=< 5,  0> velocity=< 1,  0>",
        "position=<-6,  0> velocity=< 2,  0>",
        "position=< 5,  9> velocity=< 1, -2>",
        "position=<14,  7> velocity=<-2,  0>",
        "position=<-3,  6> velocity=< 2, -1>",
    ]

    calc(log, values, True)
    return True


def run(log, values):
    log(calc(log, values, False))

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

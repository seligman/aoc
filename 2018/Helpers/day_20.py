#!/usr/bin/env python3

from collections import deque
import os

DAY_NUM = 20
DAY_DESC = 'Day 20: A Regular Map'

class Infinity:
    def __init__(self, default="#"):
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
        ret.append(self.default * (len(self.grid[0]) + 2))
        for row in self.grid:
            ret.append(self.default + "".join(row) + self.default)
        ret.append(self.default * (len(self.grid[0]) + 2))
        return ret

def decode(value, i, x, y, level, grid):
    i[0] += 1
    stack_x, stack_y = x, y
    while True:
        if value[i[0]] in "NEWS":
            if value[i[0]] == "N":
                y -= 1
                grid.set(x, y, "-")
                y -= 1
            if value[i[0]] == "S":
                y += 1
                grid.set(x, y, "-")
                y += 1
            if value[i[0]] == "W":
                x -= 1
                grid.set(x, y, "|")
                x -= 1
            if value[i[0]] == "E":
                x += 1
                grid.set(x, y, "|")
                x += 1
            grid.set(x, y, ".")

            i[0] += 1
        elif value[i[0]] in {")", "$"}:
            i[0] += 1
            break
        elif value[i[0]] == "|":
            x, y = stack_x, stack_y
            i[0] += 1
        else:
            decode(value, i, x, y, level + 1, grid)

def calc(log, values, show, frame_rate, track_long=None, highlight=None):
    grid = Infinity()
    decode(values[0], [0], 0, 0, 0, grid)

    floods = deque()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    locs = {}

    floods.append(None)
    floods.append([0, 0, 0, [(0, 0)]])
    grid.set(0, 0, "s")

    if show:
        log("  Before:")
        grid.show(log)

    total_frames = 0
    file_number = 0

    if frame_rate > 0:
        if not os.path.isdir("floods"):
            os.mkdir("floods")
    while len(floods) > 0:
        cur = floods.popleft()
        if cur is None:
            if len(floods) > 0:
                floods.append(None)
            if frame_rate > 0:
                if total_frames % frame_rate == 0:
                    while os.path.isfile(os.path.join("floods", "flood_%05d.txt" % (file_number,))):
                        file_number += 1
                    print("Writing 'flood_%05d.txt'..." % (file_number,))
                    with open(os.path.join("floods", "flood_%05d.txt" % (file_number,)), "w") as f:
                        for row in grid.get_rows():
                            f.write(row + "\n")
            total_frames += 1
        else:
            old_char = grid.get(cur[0], cur[1])
            if old_char in {".", "|", "-", "s"}:
                if highlight is not None and (cur[0], cur[1]) in highlight:
                    grid.set(cur[0], cur[1], "X")
                else:
                    grid.set(cur[0], cur[1], "x")
                if old_char in {"|", "-"}:
                    old_char = 1
                else:
                    if (cur[0], cur[1]) in locs:
                        raise Exception()
                    locs[(cur[0], cur[1])] = (cur[2], cur[3])
                    old_char = 0

                for x, y in dirs:
                    if track_long is None:
                        floods.append([x + cur[0], y + cur[1], cur[2] + old_char, []])
                    else:
                        floods.append([x + cur[0], y + cur[1], cur[2] + old_char, cur[3] + [(x + cur[0], y + cur[1])]])

    if show:
        log("  After:")
        grid.show(log)

    if track_long is not None:
        for value in locs.values():
            if track_long[0] is None or len(value[1]) > len(track_long[0]):
                track_long[0] = value[1]

    log("Shortest long distance: " + str(max([x[0] for x in locs.values()])))
    log("Part 2: " + str(sum([1 if x[0] >= 1000 else 0 for x in locs.values()])))
    log("Total Frames: " + str(total_frames))

    return max([x[0] for x in locs.values()])

def other_ffmpeg(describe, values):
    if describe:
        return "Generate final GIF"

    import subprocess

    src = os.path.join("floods", "flood_%05d.png")
    dest = os.path.join("floods", "final.gif")

    cmd = ["ffmpeg", "-y", "-framerate", "30", "-i", src, dest]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)

def other_animate_frames(describe, values):
    if describe:
        return "Animate all frames from dump_frames"

    from PIL import Image, ImageDraw, ImageFont # optional package
    from collections import deque
    import os

    file_number = -1
    out_file = -1
    last = None
    older = deque()
    colors = [
        (128, 128, 128, 255),
        (147, 147, 147, 255),
        (166, 166, 166, 255),
        (185, 185, 185, 255),
        (204, 204, 204, 255),
    ]

    first_file = None

    for _ in range(10000):
        if file_number == -1:
            file_number = 0
        else:
            file_number += 5
        filename = os.path.join("floods", "flood_%05d.txt" % (file_number,))

        if not os.path.isfile(filename):
            break
        else:
            with open(filename) as f:
                rows = [x.strip().replace(".", " ") for x in f]
            rows = "\n".join(rows)

            fnt = ImageFont.truetype(os.path.join("Puzzles", "SourceCodePro.ttf"), 5)
            if first_file is None:
                txt = Image.new('RGBA', (620, 825), (0,0,0,255))
                d = ImageDraw.Draw(txt)
            else:
                txt = Image.open(first_file)
                d = ImageDraw.Draw(txt)


            if first_file is None:
                y = 10
                for row in rows.split("\n"):
                    d.text((10, y), row, fill=(64, 64, 64, 255), font=fnt)

                    bg = "".join([x if x in {"#"} else " " for x in row])
                    d.text((10, y), bg, fill=(32, 32, 128, 255), font=fnt)
                    y += 4
            else:
                y = 10
                empty = None
                for row in rows.split("\n"):
                    if empty is None:
                        empty = " " * len(row)

                    fg = "".join(["*" if x in {"X"} else " " for x in row])
                    if fg != empty:
                        d.text((10, y), fg, fill=(255, 224, 224, 255), font=fnt)

                    fg = "".join(["x" if x in {"x"} else " " for x in row])
                    if fg != empty:
                        d.text((10, y), fg, fill=(255, 128, 128, 128), font=fnt)

                    y += 4

            if last is None:
                last = rows
                temp = ""
                for cur in last:
                    if cur == "\n":
                        temp += cur
                    else:
                        temp += " "
                for _ in range(len(colors)):
                    older.append(temp)
            else:
                temp = ""
                for i in range(len(rows)):
                    if rows[i] == "\n":
                        temp += "\n"
                    else:
                        if rows[i] == last[i]:  # pylint: disable=e1136
                            temp += " "
                        else:
                            temp += rows[i]
                older.append(temp)
                older.popleft()
                i = 0
                empty = None
                for cur in older:
                    y = 10
                    for row in cur.split("\n"):
                        if empty is None:
                            empty = " " * len(row)
                        if row != empty:
                            d.text((10, y), row, fill=colors[i], font=fnt)
                        fg = "".join(["*" if x in {"X"} else " " for x in row])
                        if fg != empty:
                            d.text((10, y), fg, fill=(255, 224, 224, 255), font=fnt)
                        y += 4
                    i += 1
                last = rows

            out_file += 1
            txt.save(os.path.join("floods", "flood_%05d.png" % (out_file,)))
            if first_file is None:
                first_file = os.path.join("floods", "flood_%05d.png" % (out_file,))
            print("Done with 'flood_%05d.png'" % (out_file,))

def test(log):
    values = [
        "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$",
    ]

    if calc(log, values, True, 0) == 18:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, False, 0),))

class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)


def other_dump_frames(describe, values):
    if describe:
        return "Dump out frame information"
    print("Getting longest run")
    long_run = [None]
    calc(DummyLog(), values, False, 0, track_long=long_run)
    highlight = set()
    for cur in long_run[0]: # pylint: disable=e1133
        highlight.add(cur)
    print(calc(DummyLog(), values, False, 4, highlight=highlight))
    

def other_show(describe, values):
    if describe:
        return "Show the final map"

    grid = Infinity()
    decode(values[0], [0], 0, 0, 0, grid)
    grid.set(0, 0, "s")
    grid.show(DummyLog(), )

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

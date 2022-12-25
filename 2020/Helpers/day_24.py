#!/usr/bin/env python3

import re

DAY_NUM = 24
DAY_DESC = 'Day 24: Lobby Layout'

def calc(log, values, mode, draw={"mode": 0}):
    from grid import Grid
    grid = Grid(".")

    def draw_grid(value, image_copies=1):
        log(f"Saving frame {grid.frame} for {value}")
        color_map = {
            "#": (0, 0, 0),
            "#t": (32, 32, 192),
            ".": (192, 192, 192),
            ".t": (160, 160, 255),
        }
        grid.draw_grid_hex(
            size=draw['size'], 
            color_map=color_map, 
            background_color=(128, 128, 128), 
            image_copies=image_copies,
            outline=(64,64,64),
            hex_size=15,
            show_all=draw["type"] in {"coin", "ca", "ca2", "ca3"},
            scale=0.5,
        )

    r = re.compile("(?P<dir>e|se|sw|w|nw|ne)")
    for row in values:
        x, y = 0, 0
        grid[x, y] = grid[x, y]
        trail = set([(x, y)])
        for m in r.finditer(row):
            x, y = Grid.cardinal_hex(m.group('dir'), x, y)
            if draw["mode"] == "draw":
                grid[x, y] = grid[x, y]
                trail.add((x, y))
        grid[x, y] = "#" if grid[x, y] == "." else "."
        if draw["mode"] == "draw" and draw["type"] not in {"ca", "ca2", "ca3"}:
            for x, y in trail:
                grid[x, y] += "t"
            draw_grid("flipping")
            for x, y in trail:
                grid[x, y] = grid[x, y][0]

    if mode == 1:
        return len([x for x in grid.grid.values() if x == "#"])

    for _ in range(100 if draw.get("type", "normal") == "normal" else 500):
        todo = []
        for y in grid.y_range(pad=1):
            for x in grid.x_range_hex(y, pad=2):
                black = 0
                for xo, yo in grid.get_dirs_hex():
                    if grid[x + xo, y + yo] == "#":
                        black += 1
                if grid[x, y] == "#" and (black == 0 or black > 2):
                    todo.append((x, y, "."))
                if grid[x, y] == "." and black == 2:
                    todo.append((x, y, "#"))

        for x, y, val in todo:
            grid[x, y] = val

        if draw["mode"] == "draw":
            use = True
            if draw["type"] == "ca2":
                draw["skip"] += 1
                use = draw["skip"] % 2 == 1
            elif draw["type"] == "ca3":
                draw["skip"] += 1
                use = draw["skip"] % 3 == 1
            if use:
                draw_grid("life")

    if draw["mode"] == "size":
        return grid.get_grid_hex_size()

    if draw["mode"] == "draw":
        draw_grid("final", image_copies=29)

    return len([x for x in grid.grid.values() if x == "#"])

def powerset(iterable):
    from itertools import chain, combinations
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def other_layout(describe, values):
    if describe:
        return "Layout a floor"

    states = [
        [
            "   #   ",
            "#     #",
            "       ",
            "#     #",
            "   #   ",
        ],
        [
            "  #   #  ",
            "   # #   ",
            "# #   # #",
            "   # #   ",
            "  #   #  ",
        ],
        [
            "  #   #  ",
            "         ",
            "#       #",
            "         ",
            "  #   #  ",
        ],
        [
            "     ",
            "   # ",
            "# #  ",
            " # # ",
            "#    ",
        ],
        [
            "     ",
            "   # ",
            "#    ",
            "   # ",
            "#    ",
        ],
        [
            "      ",
            "  #   ",
            "     #",
            "#     ",
            "   #  ",
        ],
    ]

    from grid import Grid
    import random
    output = []
    blot = Grid()

    for _ in range(5000):
        dest_x = random.randint(-50, 50)
        dest_y = random.randint(-25, 25)
        use = True
        if dest_y % 2 == 1:
            if dest_x % 2 != 1:
                use = False
        else:
            if dest_x % 2 != 0:
                use = False
        
        if use:
            for x in range(-7, 7):
                for y in range(-4, 4):
                    if blot[x + dest_x, y + dest_y] == "X":
                        use = False
        
        if use:
            for x in range(-5, 6):
                for y in range(-3, 4):
                    blot[x + dest_x, y + dest_y] = "X"

            choice = random.randint(0, len(states)-1)
            grid = Grid(".")
            off_x = len(states[choice][0]) // 2
            off_y = len(states[choice]) // 2
            for y in range(len(states[choice])):
                for x in range(len(states[choice][y])):
                    if states[choice][y][x] == "#":
                        grid[x - off_x, y - off_y] = "#"

            for y in grid.y_range():
                for x in grid.x_range_hex(y):
                    if grid[x, y] == "#":
                        xo = x + dest_x
                        yo = y + dest_y

                        steps = []
                        steps.append([0, 0, ""])
                        seen = set()
                        while True:
                            temp_x, temp_y, temp_step = steps.pop(0)
                            if (temp_x, temp_y) == (xo, yo):
                                output.append(temp_step)
                                break
                            dirs = ["e", "w", "ne", "nw", "se", "sw"]
                            random.shuffle(dirs)
                            for test in dirs:
                                test_x, test_y = Grid.cardinal_hex(test, temp_x, temp_y)
                                if (test_x, test_y) not in seen:
                                    seen.add((test_x, test_y))
                                    steps.append((test_x, test_y, temp_step + test))

    random.shuffle(output)
    for cur in output:
        print(cur)


def other_find(describe, values):
    if describe:
        return "Find a runner"

    from grid import Grid
    from dummylog import DummyLog

    seen = set()
    bits = [(0, 0)]
    seen.add((0, 0))
    for _ in range(3):
        for x, y in list(bits):
            for xo, yo in Grid.get_dirs_hex():
                if (x + xo, y + yo) not in seen:
                    seen.add((x + xo, y + yo))
                    bits.append((x + xo, y + yo))

    seen = set()

    class Keeper:
        def __init__(self):
            self.values = []
        def __call__(self, value):
            self.values.append(value)

    for start in powerset(bits):
        if len(start) > 0:
            keep = Keeper()
            keep("=" * 100)
            grid = Grid(".")
            for x, y in start:
                grid[x, y] = "#"

            counts = {}
            offs = {}
            for i in range(30):
                todo = []
                for y in grid.y_range(pad=1):
                    for x in grid.x_range_hex(y, pad=2):
                        black = 0
                        for xo, yo in grid.get_dirs_hex():
                            if grid[x + xo, y + yo] == "#":
                                black += 1
                        if grid[x, y] == "#" and (black == 0 or black > 2):
                            todo.append((x, y, "."))
                        if grid[x, y] == "." and black == 2:
                            todo.append((x, y, "#"))

                for x, y, val in todo:
                    grid[x, y] = val
                
                for x, y in list(grid.grid):
                    if grid[x, y] == ".":
                        del grid[x, y]
                
                if len(grid.grid) == 0:
                    break

                key = grid.dump_grid_hex()
                if key in seen:
                    break
                if key not in counts:
                    counts[key] = []
                if key not in offs:
                    offs[key] = (grid.axis_min(0), grid.axis_min(1))
                keep(f"{grid.axis_min(0)}, {grid.axis_min(1)} -- {offs[key][0] - grid.axis_min(0)}, {offs[key][1] - grid.axis_min(1)}")
                grid.show_grid_hex(keep)
                keep("-" * 50)

                counts[key].append(i)
                if len(counts[key]) >= 3:
                    if counts[key][-1] - counts[key][-2] == counts[key][-2] - counts[key][-3] and counts[key][-1] - counts[key][-2] != 1:
                        for key in counts:
                            seen.add(key)
                        for val in keep.values:
                            print(val)
                        break

def other_draw(describe, values):
    if describe:
        return "Animate this"
    draw_internal(values, "normal", "")

def other_draw_2(describe, values):
    if describe:
        return "Animate this (for CoinForWares)"
    draw_internal(values, "coin", "_02")

def other_draw_3(describe, values):
    if describe:
        return "Animate this (for cellular_automata)"
    draw_internal(values, "ca", "_03")

def other_draw_4(describe, values):
    if describe:
        return "Animate this (for cellular_automata, skip every other)"
    draw_internal(values, "ca2", "_04")

def other_draw_5(describe, values):
    if describe:
        return "Animate this (for cellular_automata, skip every third)"
    draw_internal(values, "ca3", "_05")

def draw_internal(values, draw_type, file_extra):
    import os
    from dummylog import DummyLog

    for cur in os.listdir('.'):
        if cur.startswith("frame_") and cur.endswith(".png"):
            os.unlink(cur)

    print("First pass")
    size = calc(DummyLog(), values, 2, draw={
        "mode": "size",
        "skip": 0,
    })
    print("Draw pass")
    calc(DummyLog(), values, 2, draw={
        "mode": "draw", 
        "size": size,
        "type": draw_type,
        "skip": 0,
    })

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "10", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", "animation_%02d%s.mp4" % (get_desc()[0], file_extra)),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def test(log):
    values = log.decode_values("""
        sesenwnenenewseeswwswswwnenewsewsw
        neeenesenwnwwswnenewnwwsewnenwseswesw
        seswneswswsenwwnwse
        nwnwneseeswswnenewneswwnewseswneseene
        swweswneswnenwsewnwneneseenw
        eesenwseswswnenwswnwnwsewwnwsene
        sewnenenenesenwsewnenwwwse
        wenwwweseeeweswwwnwwe
        wsweesenenewnwwnwsenewsenwwsesesenwne
        neeswseenwwswnwswswnw
        nenwswwsewswnenenewsenwsenwnesesenew
        enewnwewneswsewnwswenweswnenwsenwsw
        sweneswneswneneenwnewenewwneswswnese
        swwesenesewenwneswnwwneseswwne
        enesenwswwswneneswsenwnewswseenwsese
        wnwnesenesenenwwnenwsewesewsesesew
        nenewswnwewswnenesenwnesewesw
        eneswnwswnwsenenwnwnwwseeswneewsenese
        neswnwewnwnwseenwseesewsenwsweewe
        wseweeenwnesenwwwswnew
    """)

    log.test(calc(log, values, 1), 10)
    log.test(calc(log, values, 2), 2208)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

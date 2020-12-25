#!/usr/bin/env python3

import re
import math

def get_desc():
    return 24, 'Day 24: Lobby Layout'

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

    r = re.compile("(e|se|sw|w|nw|ne)")
    for row in values:
        x, y = 0, 0
        grid[x, y] = grid[x, y]
        trail = set([(x, y)])
        for m in r.finditer(row):
            hit = m.group(1)
            if hit == "e":
                x += 2
            elif hit == "w":
                x -= 2
            elif hit == "se":
                y += 1
                x += 1
            elif hit == "sw":
                y += 1
                x -= 1
            elif hit == "ne":
                y -= 1
                x += 1
            elif hit == "nw":
                y -= 1
                x -= 1
            if draw["mode"] == "draw":
                grid[x, y] = grid[x, y]
                trail.add((x, y))
        grid[x, y] = "#" if grid[x, y] == "." else "."
        if draw["mode"] == "draw" and draw["type"] not in {"ca", "ca2", "ca3"}:
            for x, y in trail:
                grid[x, y] = ".t" if grid[x, y] == "." else "#t"
            draw_grid("flipping")
            for x, y in trail:
                grid[x, y] = "." if grid[x, y] == ".t" else "#"

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

#!/usr/bin/env python3

import re
import math

def get_desc():
    return 24, 'Day 24: Lobby Layout'

def get_hex(image_width, image_height, draw_type, side_length=1):
    h = math.sin(math.pi / 3)
    ret = []
    for x in range(-1, image_width, 3):
        if x * side_length < image_height + 50:
            for y in range(-1, int(image_height / h) + 1):
                if ((y + 1) * h) * side_length < image_width + 50:
                    xo = x if (y % 2 == 0) else x + 1.5

                    ret.append([
                        (xo,        y * h),
                        (xo + 1,    y * h),
                        (xo + 1.5, (y + 1) * h),
                        (xo + 1,   (y + 2) * h),
                        (xo,       (y + 2) * h),
                        (xo - 0.5, (y + 1) * h),
                    ])

    for i in range(len(ret)):
        ret[i] = [(y * side_length, x * side_length) for (x, y) in ret[i]]

    if draw_type == "normal":
        ret = [x for x in ret if min([y[0] for y in x]) > 0]
        ret = [x for x in ret if min([y[1] for y in x]) > 0]
        ret = [x for x in ret if max([y[0] for y in x]) < image_width]
        ret = [x for x in ret if max([y[1] for y in x]) < image_height]
    else:
        ret = [x for x in ret if max([y[0] for y in x]) > 0]
        ret = [x for x in ret if max([y[1] for y in x]) > 0]
        ret = [x for x in ret if min([y[0] for y in x]) < image_width]
        ret = [x for x in ret if min([y[1] for y in x]) < image_height]

    return ret


def calc(log, values, mode, draw={"mode": 0}):
    from grid import Grid
    grid = Grid(".")

    if draw["mode"] == "draw":
        frame = 0
        from PIL import Image, ImageDraw
        img_width = 13 * draw["height"]
        img_height = img_width

        temp = {}
        x_levels = set()
        y_levels = set()
        hex = []
        for cur in get_hex(img_width, img_height, draw["type"], 8):
            min_x = min([x[0] for x in cur])
            min_y = min([x[1] for x in cur])
            x_levels.add(min_x)
            y_levels.add(min_y)
            hex.append({
                "hex": cur,
                "min_x": min_x,
                "min_y": min_y,
            })

        x_levels = list(sorted(x_levels))
        y_levels = list(sorted(y_levels))

        x_off = None
        for y in range(len(y_levels)):
            temp = sorted([x for x in hex if x["min_y"] == y_levels[y]], key=lambda x:x["min_x"])
            if x_off is None:
                x_off = -(len(temp) // 2)
            x = x_off
            for cur in temp:
                cur["y"] = y - (len(y_levels) // 2)
                cur["x"] = x * 2
                if cur["y"] % 2 == 1:
                    cur["x"] += 1
                x += 1
        # print(max([x["x"] for x in hex]) - min([x["x"] for x in hex]))
        # print(max([x["y"] for x in hex]) - min([x["y"] for x in hex]))
        # print(draw["width"], draw["height"])

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
        grid[x, y] = "X" if grid[x, y] == "." else "."
        if draw["mode"] == "draw" and draw["type"] not in {"ca", "ca2", "ca3"}:
            image = Image.new('RGB', (img_width, img_height), (128, 128, 128))
            dr = ImageDraw.Draw(image)
            for cur in hex:
                if (cur["x"], cur["y"]) in grid.grid or draw["type"] in {"coin", "ca", "ca2", "ca3"}:
                    if grid[cur["x"], cur["y"]] == "X":
                        if (cur["x"], cur["y"]) in trail:
                            color = (0, 0, 192)
                        else:
                            color = (0, 0, 0)
                    else:
                        if (cur["x"], cur["y"]) in trail:
                            color = (192, 192, 255)
                        else:
                            color = (192, 192, 192)
                    dr.polygon(cur["hex"], outline=(64,64,64), fill=color)
            log("Saving frame " + str(frame))
            image.save("frame_%05d.png" % (frame,))
            frame += 1

    if mode == 1:
        return len([x for x in grid.grid.values() if x == "X"])

    dirs = [(-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1)]

    for _ in range(100 if draw.get("type", "normal") == "normal" else 500):
        todo = []
        for y in grid.axis_range(1, 1):
            for x in grid.axis_range(0, 2):
                use = False
                if y % 2 == 0:
                    if x % 2 == 0:
                        use = True
                else:
                    if x % 2 == 1:
                        use = True
                if use:
                    black = 0
                    for xo, yo in dirs:
                        if grid[x + xo, y + yo] == "X":
                            black += 1
                    if grid[x, y] == "X" and (black == 0 or black > 2):
                        todo.append((x, y, "."))
                    if grid[x, y] == "." and black == 2:
                        todo.append((x, y, "X"))

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
                image = Image.new('RGB', (img_width, img_height), (128, 128, 128))
                dr = ImageDraw.Draw(image)
                for cur in hex:
                    if (cur["x"], cur["y"]) in grid.grid or draw["type"] in {"coin", "ca", "ca2", "ca3"}:
                        dr.polygon(cur["hex"], outline=(64,64,64), fill=(0,0,0) if grid[cur["x"], cur["y"]] == "X" else (192, 192, 192))
                log(f"Saving life frame {frame} for {draw['type']}")
                image.save("frame_%05d.png" % (frame,))
                frame += 1

    if draw["mode"] == "size":
        return grid.width(), grid.height()

    if draw["mode"] == "draw":
        for _ in range(30):
            image.save("frame_%05d.png" % (frame,))
            frame += 1

    return len([x for x in grid.grid.values() if x == "X"])

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
    from dummylog import DummyLog
    print("First pass")
    width, height = calc(DummyLog(), values, 2, draw={
        "mode": "size",
        "skip": 0,
    })
    print("Draw pass")
    calc(DummyLog(), values, 2, draw={
        "mode": "draw", 
        "width": width, "height": height,
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

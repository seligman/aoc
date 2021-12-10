#!/usr/bin/env python3

import re

def get_desc():
    return 5, 'Day 5: Hydrothermal Venture'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid()
    r = re.compile("(\d+),(\d+) -> (\d+),(\d+)")
    frame = 0
    for cur in values:
        m = r.search(cur)
        if m:
            x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            if x1 == x2 or y1 == y2 or mode == 2:
                x, y = x1, y1
                while True:
                    grid[x, y] += 1
                    if (x, y) == (x2, y2):
                        break
                    if x2 > x1: x += 1
                    elif x2 < x1: x -= 1
                    if y2 > y1: y += 1
                    elif y2 < y1: y -= 1
            if draw:
                x = len([x for x in grid.grid.values() if x > 1])
                if frame % 50 == 0:
                    print(f"Saving frame {frame}")
                frame += 1
                grid.save_frame(extra_text=[f"{x} overlap points"])

    if draw:
        colors = {
            0: (0, 0, 0),
            1: (128, 128, 128),
        }
        for cur in set(grid.grid.values()):
            if cur not in colors:
                colors[cur] = (255, 128, 128)

        grid.draw_frames(color_map=colors, show_lines=False, cell_size=(2, 2), font_size=50)

    return len([x for x in grid.grid.values() if x > 1])

def test(log):
    values = log.decode_values("""
        0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2
    """)

    log.test(calc(log, values, 1), 5)
    log.test(calc(log, values, 2), 12)

def other_draw(describe, values):
    if describe:
        return "Animate this"
    from dummylog import DummyLog
    import animate

    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(get_desc())


def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

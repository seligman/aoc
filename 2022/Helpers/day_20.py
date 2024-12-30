#!/usr/bin/env python3

# Animation: https://youtu.be/Df63_i2p7jA

DAY_NUM = 20
DAY_DESC = 'Day 20: Grove Positioning System'

def calc(log, values, mode, get_values=False, return_updates=None):
    key = 811589153
    values = [(int(x) * (1 if mode == 1 else key), i) for i, x in enumerate(values)]

    if mode == 1:
        passes = 1
    elif mode == 2:
        passes = 10

    todo = [x for x in values if x[0] != 0]

    for _ in range(passes):
        for x in todo:
            cur_pos = values.index(x)
            next_pos = (cur_pos + x[0]) % (len(values)-1)
            if next_pos == 0: next_pos = len(values)
            values.insert(next_pos, values.pop(cur_pos))
            if return_updates:
                return_updates(cur_pos, next_pos % len(values), values)

    if return_updates:
        return_updates(None, None, values)

    if get_values:
        return values

    at = min(i for i, (x, _) in enumerate(values) if x == 0)
    return sum(values[(i * 1000 + at) % len(values)][0] for i in range(1, 4))

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import colorsys # optional package
    from PIL import Image, ImageDraw # optional package
    import animate
    import math

    animate.prep()

    scale = 4

    targets = calc(DummyLog(), values, 1, get_values=True)
    colors = {}
    locs = {}
    for i, (x, node) in enumerate(targets):
        rgb = colorsys.hsv_to_rgb(i / len(targets), 1, 1)
        rgb = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        radius = 325 * scale
        mid_x = 640 * scale
        mid_y = 360 * scale
        colors[node] = rgb
        locs[i] = (
            math.cos(2 * math.pi / len(targets) * i) * radius + mid_x, 
            math.sin(2 * math.pi / len(targets) * i) * radius + mid_y,
        )

    max_trail = 100
    trail = [(None, None)] * max_trail
    steps = 0
    frame = 0
    def helper(cur_pos, next_pos, targets):
        nonlocal steps, frame
        if cur_pos is not None:
            trail.append((cur_pos, next_pos))
            while len(trail) > max_trail:
                trail.pop(0)

        while True:
            steps += 1
            if steps % 5 == 0:
                im = Image.new('RGB', (1280 * scale, 720 * scale), (0, 0, 0))
                dr = ImageDraw.ImageDraw(im)

                for i, (a, b) in enumerate(trail):
                    if a is not None:
                        gray = int((i / max_trail) * 128)
                        dr.line((locs[a], locs[b]), (gray, gray, gray), 2 * scale)

                for i, (x, node) in enumerate(targets):
                    pt = locs[i]
                    rgb = colors[node]
                    size = 10 * scale
                    dr.ellipse((pt[0] - size, pt[1] - size, pt[0] + size, pt[1] + size), rgb)
                
                if scale > 1:
                    im = im.resize((1280, 720), Image.Resampling.LANCZOS)
                im.save(f"frame_{frame:05d}.png")
                if frame % 10 == 0:
                    print(f"Saved {frame}")
                frame += 1
                if len(trail) == 0:
                    break
            if cur_pos is not None:
                break
            if len(trail) > 0:
                trail.pop(0)

    calc(DummyLog(), values, 1, return_updates=helper)

    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def test(log):
    values = log.decode_values("""
        1
        2
        -3
        3
        -2
        0
        4
    """)

    log.test(calc(log, values, 1), '3')
    log.test(calc(log, values, 2), '1623178306')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2022/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

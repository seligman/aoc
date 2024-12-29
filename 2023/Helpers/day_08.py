#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Haunted Wasteland'

def calc(log, values, mode, draw=False):
    import re
    dirs = values[0]
    map = {}
    for row in values[2:]:
        m = re.search("([A-Z0-9]+) = \\(([A-Z0-9]+), ([A-Z0-9]+)\\)", row)
        name, l, r = m.group(1), m.group(2), m.group(3)
        map[name] = (l, r)
    
    if mode == 1:
        pos = ["AAA"]
    else:
        pos = [x for x in map if x.endswith("A")]

    if draw:
        # TODO: Work on this?
        import networkx
        seen = set()
        temp = [pos[0]]
        edges = []
        while len(temp) > 0:
            if temp[0] not in seen:
                seen.add(temp[0])
                edges.append((temp[0], map[temp[0]][0]))
                edges.append((temp[0], map[temp[0]][1]))
                temp.append(map[temp[0]][0])
                temp.append(map[temp[0]][1])
            temp.pop(0)

        graph = networkx.from_edgelist(edges)
        points = networkx.spring_layout(graph, iterations=100)
        for node in list(points):
            points[node] = [points[node][0] * 500 + 500, points[node][1] * 500 + 500]
        print(points)
        draw_frame(1000, 1000, 0, seen, map, points)
        # TODO: Determine how to do this
        exit(0)

    ret = []
    for pos in pos:
        steps = 0
        while True:
            pos = map[pos][0 if dirs[steps % len(dirs)] == "L" else 1]

            if mode == 1:
                if pos == "ZZZ":
                    break
            else:
                if pos.endswith("Z"):
                    break
            steps += 1
        ret.append(steps + 1)


    if mode == 1:
        return ret[0]
    else:
        import math
        return math.lcm(*ret)

def test(log):
    values = log.decode_values("""
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
    """)

    log.test(calc(log, values, 1), '6')

    values = log.decode_values("""
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
    """)

    log.test(calc(log, values, 2), '6')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)

source_code = None
def draw_frame(im_width, im_height, frame, seen, map, points):
    from PIL import Image, ImageDraw, ImageFont
    import os

    # font_size = im_width * 0.01
    # circ_size = int(im_width * 0.02)

    global source_code
    # if source_code is None:
    #     source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
    #     source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))

    im = Image.new('RGB', (im_width, im_height), (0, 0, 0))
    dr = ImageDraw.Draw(im)

    for node in seen:
        l, r = map[node]
        x1, y1 = points[node]
        for dest in [l, r]:
            x2, y2 = points[dest]
            dr.line((x1, y1, x2, y2), (192, 192, 192), width=int(im_width * 0.001))

    im.save(f"frame_{frame:05d}.png")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

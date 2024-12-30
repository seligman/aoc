#!/usr/bin/env python3

# Animation: https://youtu.be/XyWthomQ9mM

import re
from collections import deque

DAY_NUM = 16
DAY_DESC = 'Day 16: Proboscidea Volcanium'

class Node:
    __slots__ = ['rate', 'node_name', 'tunnels', 'opened', 'valve_num']
    def __init__(self, value, next_valve_num):
        m = re.search("Valve (.*?) has flow rate=(.*?)\\; tunnels? leads? to valves? (.*?)$", value)
        self.node_name, self.rate, self.tunnels = m.groups()
        self.rate = int(self.rate)
        self.tunnels = self.tunnels.split(", ")
        self.opened = False
        if self.rate > 0:
            self.valve_num = 1 << next_valve_num[0]
            next_valve_num[0] += 1
        else:
            self.valve_num = 0
    
class State:
    __slots__ = ['a', 'b', 'opened', 'pressure', 'history']
    def __init__(self, a, b, opened, pressure, history, verb_a, verb_b):
        self.a = a
        self.b = b
        self.opened = opened
        self.pressure = pressure
        self.history = history + [(verb_a, a, verb_b, b, pressure)]

    def __repr__(self):
        return f"{self.a}-{self.b},{self.opened},{self.pressure}"

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=35)

def layout_points(points, im_width, im_height):
    offsets = {}

    minx = min(x for x,y in points.values())
    maxx = max(x for x,y in points.values())
    miny = min(y for x,y in points.values())
    maxy = max(y for x,y in points.values())

    spanx = maxx - minx
    spany = maxy - miny

    minx -= spanx * 0.01
    maxx += spanx * 0.01
    miny -= spany * 0.01
    maxy += spany * 0.01

    circ_size = int(im_width * 0.02)
    offsets = {}
    for node, (x, y) in points.items():
        x = ((x - minx) / (maxx - minx)) * (im_width - (circ_size * 2)) + circ_size
        y = ((y - miny) / (maxy - miny)) * (im_height - (circ_size * 2 + circ_size)) + circ_size
        offsets[node] = (x, y)
    
    return offsets

source_code = None
def draw_frame(nodes, points, last_step, step, info, offsets, im_width, im_height):
    from PIL import Image, ImageDraw, ImageFont # optional package
    import os

    font_size = im_width * 0.01
    circ_size = int(im_width * 0.02)

    global source_code
    if source_code is None:
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))

    if step is not None:
        a_verb, a_dest, b_verb, b_dest, pressure = step
        is_opening = set()
        if a_verb == "open":
            is_opening.add(a_dest)
        if b_verb == "open":
            is_opening.add(b_dest)  

        move_a, move_b = None, None
        if a_verb == "move":
            move_a = a_dest
        if b_verb == "move":
            move_b = b_dest
    else:
        pressure = 9999
        move_a, move_b = None, None

    for cur_step in range(0, 1 if step is None else 30):
        im = Image.new('RGB', (im_width, im_height), (0, 0, 0))
        dr = ImageDraw.Draw(im)

        for node in nodes.values():
            x1, y1 = offsets[node.node_name]
            for dest in node.tunnels:
                x2, y2 = offsets[dest]
                dr.line((x1, y1, x2, y2), (192, 192, 192), width=int(im_width * 0.01))

        perc = (cur_step / 29)
        sqt = perc * perc
        perc_ease = sqt / (2 * (sqt - perc) + 1)

        for node, (x, y) in offsets.items():
            msg = [node]
            color = (255, 255, 255)
            if nodes[node].rate > 0:
                msg.append(str(nodes[node].rate))
                if step is not None and node in is_opening:
                    color = (
                        int(32 * perc + 255 * (1 - perc)),
                        32,
                        int(255 * perc + 32 * (1 - perc)),
                    )
                elif node in info["opened"]:
                    color = (32, 32, 255)
                else:
                    color = (255, 32, 32)

            dr.ellipse((x - circ_size, y - circ_size, x + circ_size, y + circ_size), fill=color)
            
            height = 0
            for line in msg:
                height += dr.textsize(line, source_code)[1]
            ty = y - height // 2
            for line in msg:
                sx, sy = dr.textsize(line, source_code)
                dr.text((x - sx // 2, ty), line, (32, 32, 32), source_code)
                ty += sy

        msg = f"Time: {info['time'] + perc:3.1f}\nPressure: {pressure:5,}"
        dr.text((10, 10), msg, (255, 255, 255), source_code)

        for move_x, key, desc in ((move_a, "pos_a", "[A]"), (move_b, "pos_b", "[B]")):
            if move_x is None:
                x, y = offsets[info[key]]
            else:
                x = offsets[move_x][0] * perc_ease + offsets[info[key]][0] * (1 - perc_ease)
                y = offsets[move_x][1] * perc_ease + offsets[info[key]][1] * (1 - perc_ease)

            w, h = dr.textsize(desc, source_code)
            dr.rectangle((x - w / 2, y + circ_size - h / 2, x + w / 2, y + circ_size + h / 2), fill=(50, 50, 50))
            dr.text((x - w / 2, y + circ_size - h / 2), desc, fill=(255, 192, 192), font=source_code)

        im.save(f"frame_{info['frame']:05d}.png")
        if step is not None:
            info['frame'] += 1

    if step is not None:
        info["opened"] |= is_opening
        if move_a is not None:
            info["pos_a"] = move_a
        if move_b is not None:
            info["pos_b"] = move_b
        info["time"] += 1

def draw_steps(nodes, points, history, im_width, im_height):
    last_step = None
    info = {
        "frame": 0,
        "opened": set(),
        "pos_a": "AA",
        "pos_b": "AA",
        "time": 0,
    }
    for i in range(len(history)-1, -1, -1):
        x = history[i]
        if x[0] != "move":
            break
        history[i] = ("", x[1], x[2], x[3], x[4])
    for i in range(len(history)-1, -1, -1):
        x = history[i]
        if x[2] != "move":
            break
        history[i] = (x[0], x[1], "", x[3], x[4])

    offsets = layout_points(points, im_width, im_height)

    for step in history:
        draw_frame(nodes, points, last_step, step, info, offsets, im_width, im_height)
        last_step = step

def calc(log, values, mode, draw=False):
    next_valve_num = [0]
    nodes = {x.node_name: x for x in [Node(y, next_valve_num) for y in values]}
    first = min(nodes.keys())

    if draw:
        im_width, im_height = 1080, 1080
        saved_points = {
            "AA": [-0.2592,  0.1372], "AH": [-0.2626,  0.5164], "AL": [-0.1706,  0.2748], "AM": [ 0.0168,  0.3657], "CD": [-0.3164, -0.7735], "CE": [-0.2950, -0.4771],
            "CS": [-0.4092,  0.2149], "CX": [-0.0168,  0.2873], "DC": [-0.1999, -0.9999], "DU": [ 0.1395,  0.4486], "DX": [ 0.0199, -0.9806], "EA": [ 0.2278,  0.0482],
            "EI": [ 0.6691, -0.0972], "GX": [ 0.1351, -0.1384], "HD": [ 0.4788, -0.2034], "HS": [-0.1963,  0.4810], "JC": [-0.3452, -0.6604], "JI": [ 0.2549, -0.2687],
            "MS": [-0.3064,  0.3240], "MW": [ 0.9139,  0.3389], "NC": [ 0.2471,  0.6917], "NM": [-0.1315, -0.9671], "NU": [-0.0577,  0.4272], "OE": [-0.0952,  0.1608],
            "OV": [-0.2733,  0.6155], "PY": [ 0.9004,  0.1912], "QC": [-0.3108,  0.4572], "QE": [ 0.1205,  0.1601], "RA": [ 0.0066, -0.2856], "RN": [-0.0912,  0.5709],
            "SH": [ 0.2944,  0.4498], "TK": [-0.1408, -0.0898], "TP": [-0.0941, -0.5014], "UB": [ 0.8125,  0.0400], "UE": [-0.2022, -0.8613], "UI": [ 0.3688,  0.5748],
            "VE": [-0.2813, -0.9001], "VJ": [-0.4360,  0.3531], "VQ": [ 0.0672,  0.7148], "WC": [-0.1946,  0.0872], "WD": [-0.1486, -0.3905], "WK": [-0.1253,  0.6411],
            "XI": [-0.0202,  0.6181], "XK": [-0.2164, -0.6897], "XO": [ 0.3479,  0.2071], "XS": [-0.3962, -0.5669], "YH": [-0.3874, -0.8043], "YP": [ 0.1397, -0.9770],
            "YS": [-0.1767,  0.3682], "ZG": [ 0.3864,  0.3973], "ZN": [ 0.0104,  0.4694],
        }
        while True:
            if saved_points is None:
                import networkx
                edges = []
                for x in nodes.values():
                    for y in x.tunnels:
                        edges.append((x.node_name, y))
                graph = networkx.from_edgelist(edges)
                points = networkx.fruchterman_reingold_layout(graph, iterations=50)
            else:
                points = saved_points
                saved_points = None
            points = {k: (int(x * 10000) / 10000, int(y * 10000) / 10000) for k, (x, y) in points.items()}
            info = {
                "frame": 0,
                "opened": set(),
                "pos_a": "AA",
                "pos_b": "AA",
                "time": 0,
            }
            offsets = layout_points(points, im_width, im_height)
            draw_frame(nodes, points, None, None, info, offsets, im_width, im_height)
            cluster = False
            for x in offsets:
                if cluster:
                    break
                for y in offsets:
                    if x != y:
                        dist = (offsets[x][0] - offsets[y][0]) * (offsets[x][0] - offsets[y][0]) + (offsets[x][1] - offsets[y][1]) * (offsets[x][1] - offsets[y][1])
                        if dist <= int(im_width * 0.035) * int(im_width * 0.035):
                            cluster = True
                            break

            if cluster:
                print("Ignoring clustered image")
            else:
                yn = input("Does that frame look good? [y/(n)] ")
                if yn == "y":
                    print("Use this variable to save this layout: ")
                    print("-" * 100)
                    print(" " * 8 + "saved_points = {")
                    line = " " * 12
                    for k, (x, y) in [(x, points[x]) for x in sorted(points)]:
                        line += f'"{k}": [{x:7.4f}, {y:7.4f}], '
                        if len(line) > 150:
                            print(line)
                            line = " " * 12
                    if len(line.strip()) > 0:
                        print(line)
                    print(" " * 8 + "}")
                    print("-" * 100)
                    break

    best = {}
    target_best = 0

    def is_best(val):
        if val.pressure < target_best:
            return False

        key = (val.a, val.b, val.opened)

        if key not in best or val.pressure > best[key].pressure:
            best[key] = val
            return True
            
        return False

    best_history = []
    total_time = 30 if mode == 1 else 26
    states = deque([State(first, None if mode == 1 else first, 0, 0, [], "start", "start")])

    for time in range(1, total_time + 1):
        best_history.append(0 if len(best) == 0 else max(x.pressure for x in best.values()))
        best_change = max(x.rate for x in nodes.values()) * (total_time - time)
        target_best = int(best_history[-1] - best_change)

        next_states = deque()
        for cur in states:
            node_a = nodes[cur.a]
            node_b = None if cur.b is None else nodes[cur.b]

            if node_a.rate > 0 and (node_a.valve_num & cur.opened) == 0:
                if node_b is not None and node_b.rate > 0 and (node_b.valve_num & cur.opened) == 0 and node_b.valve_num != node_a.valve_num:
                    val = State(
                        node_a.node_name, 
                        node_b.node_name, 
                        cur.opened | node_a.valve_num | node_b.valve_num, 
                        cur.pressure + node_a.rate * (total_time - time) + node_b.rate * (total_time - time),
                        cur.history, "open", "open",
                    )
                    if is_best(val): next_states.append(val)
                for y in [None] if node_b is None else node_b.tunnels:
                    val = State(node_a.node_name, y, cur.opened | node_a.valve_num, cur.pressure + node_a.rate * (total_time - time), cur.history, "open", "move")
                    if is_best(val): next_states.append(val)
            for x in node_a.tunnels:
                if node_b is not None and node_b.rate > 0 and (node_b.valve_num & cur.opened) == 0:
                    val = State(x, node_b.node_name, cur.opened | node_b.valve_num, cur.pressure + node_b.rate * (total_time - time), cur.history, "move", "open")
                    if is_best(val): next_states.append(val)
                for y in [None] if node_b is None else node_b.tunnels:
                    val = State(x, y, cur.opened, cur.pressure, cur.history, "move", "move")
                    if is_best(val): next_states.append(val)
        states = next_states

    if draw:
        for x in best.values():
            if x.pressure == best_history[-1]:
                draw_steps(nodes, points, x.history, im_width, im_height)
                break

    return best_history[-1]

def test(log):
    values = log.decode_values("""
        Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        Valve BB has flow rate=13; tunnels lead to valves CC, AA
        Valve CC has flow rate=2; tunnels lead to valves DD, BB
        Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
        Valve EE has flow rate=3; tunnels lead to valves FF, DD
        Valve FF has flow rate=0; tunnels lead to valves EE, GG
        Valve GG has flow rate=0; tunnels lead to valves FF, HH
        Valve HH has flow rate=22; tunnel leads to valve GG
        Valve II has flow rate=0; tunnels lead to valves AA, JJ
        Valve JJ has flow rate=21; tunnel leads to valve II
    """)

    log.test(calc(log, values, 1), 1651)
    log.test(calc(log, values, 2), 1707)

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

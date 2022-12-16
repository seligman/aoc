#!/usr/bin/env python3

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

source_code = None
def draw_frame(nodes, points, last_step, step, info):
    from PIL import Image, ImageDraw, ImageFont
    import os
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

    im_width, im_height = 1024, 1024
    font_size = im_width * 0.01

    global source_code
    if source_code is None:
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))

    circ_size = int(im_width * 0.02)
    offsets = {}
    for node, (x, y) in points.items():
        x = ((x - minx) / (maxx - minx)) * (im_width - (circ_size * 2)) + circ_size
        y = ((y - miny) / (maxy - miny)) * (im_height - (circ_size * 2 + circ_size)) + circ_size
        offsets[node] = (x, y)
    
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
                dr.line((x1, y1, x2, y2), (192, 192, 192))

        perc = (cur_step / 29)
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
                x = offsets[move_x][0] * perc + offsets[info[key]][0] * (1 - perc)
                y = offsets[move_x][1] * perc + offsets[info[key]][1] * (1 - perc)

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

def draw_steps(nodes, points, history):
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

    for step in history:
        draw_frame(nodes, points, last_step, step, info)
        last_step = step

def calc(log, values, mode, draw=False):
    next_valve_num = [0]
    nodes = {x.node_name: x for x in [Node(y, next_valve_num) for y in values]}
    first = min(nodes.keys())

    if draw:
        import networkx
        edges = []
        for x in nodes.values():
            for y in x.tunnels:
                edges.append((x.node_name, y))
        graph = networkx.from_edgelist(edges)
        while True:
            points = networkx.fruchterman_reingold_layout(graph, iterations=50)
            info =     info = {
                    "frame": 0,
                    "opened": set(),
                    "pos_a": "AA",
                    "pos_b": "AA",
                    "time": 0,
                }
            draw_frame(nodes, points, None, None, info)
            yn = input("Good frame? ")
            if yn == "y":
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
                draw_steps(nodes, points, x.history)
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
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

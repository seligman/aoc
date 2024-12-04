#!/usr/bin/env python3

import re
from collections import defaultdict

DAY_NUM = 16
DAY_DESC = 'Day 16: Ticket Translation'

def in_range(value, rule):
    for range in rule["ranges"]:
        if range[0] <= value <= range[1]:
            return True
    return False

def calc(log, values, mode, draw=0):
    rules = []
    valid_values = []
    invalid = 0

    for cur in values:
        m = re.search(r"^(?P<name>[a-z ]+): (?P<x1>[\d]+)-(?P<y1>[\d]+) or (?P<x2>[\d]+)-(?P<y2>[\d]+)", cur)
        if m is not None:
            rules.append({
                "name": m.group("name"),
                "ranges": [
                    [int(m.group("x1")), int(m.group("y1"))],
                    [int(m.group("x2")), int(m.group("y2"))],
                ],
                "position": None,
                'possibles': set(),
            })

        m = re.search(r"^[\d,]+$", cur)
        if m is not None:
            cur = [int(x) for x in cur.split(",")]
            all_valid = True
            for x in cur:
                if not max([in_range(x, rule) for rule in rules]):
                    invalid += x
                    all_valid = False

            if all_valid:
                valid_values.append(cur)

    if mode == 1:
        return invalid

    if mode == 2:
        steps = []
        ticket, valid_values = valid_values[0], valid_values[1:]
        for i in range(len(ticket)):
            for rule in rules:
                if min([in_range(x[i], rule) for x in valid_values]):
                    rule["possibles"].add(i)

        left = len(rules)
        while left > 0:
            temp = {x:[] for x in range(len(ticket))}
            for rule in rules:
                for x in rule["possibles"]:
                    temp[x].append(rule)

            for val, targets in temp.items():
                if len(targets) == 1:
                    targets[0]['position'] = val
                    targets[0]['possibles'] = set()
                    steps.append(targets[0]['name'])
                    left -= 1

        xys = {}
        for cur in ["departure", "arrival", "-"]:
            xys[cur] = {
                "x": 0,
                "y": 0,
                "max": 0,
                "data": []
            }
        
        ret = 1
        for rule in rules:
            if rule['name'].startswith("departure"):
                ret *= ticket[rule['position']]

        if draw == 1:
            for rule in rules:
                temp = rule['name']
                cat = "-"
                for cur in ["departure", "arrival"]:
                    if temp.startswith(cur + " "):
                        cat = cur
                        temp = temp[len(cur)+1:]
                rule['xy'] = (xys[cat]['x'], xys[cat]['y'])
                rule['temp'] = temp
                rule['value'] = "%3s" % (ticket[rule['position']],)
                xys[cat]['max'] = max(len(temp), xys[cat]['max'])
                xys[cat]['x'] += 1
                xys[cat]['data'].append(rule)
                if xys[cat]['x'] == 2:
                    xys[cat]['x'] = 0
                    xys[cat]['y'] += 1
            
            from grid import Grid
            disp = Grid(default = ' ')
            def insert(disp, x, y, value, fixup=None, fixup_name=None, target=None):
                for cur in value:
                    disp[x, y] = cur
                    if fixup is not None:
                        fixup[fixup_name].append((x, y, cur))
                    x += 1
                if fixup is not None:
                    temp = len(value)
                    while temp < target:
                        fixup[fixup_name].append((x, y, ' '))
                        x += 1
                        temp += 1

            disp[0, 0] = " "
            fixup = {}
            y = 0
            insert(disp, 2, 1, " -- departure --")
            for rule in xys["departure"]['data']:
                y = max(y, rule['xy'][1])
                fixup[rule['name']] = []
                insert(disp, 2 + rule['xy'][0] * (xys['departure']['max'] + 5), rule['xy'][1] + 2, rule['temp'], fixup=fixup, fixup_name=rule['name'], target=xys['departure']['max'])
                insert(disp, 2 + xys['departure']['max'] + 1 + rule['xy'][0] * (xys['departure']['max'] + 5), rule['xy'][1] + 2, rule['value'])

            y += 3
            insert(disp, 2, y, " -- arrival --")
            for rule in xys["arrival"]['data']:
                fixup[rule['name']] = []
                insert(disp, 2 + rule['xy'][0] * (xys['arrival']['max'] + 5), rule['xy'][1] + 1 + y, rule['temp'], fixup=fixup, fixup_name=rule['name'], target=xys['arrival']['max'])
                insert(disp, 2 + xys['arrival']['max'] + 1 + rule['xy'][0] * (xys['arrival']['max'] + 5), rule['xy'][1] + 1 + y, rule['value'])

            x = disp.width() + 5
            for rule in xys['-']['data']:
                fixup[rule['name']] = []
                insert(disp, x + rule['xy'][0] * (xys['-']['max'] + 5), rule['xy'][1] + 2, rule['temp'], fixup=fixup, fixup_name=rule['name'], target=xys['-']['max'])
                insert(disp, x + xys['-']['max'] + 1 + rule['xy'][0] * (xys['-']['max'] + 5), rule['xy'][1] + 2, rule['value'])
            y = disp.height()

            for x in range(disp.width() + 2):
                disp[x, 0] = "-"
                disp[x, y] = "-"
            disp[0, 0] = "+"
            disp[disp.width() - 1, 0] = "+"
            disp[0, disp.height() - 1] = "+"
            disp[disp.width() - 1, disp.height() - 1] = "+"
            for y in range(1, disp.height() - 1):
                disp[0, y] = "|"
                disp[disp.width() - 1, y] = "|"
            
            return disp, fixup, steps

        return ret

def other_draw(describe, values):
    if describe:
        return "Animate this"
    
    from dummylog import DummyLog
    disp, fixup, steps = calc(DummyLog(), values, 2, draw=1)

    for cur in steps:
        for x, y, _ in fixup[cur]:
            disp[x, y] = "*"

    import random
    w, h = disp.get_font_size(13)
    index = 0

    for cur in steps:
        index += 1
        print(f"{index:2d} / {len(steps):2d}: {cur}")
        reveal = list(range(len(fixup[cur])))
        random.shuffle(reveal)
        revealed = set()
        for to_reveal in reveal:
            revealed.add(to_reveal)
            for _ in range(2):
                i = 0
                for x, y, digit in fixup[cur]:
                    color = (0, 0, 0)
                    if i not in revealed:
                        digit = chr(random.randint(33, 125))
                        color = (32, 32, 32)
                    disp[x, y] = [digit, color]
                    i += 1
                disp.draw_grid(show_lines=False, default_color=(0,0,0), font_size=13, cell_size=(w,h), color_map={})

    for y in disp.y_range():
        print("".join([x if isinstance(x, str) else x[0] for x in [disp[x, y] for x in disp.x_range()]]))

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "30", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", "animation_%02d.mp4" % (get_desc()[0],)),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def test(log):
    values = log.decode_values("""
        class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50

        your ticket:
        7,1,14

        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12
    """)

    log.test(calc(log, values, 1), 71)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2020/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

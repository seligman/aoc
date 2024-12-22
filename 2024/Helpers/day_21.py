#!/usr/bin/env python3

DAY_NUM = 21
DAY_DESC = 'Day 21: Keypad Conundrum'

from functools import cache
from collections import defaultdict
from multiprocessing import Pool
import time

_return_path = None
_target_robots = 0

class Pad:
    def __init__(self, data, width):
        self.width = width
        self.height = len(data) // self.width
        self.data = decode_pad(data, self.width)
        self.rev = {v: k for k, v in self.data.items()}
        self.pos = self.data["A"]
    
    def get(self, x, y):
        if x >= self.width or y >= self.height:
            return "  "
        else:
            if self.pos == (x, y):
                return self.rev[(x, y)] + "*"
            else:
                return self.rev[(x, y)] + " "

_fnt = None
def draw_helper(job):
    from grid import Grid
    from PIL import Image, ImageDraw

    global _fnt
    if _fnt is None:
        grid = Grid()
        _fnt = grid.get_font(20)

    im = Image.new('RGBA', (1280, 720), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    x, y = 1, 3
    size = 50

    for pad in job['pads']:
        if x > 23:
            x = 1
            y += 4
        pad.offset = (x, y)
        for ox in range(pad.width):
            for oy in range(pad.height):
                val = pad.rev[(ox, oy)]
                if val != ".":
                    pos = ((x + ox) * size, (y + oy) * size, (x + ox + 1) * size, (y + oy + 1) * size)
                    dr.rectangle(pos, (100, 100, 100), (200, 200, 255))
                    bb = _fnt.getbbox(val)
                    dr.text(((pos[0] + pos[2]) / 2 - (bb[0] + bb[2]) / 2, (pos[1] + pos[3]) / 2 - (bb[1] + bb[3]) / 2), val, (0, 0, 0), font=_fnt)
        x += pad.width + 1
    ended = (x, y)

    seen = set()
    for cur in job['frame']:
        if "pad" in cur:
            seen.add(cur["pad"])
            x = cur["start"][0] * (1 - job['perc']) + cur["end"][0] * job['perc']
            y = cur["start"][1] * (1 - job['perc']) + cur["end"][1] * job['perc']
            x += job['pads'][cur["pad"]].offset[0]
            y += job['pads'][cur["pad"]].offset[1]
            x, y = (x + 0.5) * size, (y + 0.5) * size
            color = None
            if cur["click"]:
                color = (128, 128, 128, int((1 - job['perc']) * 255))
            dr.circle((x, y), radius=size * 0.45, outline=(255, 200, 200), width=3, fill=color)

    for i in range(len(job['pads'])):
        if i not in seen:
            x = job['pos'][i][0] + job['pads'][i].offset[0]
            y = job['pos'][i][1] + job['pads'][i].offset[1]

            x, y = (x + 0.5) * size, (y + 0.5) * size
            dr.circle((x, y), radius=size * 0.45, outline=(255, 200, 200), width=3)

    if len(job["text"]) > 0:
        x, y = ended
        x -= 4
        y += 4
        x, y = (x + 0.5) * size, (y + 0.5) * size
        dr.text((x, y), job["text"], fill=(255, 255, 255), font=_fnt)

    x, y = ended
    x = 3
    y += 2
    x, y = (x + 0.5) * size, (y + 0.5) * size
    dr.text((x, y), f'Steps: {job["step"]:,}', fill=(255, 255, 255), font=_fnt)

    fn = f"frame_{job['frame_no']:05d}.png"
    im.save(fn)
    return fn

def other_draw(describe, values):
    if describe:
        return "Draw this"
    draw_internal(values, 60, 30, "")

def other_draw_long(describe, values):
    if describe:
        return "Draw this, long animation"
    draw_internal(values, 1200, 60, "_long")

def draw_internal(values, secs, frame_rate, extra):
    from dummylog import DummyLog

    global _return_path, _target_robots
    paths = []
    def helper(val):
        paths.append(val)
    _return_path = helper
    _target_robots = 12

    calc(DummyLog(), values, 3)

    pads = []
    while len(pads) < _target_robots - 1:
        pads.append(Pad(".^A<v>", 3))
    pads.append(Pad("789456123.0A", 3))
    pos = [x.pos for x in pads]

    def apply_press(pad, step):
        if step == "<":pad.pos = (pad.pos[0] - 1, pad.pos[1])
        elif step == ">": pad.pos = (pad.pos[0] + 1, pad.pos[1])
        elif step == "^": pad.pos = (pad.pos[0], pad.pos[1] - 1)
        elif step == "v": pad.pos = (pad.pos[0], pad.pos[1] + 1)
        elif step == "A":
            return pad.rev[pad.pos]
        return None

    frames = defaultdict(list)
    for frame_no, step in enumerate(paths[0]):
        temp = step
        i = 0
        while temp is not None and i < len(pads):
            start = pads[i].pos
            temp = apply_press(pads[i], temp)
            frames[frame_no + i].append({"pad": i, "start": start, "end": pads[i].pos, "click": temp is not None})
            i += 1
        if temp is not None:
            frames[frame_no + i].append({"text": temp})

    frame_no = 0
    todo = []
    text = ""
    for i in range(max(frames)+1):
        for cur in frames[i]:
            if "text" in cur:
                text += cur["text"]
        for step in range(10):
            todo.append({
                "pad": i, 
                "perc": step / 10, 
                "frame_no": frame_no, 
                "pads": pads, 
                "pos": pos[:], 
                "frame": frames[i], 
                "text": text, 
                "step": i,
            })
            frame_no += 1
        for cur in frames[i]:
            if "pad" in cur:
                pos[cur["pad"]] = cur["end"]

    from grid import Grid
    grid = Grid()
    grid.ease_frames(rate=frame_rate, secs=secs, frames=todo)
    for i in range(len(todo)):
        todo[i] = todo[i].copy()
        todo[i]['frame_no'] = i

    left = len(todo)
    msg_at = time.time()

    import animate
    animate.prep()

    with Pool() as pool:
        for msg in pool.imap(draw_helper, todo):
            left -= 1
            if time.time() >= msg_at:
                msg_at += 1
                print(f"Saved {msg}, {left} left")

    animate.create_mp4(DAY_NUM, rate=frame_rate, final_secs=5, extra=extra)

def best_dirpad(x, y, dx, dy, robots, invalid):
    ret = None
    todo = [(x, y, "")]

    while len(todo) > 0:
        x, y, path = todo.pop(0)
        if (x, y) == (dx, dy):
            temp = best_robot(path + "A", robots - 1)
            if _return_path is None:
                ret = minn(ret, temp)
            else:
                if ret is None or len(temp) < len(ret):
                    ret = temp
        elif (x, y) != invalid:
            for ox, oy, val in ((-1, 0, "<"), (1, 0, ">"), (0, -1, "^"), (0, 1, "v")):
                if is_dir(x, dx, ox) or is_dir(y, dy, oy):
                    todo.append((x + ox, y + oy, path + val))

    return ret

@cache
def best_robot(path, robots):
    if robots == 1:
        if _return_path is None:
            return len(path)
        else:
            return path

    if _return_path is None:
        ret = 0
    else:
        ret = ""
    pad = decode_pad(".^A<v>", 3)
    x, y = pad["A"]

    for val in path:
        dx, dy = pad[val]
        ret += best_dirpad(x, y, dx, dy, robots, pad["."])
        x, y = dx, dy

    return ret

def minn(*vals):
    vals = [x for x in vals if x is not None]
    return vals[0] if len(vals) == 1 else min(*vals)

def decode_pad(val, width):
    return {val: (x % width, x // width) for x, val in enumerate(val)}

def is_dir(start, dest, change):
    return (change < 0 and dest < start) or (change > 0 and dest > start)

def cheapest(x, y, dx, dy, robots, invalid):
    ret = None
    todo = [(x, y, "")]
    while len(todo) > 0:
        x, y, path = todo.pop(0)
        if (x, y) == (dx, dy):
            temp = best_robot(path + "A", robots)
            if _return_path is None:
                ret = minn(ret, temp)
            else:
                if ret is None or len(temp) < len(ret):
                    ret = temp
        elif (x, y) != invalid:
            for ox, oy, val in ((-1, 0, "<"), (1, 0, ">"), (0, -1, "^"), (0, 1, "v")):
                if is_dir(x, dx, ox) or is_dir(y, dy, oy):
                    todo.append((x + ox, y + oy, path + val))
    return ret

def calc(log, values, mode, draw=False):
    ret = 0
    pad = decode_pad("789456123.0A", 3)
    for row in values:
        result = 0 if _return_path is None else ""
        x, y = pad["A"]
        for val in row:
            dx, dy = pad[val]
            temp = cheapest(x, y, dx, dy, [-1, 3, 26, _target_robots][mode], pad["."])
            result += temp
            x, y = dx, dy
        if _return_path is not None:
            _return_path(result)
        if isinstance(result, str):
            result = len(result)
        ret += result * int(row[:-1].lstrip("0"))
    return ret 

def test(log):
    values = log.decode_values("""
        029A
        980A
        179A
        456A
        379A
    """)

    log.test(calc(log, values, 1), '126384')
    # log.test(calc(log, values, 2), 'TODO')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

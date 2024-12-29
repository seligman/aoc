#!/usr/bin/env python3

# Animation: https://youtu.be/1KsEUjXK9_s

DAY_NUM = 16
DAY_DESC = 'Day 16: The Floor Will Be Lava'

def add_if_new(node, todo, ox ,oy):
    key = (node["x"], node["y"], ox, oy)
    if key not in node["seen"]:
        node = node.copy()
        node["step"] += 1
        node["seen"].add(key)
        node['ox'] = ox
        node['oy'] = oy
        todo.append(node)

queue, procs = None, None
def init_draw():
    import multiprocessing
    global queue, procs
    queue = multiprocessing.Queue()
    procs = [multiprocessing.Process(target=draw_worker, args=(queue,)) for _ in range(multiprocessing.cpu_count())]
    [x.start() for x in procs]

def draw_frame(grid, energy, cell_size, lights, mirrors, frame):
    for i in range(len(lights)-1, -1, -1):
        if lights[i]['age'] > 10:
            lights.pop(i)
    lights_deep = [x.copy() for x in lights]
    queue.put((grid.width(), grid.height(), energy.copy(), cell_size, lights_deep.copy(), mirrors, frame))
    for light in lights:
        light['age'] += 1

def finish_draw():
    [queue.put(None) for _ in procs]
    [x.join() for x in procs]

def draw_worker(queue):
    from PIL import Image, ImageDraw
    while True:
        job = queue.get()
        if job is None:
            break

        width, height, energy, cell_size, lights, mirrors, frame = job
        im = Image.new('RGB', (width * cell_size, height * cell_size), (0, 0, 0))
        dr = ImageDraw.Draw(im)

        for (x, y) in energy:
            dr.rectangle((
                int((x + 0.10) * cell_size + 0.5),
                int((y + 0.10) * cell_size + 0.5),
                int((x + 0.90) * cell_size + 0.5),
                int((y + 0.90) * cell_size + 0.5),
            ), fill=(64, 64, 0))
        for light in lights:
            rgb = int((1 - (light['age'] / 10)) * (255-64) + 64)
            line = [
                int(((light["x2"] + 0.5 - (light["x2"] - light["x1"]) / 2)) * cell_size + 0.5),
                int(((light["y2"] + 0.5 - (light["y2"] - light["y1"]) / 2)) * cell_size + 0.5),
                ((light["x2"] + 0.5) * cell_size + 0.5),
                ((light["y2"] + 0.5) * cell_size + 0.5),
                int(((light["x2"] + 0.5 - (light["x2"] - light["x3"]) / 2)) * cell_size + 0.5),
                int(((light["y2"] + 0.5 - (light["y2"] - light["y3"]) / 2)) * cell_size + 0.5),
            ]
            dr.line(line, fill=(rgb, rgb, 0), width=int(cell_size * 0.2))
        for (x, y), val in mirrors.items():
            if val == "\\": line = [(10,10), (90,90)]
            if val == "/": line = [(10,90), (90,10)]
            if val == "|": line = [(50, 10), (50, 90)]
            if val == "-": line = [(10, 50), (90, 50)]
            line = [(int(((lx / 100) + x) * cell_size + 0.5), int(((ly / 100) + y) * cell_size + 0.5)) for lx, ly in line]
            dr.line(line, fill=(255, 255, 255), width=int(cell_size * 0.1))
        im.save(f"frame_{frame:05d}.png")
        print(f"Saved frame_{frame:05d}.png")

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    from collections import deque
    grid = Grid.from_text(values)

    def get_starts():
        for y in grid.y_range():
            yield {"x": -1, "y": y, "ox": 1, "oy": 0}
            if mode == 1: return
            yield {"x": grid.axis_max(0) + 1, "y": y, "ox": -1, "oy": 0}
        for x in grid.x_range():
            yield {"x": x, "y": -1, "ox": 0, "oy": 1}
            yield {"x": x, "y": grid.axis_max(1) + 1, "ox": 0, "oy": -1}

    best = 0
    history = {}

    if draw:
        cell_size = 50
        frame = 0

    for first_node in get_starts():
        first_node["seen"] = set()
        first_node["energy"] = set()
        first_node["step"] = -1
        first_node["first"] = True

        energy = set()

        max_x = grid.axis_max(0)
        max_y = grid.axis_max(1)
        mirrors = {}
        for pt, val in grid.grid.items():
            if val in "-|\\/":
                mirrors[pt] = val

        todo = deque()
        todo.append(first_node)
        add_history = {}

        last_step = -1
        lights = []

        if draw:
            for _ in range(10):
                draw_frame(grid, energy, cell_size, lights, mirrors, frame)
                frame += 1
        while len(todo) > 0:
            node = todo.popleft()

            if node['step'] == 50 and add_history is not None:
                if (node['x'], node['y'], node['ox'], node['oy']) not in add_history:
                    node['seen'] = set()
                    node['energy'] = set()
                    add_history[(node['x'], node['y'], node['ox'], node['oy'])] = (node['energy'], node['seen'])

            if node['first']:
                node['first'] = False
            else:
                energy.add((node['x'], node['y']))
                node['energy'].add((node['x'], node['y']))

            if draw:
                if node['step'] != last_step:
                    last_step = node['step']
                    draw_frame(grid, energy, cell_size, lights, mirrors, frame)
                    frame += 1

            while True:
                if draw:
                    light = {
                        "x1": node['x'], 
                        "y1": node['y'],
                        "x2": node['x'] + node['ox'],
                        "y2": node['y'] + node['oy'],
                        "age": 0,
                    }
                node['x'], node['y'] = node['x'] + node['ox'], node['y'] + node['oy']
                temp = history.get((node['x'], node['y'], node['ox'], node['oy']), None)
                if temp is not None:
                    energy.update(temp[0])
                    node['energy'].update(temp[0])
                    node['seen'].update(temp[1])
                    break

                if 0 <= node['x'] <= max_x and 0 <= node['y'] <= max_y:
                    val = mirrors.get((node['x'], node['y']), "")
                    if (val == "|" and node['oy'] == 0) or (val == "-" and node['ox'] == 0):
                        if draw:
                            light = light.copy()
                            light["x3"] = light["x2"] + abs(node['oy'])
                            light["y3"] = light["y2"] + abs(node['ox'])
                            lights.append(light)
                            light = light.copy()
                            light["x3"] = light["x2"] + -abs(node['oy'])
                            light["y3"] = light["y2"] + -abs(node['ox'])
                            lights.append(light)
                        add_if_new(node, todo, abs(node['oy']), abs(node['ox']))
                        add_if_new(node, todo, -abs(node['oy']), -abs(node['ox']))
                        break
                    else:
                        if val == "/":
                            if draw:
                                light["x3"] = light["x2"] + -node['oy']
                                light["y3"] = light["y2"] + -node['ox']
                                lights.append(light)
                            add_if_new(node, todo, -node['oy'], -node['ox'])
                            break
                        elif val == "\\":
                            if draw:
                                light["x3"] = light["x2"] + node['oy']
                                light["y3"] = light["y2"] + node['ox']
                                lights.append(light)
                            add_if_new(node, todo, node['oy'], node['ox'])
                            break
                        else:
                            if draw:
                                light["x3"] = light["x2"] + node['ox']
                                light["y3"] = light["y2"] + node['oy']
                                lights.append(light)
                            add_if_new(node, todo, node['ox'], node['oy'])
                            break
                else:
                    break 

        if add_history is not None:
            history |= add_history
        best = max(best, len(energy))

    if draw:
        for i in range(10):
            draw_frame(grid, energy, cell_size, lights, mirrors, frame)
            frame += 1

    return best

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    avalues = [
        r".|...\....",
        r"|.-.\.....",
        r".....|-...",
        r"........|.",
        r"..........",
        r"........." + "\\",
        r"..../.\\..",
        r".-.-/..|..",
        r".|....-|." + "\\",
        r"..//.|....",
    ]
    init_draw()
    calc(DummyLog(), values, 1, draw=True)
    finish_draw()
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def test(log):
    values = log.decode_values(r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
    """)

    log.test(calc(log, values, 1), '46')
    log.test(calc(log, values, 2), '51')

    values = log.decode_values(r"""
        .....
        ./-\.
        .|.|.
        .\-/.
        .....
    """)
    log.test(calc(log, values, 2), '9')

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

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

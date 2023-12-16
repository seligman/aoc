#!/usr/bin/env python3

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

def calc(log, values, mode):
    from grid import Grid, Point
    from collections import deque
    grid = Grid.from_text(values)

    def get_starts():
        for y in grid.y_range():
            yield {"x": 0, "y": y, "ox": 1, "oy": 0}
            if mode == 1: return
            yield {"x": grid.axis_max(0), "y": y, "ox": -1, "oy": 0}
        for x in grid.x_range():
            yield {"x": x, "y": 0, "ox": 0, "oy": 1}
            yield {"x": x, "y": grid.axis_max(1), "ox": 0, "oy": -1}

    best = 0
    history = {}

    for first_node in get_starts():
        first_node["seen"] = set()
        first_node["energy"] = set()
        first_node["step"] = 0

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

        while len(todo) > 0:
            node = todo.popleft()
            # print(node['step'])
            if node['step'] == 50 and add_history is not None:
                if (node['x'], node['y'], node['ox'], node['oy']) not in add_history:
                    node['seen'] = set()
                    node['energy'] = set()
                    add_history[(node['x'], node['y'], node['ox'], node['oy'])] = (node['energy'], node['seen'])

            energy.add((node['x'], node['y']))
            node['energy'].add((node['x'], node['y']))
            while True:
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
                        add_if_new(node, todo, abs(node['oy']), abs(node['ox']))
                        add_if_new(node, todo, -abs(node['oy']), -abs(node['ox']))
                        break
                    else:
                        if val == "/":
                            add_if_new(node, todo, -node['oy'], -node['ox'])
                            break
                        elif val == "\\":
                            add_if_new(node, todo, node['oy'], node['ox'])
                            break
                        else:
                            add_if_new(node, todo, node['ox'], node['oy'])
                            break
                else:
                    break 

        if add_history is not None:
            history |= add_history
        best = max(best, len(energy))

    return best

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
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

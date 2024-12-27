#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Cryostasis'

from collections import deque, defaultdict
from hashlib import sha256
import textwrap

def get_out(prog, end_at_nl=False):
    l = ""
    while len(prog.output) > 0:
        l += chr(prog.get_output())
        if end_at_nl and l[-1] == "\n":
            break
    return l

def add_in(prog, val):
    for cur in val + "\n":
        prog.add_to_input(ord(cur))

def create_id(value):
    return sha256(value.encode("utf-8")).hexdigest()[:10]

def get_path(cur_room, dest_room, paths):
    todo = deque()
    seen = set([])
    todo.append([cur_room, []])

    while len(todo) > 0:
        room, path = todo.pop()
        if room not in seen:
            seen.add(room)
            if room == dest_room:
                return path
            else:
                for direction, other_room in paths[room]:
                    todo.append((other_room, path + [direction]))

def wrap_line(log, val):
    for row in textwrap.wrap(val, 78, subsequent_indent=" " * 5):
        log(row)

def calc(log, values):
    from program import Program
    prog = Program.from_values(values, log)

    todo = deque()
    prog.tick_till_end()
    todo.appendleft((prog.make_copy(), [], None, ""))
    start_prog = prog.make_copy()
    start_room = None
    final_room = None
    seen = set()
    rooms = {}
    paths = defaultdict(list)
    while len(todo) > 0:
        prog, path, source_room, in_direction = todo.pop()
        room = get_out(prog)
        room = "\n".join(x for x in room.split("\n") if len(x.strip()))

        if create_id(room) not in seen:
            if source_room is not None:
                rooms[source_room]["targets"][in_direction] = create_id(room)
            seen.add(create_id(room))
            info = {
                "name": None,
                "exits": [],
                "targets": {},
                "items": [],
                "room": room,
                "path": path,
                "start": source_room is None,
                "end": False,
            }
            if source_room is None:
                start_room = create_id(room)

            if source_room is not None:
                paths[source_room].append((in_direction, create_id(room)))
                rev = {"north": "south", "south": "north", "west": "east", "east": "west"}[in_direction]
                paths[create_id(room)].append((rev, source_room))

            rooms[create_id(room)] = info
            skip = 0
            target = None

            for row in room.split("\n"):
                if skip > 0:
                    skip -= 1
                elif row.startswith("="):
                    info["name"] = row.strip("= ")
                    skip += 1
                elif row.startswith("Doors here lead"):
                    target = info['exits']
                elif row.startswith("Items here"):
                    target = info['items']
                elif row.startswith("- "):
                    target.append(row[2:])
                elif row == "Command?":
                    pass
                elif row.startswith("A loud, robotic voice"):
                    final_room = create_id(room)
                    info['exits'] = []
                    info['end'] = True
                    break
                else:
                    raise Exception(row)

            temp = prog.make_copy()
            for cur in info['exits']:
                prog = temp.make_copy()
                add_in(prog, cur)
                prog.tick_till_end()
                todo.append((prog.make_copy(), path + [cur], create_id(room), cur))

    log("-- Map of rooms --")
    from grid import Grid
    grid = Grid(default=" ")
    todo = deque([(start_room, 0, 0)])
    seen = set()
    while len(todo) > 0:
        room, x, y = todo.pop()
        if room not in seen:
            if room == start_room:
                grid.set("S", x, y)
            elif room == final_room:
                grid.set("E", x, y)
            else:
                grid.set("#", x, y)

            seen.add(room)
            for direction, dest_room in paths[room]:
                ox, oy, size, disp = {
                    "north": (0, -1, 2, "|"),
                    "south": (0, 1, 2, "|"),
                    "west": (-1, 0, 5, "-"),
                    "east": (1, 0, 5, "-"),
                }[direction]
                for i in range(1, size):
                    grid.set(disp, x + ox * i, y + oy * i)
                todo.append((dest_room, x + ox * size, y + oy * size))

    grid.show_grid(log, disp_map={x: x for x in "- #|SE"})

    log("")
    log("-- Items --")

    valid = set()
    invalid = set()
    for room in rooms:
        for item in rooms[room]['items']:
            prog = start_prog.make_copy()
            for step in rooms[room]['path']:
                add_in(prog, step)
            add_in(prog, "take " + item)
            add_in(prog, "inv")
            prog.tick_till_end(bail=100000)
            test = get_out(prog)
            if f"Items in your inventory:\n- {item}\n" in test:
                valid.add((room, item))
            else:
                invalid.add((room, item))

    for desc, target in (("Valid", valid), ("Invalid", invalid)):
        wrap_line(log, desc + " items: " + ", ".join(sorted(x[1] for x in target)))

    log("")
    log("-- Final Path --")

    todo = deque()
    for room, item in valid:
        todo.append([(room, item)])

    used_groups = set()
    while len(todo) > 0:
        source_items = todo.popleft()
        just_items = list(x[1] for x in source_items)
        if tuple(sorted(just_items)) not in used_groups:
            used_groups.add(tuple(sorted(just_items)))
            steps = []
            cur_room = start_room
            left = [x for x in source_items]
            while len(left) > 0:
                left = [(x[0], x[1], get_path(cur_room, x[0], paths)) for x in left]
                left.sort(key=lambda x: (len(x[2]), x[0]))
                room, item, path = left.pop(0)
                steps += path
                steps.append("take " + item)
                cur_room = room
            temp = get_path(cur_room, final_room, paths)
            steps += temp[:-1]
            final_step = temp[-1]

            prog = start_prog.make_copy()
            for step in steps:
                add_in(prog, step)
                prog.tick_till_end()
                prog.output.clear()

            add_in(prog, "inv")
            add_in(prog, final_step)
            prog.tick_till_end()
            final_text = get_out(prog)
            if "Droids on this ship are heavier" in final_text:
                already_used = set(x[1] for x in source_items)
                for room, item in valid:
                    if item not in already_used:
                        todo.append(source_items + [(room, item)])
            elif "Alert! Droids on this ship are lighter" in final_text:
                pass
            elif "Analysis complete! You may proceed" in final_text:
                wrap_line(log, "Items: " + ", ".join(sorted(just_items)))
                wrap_line(log, "Path: " + ", ".join(steps + [final_step]))
                temp = [x for x in final_text.split("\n") if len(x)][-1]
                wrap_line(log, "Final Message: " + temp)
                return ""

def test(log):
    return True

def run(log, values):
    calc(log, values)

def other_interactive(describe, values):
    if describe:
        return "Interactive version"
    class DummyLog:
        def show(self, value):
            print(value)
        def __call__(self, value):
            print(value)
    log = DummyLog()

    from program import Program
    prog = Program.from_values(values, log)
    while True:
        while True:
            hit_end = prog.tick_till_end(bail=1000)
            while True:
                row = get_out(prog, end_at_nl=True)
                if len(row) == 0:
                    break
                print(row, end="", flush=True)
            if hit_end:
                break
        val = input("> ")
        if len(val) == 0:
            exit(0)
        for cur in val.split(","):
            print(cur.strip())
            add_in(prog, cur.strip())

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    if "interactive" in sys.argv[1:]:
        other_interactive(False, values)
    else:
        run(print, values)

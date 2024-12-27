#!/usr/bin/env python3

DAY_NUM = 25
DAY_DESC = 'Day 25: Cryostasis'


def calc(log, values):
    from program import Program
    prog = Program.from_values(values, log)

    def get_out(prog):
        l = ""
        while len(prog.output) > 0:
            l += chr(prog.get_output())
        return l

    def add_in(prog, val):
        for cur in val + "\n":
            prog.add_to_input(ord(cur))

    from collections import deque
    todo = deque()
    prog.tick_till_end()
    todo.appendleft((prog.make_copy(), [], ""))
    start_prog = prog.make_copy()
    final_room = None
    seen = set()
    rooms = {}
    while len(todo) > 0:
        prog, path, in_data = todo.pop()
        room = get_out(prog)
        room = "\n".join(x for x in room.split("\n") if len(x.strip()))

        if room not in seen:
            seen.add(room)
            skip = 0
            target = None
            exits = []
            items = []
            name = ""

            for row in room.split("\n"):
                if skip > 0:
                    skip -= 1
                elif row.startswith("="):
                    name = row.strip("= ")
                    skip += 1
                elif row.startswith("Doors here lead"):
                    target = exits
                elif row.startswith("Items here"):
                    target = items
                elif row.startswith("- "):
                    target.append(row[2:])
                elif row == "Command?":
                    pass
                elif row.startswith("A loud, robotic voice"):
                    final_room = room
                    exits = []
                    break
                else:
                    raise Exception(row)

            rooms[room] = {
                "name": name,
                "exits": exits,
                "path": path,
                "items": items,
                "room": room,
            }
            log("Found room: " + name + ", with " + str(len(items)) + " items")

            temp = prog.make_copy()
            for cur in exits:
                prog = temp.make_copy()
                add_in(prog, cur)
                prog.tick_till_end()
                todo.append((prog.make_copy(), path + [cur], cur))

    valid = set()
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
                log(item + " in room " + rooms[room]['name'] + " is valid")
                valid.add((room, item))

    tried = set()
    todo = deque([([], start_prog.make_copy())])
    valid = list(valid)
    try_number = 0
    while len(todo) > 0:
        items, cur_prog = todo.popleft()
        try_number += 1
        if try_number % 5 == 0:
            print("Trying " + ", ".join(items))
        prog = cur_prog.make_copy()
        for cur in rooms[final_room]['path'][:-1]:
            add_in(prog, cur)
        prog.tick_till_end()
        get_out(prog)
        add_in(prog, rooms[final_room]['path'][-1])
        prog.tick_till_end()
        final_text = get_out(prog)

        if "Droids on this ship are heavier" in final_text:
            for room, item in valid:
                if item not in items:
                    key = tuple(sorted(items + [item]))
                    if key not in tried:
                        tried.add(key)
                        prog = cur_prog.make_copy()
                        for cur in rooms[room]['path']:
                            add_in(prog, cur)
                        add_in(prog, "take " + item)
                        for cur in rooms[room]['path'][::-1]:
                            add_in(prog, {"west": "east", "east": "west", "north": "south", "south": "north"}[cur])
                        prog.tick_till_end()
                        get_out(prog)
                        todo.append((items + [item], prog))
        elif "Alert! Droids on this ship are lighter" in final_text:
            pass
        elif "Analysis complete! You may proceed" in final_text:
            log(final_text)
            return ""
        else:
            raise Exception(final_text)


def test(log):
    return True

def run(log, values):
    calc(log, values)

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
    run(print, values)

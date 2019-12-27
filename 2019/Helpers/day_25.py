#!/usr/bin/env python

def get_desc():
    return 25, 'Day 25: Cryostasis'


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

    prog.tick_till_end()
    seen = set()
    final = None
    items = []
    seen.add(get_out(prog))

    from collections import deque
    todo = deque()
    todo.appendleft((prog.ticker.copy(), []))
    while len(todo) > 0:
        ticker, trail = todo.pop()
        for d in ["east", "west", "north", "south"]:
            prog.ticker = ticker.copy()
            add_in(prog, d)
            prog.tick_till_end()
            room = get_out(prog)
            if room not in seen:
                seen.add(room)
                if "Items here:" in room:
                    item_name = None
                    for cur in room.split("\n"):
                        if cur == "Items here:":
                            item_name = "--"
                        elif item_name == "--":
                            item_name = cur[2:]
                    items.append([False, item_name, trail + [d]])
                elif "next" in room:
                    if final is None:
                        final = [trail + [d], room]
                todo.appendleft((prog.ticker.copy(), trail + [d]))

    for i in range(len(items)):
        prog = Program.from_values(values, log)
        for cur in items[i][2]:
            add_in(prog, cur)
        prog.tick_till_end()
        get_out(prog)
        add_in(prog, "take " + items[i][1])
        add_in(prog, "inv")
        bail = 10000
        while prog.flag_running and bail > 0:
            bail -= 1
            prog.tick()
        if "Items in your inventory:\n- " + items[i][1] in get_out(prog):
            items[i][0] = True
        log.show("Item: %s is %s" % (items[i][1], "valid" if items[i][0] else "invalid"))

    items = [x for x in items if x[0]]

    found_doors = False
    for cur in final[1].split("\n"):
        if cur == "Doors here lead:":
            found_doors = True
        elif found_doors:
            if cur[2:] != final[0][-1]:
                final[0].append(cur[2:])
                break

    import itertools
    rev = {
        "west": "east",
        "east": "west",
        "north": "south",
        "south": "north",
    }

    prog = Program.from_values(values, log)
    for item in items:
        for path in item[2]:
            add_in(prog, path)
        add_in(prog, "take " + item[1])
        for path in item[2][::-1]:
            add_in(prog, rev[path])
    for path in final[0][:-1]:
        add_in(prog, path)
    for item in items:
        add_in(prog, "drop " + item[1])
    prog.tick_till_end()
    get_out(prog)

    ticker = prog.ticker.copy()
    results = None

    for test_len in range(1, len(items)):
        for cur in itertools.combinations(items, test_len):
            prog.ticker = ticker.copy()
            for item in cur:
                add_in(prog, "take " + item[1])
            prog.tick_till_end()
            get_out(prog)
            add_in(prog, final[0][-1])
            prog.tick_till_end()
            results = get_out(prog)

            if "keypad" in results:
                log.show("-- Items --")
                for item in cur:
                    log.show(item[1])
                log.show("-- Room --")
                log.show(results)
                break
            else:
                results = None
        if results is not None:
            break


def test(log):
    return True


def run(log, values):
    calc(log, values)

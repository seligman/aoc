#!/usr/bin/env python3

DAY_NUM = 20
DAY_DESC = 'Day 20: Pulse Propagation'

def calc(log, values, mode):
    mods = {}
    for row in values:
        row = row.split(" -> ")
        temp = {"dest": row[1].split(", "), "id": row[0][1:]}

        if row[0] == "broadcaster":
            temp["type"] = "broad"
            head = temp
        elif row[0].startswith("%"):
            temp["type"] = "flip"
            temp["state"] = "off"
        elif row[0].startswith("&"):
            temp["type"] = "con"
            temp["vals"] = {}
        else:
            raise Exception("Invalid input")
        mods[temp["id"]] = temp

    mods["output"] = {"type": "output", "id": "output", "high": 0, "low": 0, "dest": []}
    mods["rx"] = {"type": "special", "id": "rx", "dest": []}

    # Create a reverse lookup map
    lookup = {}
    for cur in mods.values():
        for other in cur["dest"]:
            if other not in lookup:
                lookup[other] = []
            lookup[other].append(cur['id'])
    
    # Make sure the con modules start in a proper state
    for cur in lookup:
        if mods[cur]["type"] == "con":
            mods[cur]["vals"] = {x: "low" for x in lookup[cur]}

    tot = {"high": 0, "low": 0}

    if mode == 2:
        if len(lookup["rx"]) != 1:
            raise Exception("more than one dest") # If there's more than one input, then yeah, good luck
        before_rx = mods[lookup["rx"][0]]
        if before_rx["type"] != "con":
            raise Exception("unexpected input to rx") # If this is some other type, this logic breaks down
        cycles = {x: [] for x in lookup[before_rx["id"]]}

    presses = 0
    while True:
        todo = [("low", head, {"id": "--"})]
        while len(todo):
            pulse, cur, source = todo.pop(0)
            tot[pulse] += 1

            if mode == 2:
                if source["id"] in cycles and pulse == "high":
                    cycles[source["id"]].append(presses)
                    if all(len(x) >= 2 for x in cycles.values()):
                        temp = [x[1] - x[0] for x in cycles.values()]
                        import math
                        return math.lcm(*temp)

            if cur["type"] == "flip":
                if pulse == "low":
                    cur["state"] = "off" if cur["state"] == "on" else "on"
                    for dest in cur["dest"]:
                        todo.append(("high" if cur["state"] == "on" else "low", mods[dest], cur))
            elif cur["type"] == "con":
                cur["vals"][source["id"]] = pulse
                if set(cur["vals"].values()) == {"high"}:
                    pulse = "low"
                else:
                    pulse = "high"
                for dest in cur["dest"]:
                    todo.append((pulse, mods[dest], cur))
            elif cur["type"] == "output":
                cur["out"] = pulse
                cur[pulse] += 1
            elif cur["type"] == "broad":
                for dest in cur["dest"]:
                    todo.append((pulse, mods[dest], cur))
        presses += 1
        if mode == 1 and presses == 1000:
            break

    return tot['high'] * tot['low']

def test(log):
    values = log.decode_values("""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
    """)

    log.test(calc(log, values, 1), '32000000')

    values = log.decode_values("""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
    """)

    log.test(calc(log, values, 1), '11687500')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

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

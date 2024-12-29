#!/usr/bin/env python3

import re

DAY_NUM = 14
DAY_DESC = 'Day 14: Reindeer Olympics'

class Deer:
    def __init__(self, name, speed, limit, rest):
        self.name = name
        self.speed = int(speed)
        self.limit = int(limit)
        self.rest = int(rest)
        self.state = "fly"
        self.left = self.limit
        self.distance = 0
        self.points = 0

def calc(log, values, secs):
    r = re.compile("(.*) can fly (.*) km/s for (.*) seconds, but then must rest for (.*) seconds.")

    deers = []
    for cur in values:
        m = r.search(cur)
        deers.append(Deer(*m.groups()))

    while secs > 0:
        secs -= 1
        for deer in deers:
            deer.left -= 1
            if deer.state == "fly":
                deer.distance += deer.speed
            if deer.left == 0:
                if deer.state == "fly":
                    deer.state = "rest"
                    deer.left = deer.rest
                else:
                    deer.state = "fly"
                    deer.left = deer.limit
        lead = max([x.distance for x in deers])
        for deer in deers:
            if deer.distance == lead:
                deer.points += 1

    log("Part 2: %d" % (max([x.points for x in deers]),))

    return max([x.distance for x in deers])

def test(log):
    values = [
        "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
        "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
    ]

    if calc(log, values, 1000) == 1120:
        return True
    else:
        return False

def run(log, values):
    log("Part 1: %d" % (calc(log, values, 2503),))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2015/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

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
    __slots__ = ['a', 'b', 'opened', 'pressure']
    def __init__(self, a, b, opened, pressure):
        self.a = a
        self.b = b
        self.opened = opened
        self.pressure = pressure

    def __repr__(self):
        return f"{self.a}-{self.b},{self.opened},{self.pressure}"

def calc(log, values, mode):
    next_valve_num = [0]
    nodes = {x.node_name: x for x in [Node(y, next_valve_num) for y in values]}
    first = min(nodes.keys())

    best = {}
    target_best = 0

    def is_best(val):
        if val.pressure < target_best:
            return False

        key = (val.a, val.b, val.opened)

        if key not in best or val.pressure > best[key]:
            best[key] = val.pressure
            return True
            
        return False

    best_history = []
    total_time = 30 if mode == 1 else 26
    states = deque([State(first, None if mode == 1 else first, 0, 0)])

    for time in range(1, total_time + 1):
        best_history.append(0 if len(best) == 0 else max(best.values()))
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
                    )
                    if is_best(val): next_states.append(val)
                for y in [None] if node_b is None else node_b.tunnels:
                    val = State(node_a.node_name, y, cur.opened | node_a.valve_num, cur.pressure + node_a.rate * (total_time - time))
                    if is_best(val): next_states.append(val)
            for x in node_a.tunnels:
                if node_b is not None and node_b.rate > 0 and (node_b.valve_num & cur.opened) == 0:
                    val = State(x, node_b.node_name, cur.opened | node_b.valve_num, cur.pressure + node_b.rate * (total_time - time))
                    if is_best(val): next_states.append(val)
                for y in [None] if node_b is None else node_b.tunnels:
                    val = State(x, y, cur.opened, cur.pressure)
                    if is_best(val): next_states.append(val)
        states = next_states

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

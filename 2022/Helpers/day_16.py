#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Proboscidea Volcanium'

def calc(log, values, mode):
    import re
    first = None
    nodes = {}
    for row in values:
        m = re.search("Valve (.*?) has flow rate=(.*?)\\; tunnels? leads? to valves? (.*?)$", row)
        node, rate, tunnels = m.groups()
        tunnels = tunnels.split(", ")
        rate = int(rate)
        if first is None or node < first:
            first = node
        nodes[node] = {
            "rate": rate,
            "node": node,
            "tunnels": tunnels,
            "opened": False,
        }

    from collections import defaultdict
    best = defaultdict(lambda:-1)

    if mode == 1:
        states = [(first, set(), 0)]
        for time in range(1, 31):
            temp = []
            for node, opened, pressure in states:
                key = (node,) + tuple(sorted(opened))
                if pressure > best[key]:
                    best[key] = pressure
                    node = nodes[node]
                    if node['rate'] > 0 and node['node'] not in opened:
                        temp.append((node['node'], opened | set([node['node']]), pressure + node['rate'] * (30 - time)))
                    for x in node['tunnels']:
                        temp.append((x, opened, pressure))
            states = temp
    else:
        seen = {}
        m = 0

        def recurse(t, pos1, pos2, flow):
            nonlocal m
            
            if seen.get((t, pos1, pos2), -1) >= sum(flow):
                return
            seen[t, pos1, pos2] = sum(flow)
            
            if t == 26:
                if sum(flow) > m:
                    m = sum(flow)
                return
            
            if all(x['opened'] for x in nodes.values() if x['rate'] > 0):
                tf = sum(x['rate'] for x in nodes.values() if x['opened'])
                recurse(t + 1, pos1, pos2, flow + [tf])
                return
            
            for k in (0, 1):
                if k == 0:
                    if nodes[pos1]['opened'] or nodes[pos1]['rate'] <= 0:
                        continue
                        
                    nodes[pos1]['opened'] = True
                    
                    for k2 in (0, 1):
                        if k2 == 0:
                            if nodes[pos2]['opened'] or nodes[pos2]['rate'] <= 0:
                                continue
                            
                            nodes[pos2]['opened'] = True
                            j = sum(x['rate'] for x in nodes.values() if x['opened'])
                            recurse(t + 1, pos1, pos2, flow + [ j ])
                            nodes[pos2]['opened'] = False
                        else:
                            j = sum(x['rate'] for x in nodes.values() if x['opened'])
                            for v2 in nodes[pos2]['tunnels']:
                                recurse(t + 1, pos1, v2, flow + [ j ])
                    nodes[pos1]['opened'] = False
                else:
                    j = sum(x['rate'] for x in nodes.values() if x['opened'])
                    for v in nodes[pos1]['tunnels']:
                        for k2 in (0, 1):
                            if k2 == 0:
                                if nodes[pos2]['opened'] or nodes[pos2]['rate'] <= 0:
                                    continue

                                nodes[pos2]['opened'] = True
                                j = sum(x['rate'] for x in nodes.values() if x['opened'])
                                recurse(t + 1, v, pos2, flow + [ j ])
                                nodes[pos2]['opened'] = False
                            else:
                                j = sum(x['rate'] for x in nodes.values() if x['opened'])
                                for v2 in nodes[pos2]['tunnels']:
                                    recurse(t + 1, v, v2, flow + [ j ])

        recurse(1, first, first, [ 0 ])

        return m

    return max(x for x in best.values())

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

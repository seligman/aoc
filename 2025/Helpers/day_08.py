#!/usr/bin/env python3

DAY_NUM = 8
DAY_DESC = 'Day 8: Playground'

def calc(log, values, mode, num_paths=10):
    points = []
    for row in values:
        row = [int(x) for x in row.split(",")]
        points.append({
            "x": row[0],
            "y": row[1],
            "z": row[2],
            "set": None,
            "i": len(points),
        })

    import math
    import itertools
    from collections import defaultdict
    connected = []
    paths = defaultdict(list)
    for a, b in itertools.combinations(points, 2):
        dist = math.sqrt (((a['x'] - b['x']) ** 2) + ((a['y'] - b['y']) ** 2) + ((a['z'] - b['z']) ** 2))
        connected.append([dist, a, b])
    connected.sort(key=lambda x: x[0])

    if mode == 2:
        used = set()
        for _, a, b in connected:
            used.add(a['i'])
            used.add(b['i'])
            if len(used) == len(points):
                return a['x'] * b['x']

    for _, a, b in connected[:num_paths]:
        paths[a['i']].append(b['i'])
        paths[b['i']].append(a['i'])

    cur_set = 1
    made = 0

    for _, a, b in connected[:num_paths]:
        if a['set'] is None:
            todo = [a['i']]
            used = set()
            while len(todo):
                x = todo.pop(0)
                # print(cur_set, x)
                if x not in used:
                    used.add(x)
                    points[x]['set'] = cur_set
                    todo.extend(paths[x])
            cur_set += 1

    from collections import defaultdict
    totals = defaultdict(int)
    for cur in points:
        if cur['set'] is not None:
            totals[cur['set']] += 1
    
    totals = list(totals.values())
    totals.sort(reverse=True)
    totals = totals[:3]
    ret = 1
    for val in totals:
        ret *= val
    return ret

def test(log):
    values = log.decode_values("""
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
    """)

    log.test(calc(log, values, 1, 10), '40')
    log.test(calc(log, values, 2), '25272')

def run(log, values):
    log("Part 1")
    log(calc(log, values, 1, 1000))
    log("Part 2")
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

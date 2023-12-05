#!/usr/bin/env python3

import re

DAY_NUM = 5
DAY_DESC = 'Day 5: If You Give A Seed A Fertilizer'

def calc(log, values, mode):
    seeds = list(map(int, values[0].split(": ")[1].split(" ")))
    all_maps = {}
    for row in values[2:] + [""]:
        m = re.search("([a-z]+)-to-([a-z]+) map:", row)
        if m is not None:
            source_type, dest_type = m.group(1), m.group(2)
            maps = []
        m = re.search("([0-9]+) ([0-9]+) ([0-9]+)", row)
        if m is not None:
            dest, source, count = int(m.group(1)), int(m.group(2)), int(m.group(3))
            maps.append((dest - source, source, source + count - 1))
        if len(row) == 0:
            all_maps[source_type] = {
                "target": dest_type,
                "maps": maps,
            }

    ret = None

    if mode == 1:
        seeds = [(x, x) for x in seeds]
    else:
        seeds = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]

    pos = "seed"
    while pos in all_maps:
        next_seeds = []
        temp = all_maps[pos]
        pos = temp["target"]
        while len(seeds) > 0:
            a, b = seeds.pop(0)
            found = False
            for offset, c, d in temp["maps"]:
                if c <= a <= d and c <= b <= d:
                    next_seeds.append((a + offset, b + offset))
                    found = True
                    break
                elif c <= a <= d:
                    next_seeds.append((a + offset, d + offset))
                    seeds.append((d + 1, b))
                    found = True
                    break
                elif c <= b <= d:
                    seeds.append((a, c - 1))
                    next_seeds.append((c + offset, b + offset))
                    found = True
                    break
                elif a < c and b > d:
                    seeds.append((d + 1, b))
                    seeds.append((a, c - 1))
                    next_seeds.append((c + offset, d + offset))
                    found = True
                    break
            if not found:
                next_seeds.append((a, b))
        seeds = next_seeds

    ret = min(x[0] for x in seeds)
    return ret

def test(log):
    values = log.decode_values("""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
    """)

    log.test(calc(log, values, 1), '35')
    log.test(calc(log, values, 2), '46')

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

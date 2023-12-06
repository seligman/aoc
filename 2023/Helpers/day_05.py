#!/usr/bin/env python3

import re

DAY_NUM = 5
DAY_DESC = 'Day 5: If You Give A Seed A Fertilizer'

def intersect(target_start, target_end, test_start, test_end):
    # Check to see if 'test' intersects with 'target', break up results as needed
    # Return is_inside, part_start, part_end for each segment
    target_start, target_end = min(target_start, target_end), max(target_start, target_end)
    test_start, test_end = min(test_start, test_end), max(test_start, test_end)

    if target_start <= test_start <= target_end and target_start <= test_end <= target_end:
        yield True, test_start, test_end
    elif target_start <= test_start <= target_end:
        yield True, test_start, target_end
        yield False, target_end + 1, test_end
    elif target_start <= test_end <= target_end:
        yield False, test_start, target_start - 1
        yield True, target_start, test_end
    elif test_start < target_start and test_end > target_end:
        yield False, test_start, target_start - 1
        yield True, target_start, target_end
        yield False, target_end + 1, test_end

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
            seed_start, seed_end = seeds.pop(0)
            found = False
            for offset, target_start, target_end in temp["maps"]:
                for is_inside, part_start, part_end in intersect(target_start, target_end, seed_start, seed_end):
                    found = True
                    if is_inside:
                        next_seeds.append((part_start + offset, part_end + offset))
                    else:
                        seeds.append((part_start, part_end))
                if found:
                    break
            if not found:
                next_seeds.append((seed_start, seed_end))
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

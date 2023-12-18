#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Lavaduct Lagoon'

def poly_area(poly):
    area = 0.0
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]
    area = abs(area) / 2.0
    return area

def calc(log, values, mode):
    lines = [(0, 0)]
    x, y = 0, 0
    line_len = 0
    for row in values:
        row = row.split(' ')
        if mode == 1:
            ox, oy = {
                "R": (1, 0),
                "D": (0, 1),
                "L": (-1, 0),
                "U": (0, -1),
            }[row[0]]
            l = int(row[1])
        else:
            ox, oy = {
                "0": (1, 0),
                "1": (0, 1),
                "2": (-1, 0),
                "3": (0, -1),
            }[row[2][-2]]
            l = int(row[2][2:7], 16)
        x, y = x + ox * l, y + oy * l
        lines.append((x, y))
        line_len += l

    return int(poly_area(lines) + line_len // 2 + 1)

def test(log):
    values = log.decode_values("""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
    """)

    log.test(calc(log, values, 1), '62')
    log.test(calc(log, values, 2), '952408144115')

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

#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Never Tell Me The Odds'

def calc(log, values, mode, lower, upper):
    import itertools

    hail = []
    for row in values:
        row = row.split(" @ ")
        pos = [int(x.strip()) for x in row[0].split(",")]
        vel = [int(x.strip()) for x in row[1].split(",")]
        hail.append(pos + vel)

    if mode == 1:
        ret = 0
        import numpy as np
        for (x1, y1, z1, vx1, vy1, vz1), (x2, y2, z2, vx2, vy2, vz2) in itertools.combinations(hail, 2):
            m1, m2 = vy1 / vx1, vy2 / vx2
            if m1 == m2:
                continue
            A = np.array([[m1, -1], [m2, -1]])
            b = np.array([m1 * x1 - y1, m2 * x2 - y2])
            x, y = np.linalg.solve(A, b)
            if not (lower <= x <= upper and lower <= y <= upper):
                continue
            t1 = (x - x1) / vx1
            t2 = (x - x2) / vx2
            if t1 > 0 and t2 > 0:
                ret += 1
        return ret
    else:
        from z3 import BitVec, Solver, sat
        solver = Solver()
        x, y, z, vx, vy, vz = (BitVec(name, 64) for name in ('x', 'y', 'z', 'vx', 'vy', 'vz'))
        for i, (a, b, c, va, vb, vc) in enumerate(hail[:10]):
            t = BitVec(f"t{i}", 64)
            solver.add(t > 0)
            solver.add(x + vx * t == a + va * t)
            solver.add(y + vy * t == b + vb * t)
            solver.add(z + vz * t == c + vc * t)
        if solver.check() == sat:
            m = solver.model()
            return sum(m.eval(var).as_long() for var in (x, y, z))

def test(log):
    values = log.decode_values("""
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
    """)

    log.test(calc(log, values, 1, 7, 27), '2')
    log.test(calc(log, values, 2, 0, 0), '47')

def run(log, values):
    log(calc(log, values, 1, 200000000000000, 400000000000000))
    log(calc(log, values, 2, 0, 0))

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

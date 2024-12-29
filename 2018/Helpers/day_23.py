#!/usr/bin/env python3

import re
from collections import deque

DAY_NUM = 23
DAY_DESC = 'Day 23: Experimental Emergency Teleportation'

def get_bots(log, values):
    r = re.compile("pos=<([0-9-]+),([0-9-]+),([0-9-]+)>, r=([0-9]+)")
    bots = []
    for cur in values:
        if cur.startswith("#"):
            log("# Note: " + cur)
        else:
            m = r.search(cur)
            if m is None:
                log(cur)
            bots.append([int(x) for x in m.groups()])
    return bots

def calc(log, values):
    bots = get_bots(log, values)
    best_i = None
    best_val = None
    for i in range(len(bots)):
        if best_i is None or bots[i][3] > best_val:
            best_val = bots[i][3]
            best_i = i

    bx, by, bz, bdist = bots[best_i]

    ret = 0

    for i in range(len(bots)):
        x, y, z, _dist = bots[i]

        if abs(x - bx) + abs(y - by) + abs(z - bz) <= bdist:
            ret += 1

    return ret

def find(done, bots, xs, ys, zs, dist, ox, oy, oz, forced_count):
    at_target = []

    for x in range(min(xs), max(xs)+1, dist):
        for y in range(min(ys), max(ys)+1, dist):
            for z in range(min(zs), max(zs)+1, dist):

                # See how many bots are possible
                count = 0
                for bx, by, bz, bdist in bots:
                    if dist == 1:
                        calc = abs(x - bx) + abs(y - by) + abs(z - bz)
                        if calc <= bdist:
                            count += 1
                    else:
                        calc =  abs((ox+x) - (ox+bx))
                        calc += abs((oy+y) - (oy+by))
                        calc += abs((oz+z) - (oz+bz))
                        # The minus three is to include the current box 
                        # in any bots that are near it
                        if calc //dist - 3 <= (bdist) // dist:
                            count += 1

                if count >= forced_count:
                    at_target.append((x, y, z, count, abs(x) + abs(y) + abs(z)))

    while len(at_target) > 0:
        best = []
        best_i = None

        # Find the best candidate from the possible boxes
        for i in range(len(at_target)):
            if best_i is None or at_target[i][4] < best[4]:
                best = at_target[i]
                best_i = i

        if dist == 1:
            # At the end, just return the best match
            return best[4], best[3]
        else:
            # Search in the sub boxes, see if we find any matches
            xs = [best[0] , best[0] + dist//2]
            ys = [best[1] , best[1] + dist//2]
            zs = [best[2] , best[2] + dist//2]
            a, b = find(done, bots, xs, ys, zs, dist // 2, ox, oy, oz, forced_count)
            if a is None:
                # This is a false path, remove it from consideration and try any others
                at_target.pop(best_i)
            else:
                # We found something, go ahead and let it bubble up
                return a, b

    # This means all of the candidates yeild false paths, so let this one
    # be treated as a false path by our caller
    return None, None

def calc2(log, values):
    bots = get_bots(log, values)

    # Find the range of the bots
    xs = [x[0] for x in bots] + [0]
    ys = [x[1] for x in bots] + [0]
    zs = [x[2] for x in bots] + [0]

    # Pick a starting resolution big enough to find all of the bots
    dist = 1
    while dist < max(xs) - min(xs) or dist < max(ys) - min(ys) or dist < max(zs) - min(zs):
        dist *= 2

    # And some offset values so there are no strange issues wrapping around zero
    ox = -min(xs)
    oy = -min(ys)
    oz = -min(zs)

    # Try to find all of the bots, backing off with a binary search till
    # we can find the most bots
    span = 1
    while span < len(bots):
        span *= 2
    forced_check = 1
    tried = {}

    best_val, best_count = None, None

    while True:
        # We might try the same value multiple times, save some time if we've seen it already
        if forced_check not in tried:
            tried[forced_check] = find(set(), bots, xs, ys, zs, dist, ox, oy, oz, forced_check)
        test_val, test_count = tried[forced_check]

        if test_val is None:
            # Nothing found at this level, so go back
            if span > 1:
                span = span // 2
            forced_check = max(1, forced_check - span)
        else:
            # We found something, so go forward
            if best_count is None or test_count > best_count:
                best_val, best_count = test_val, test_count
            if span == 1:
                # This means we went back one, and it was empty, so we're done!
                break
            forced_check += span

    log("The max count I found was: " + str(best_count))
    return best_val

def run(log, values):
    log("Part 1: " + str(calc(log, values)))
    log("Part 2: " + str(calc2(log, values)))

def test(log):
    values = [
        "pos=<0,0,0>, r=4",
        "pos=<1,0,0>, r=1",
        "pos=<4,0,0>, r=3",
        "pos=<0,2,0>, r=1",
        "pos=<0,5,0>, r=3",
        "pos=<0,0,3>, r=1",
        "pos=<1,1,1>, r=1",
        "pos=<1,1,2>, r=1",
        "pos=<1,3,1>, r=1",
    ]

    if calc(log, values) == 7:
        return True
    else:
        return False

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

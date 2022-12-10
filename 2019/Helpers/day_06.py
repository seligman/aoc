#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Universal Orbit Map'


def calc(log, values, calc_all):
    orbits = {}

    # Build a dictionary of all of the paths
    for cur in values:
        cur = cur.split(")")
        orbits[cur[1]] = cur[0]

    if calc_all:
        # Just find all of the orbits
        count = 0
        for cur in orbits:
            while cur in orbits:
                count += 1
                cur = orbits[cur]
        return count
    else:
        # Find the most direct path between me and Santa
        paths = []
        for cur in ["YOU", "SAN"]:
            paths.append([])
            while cur in orbits:
                cur = orbits[cur]
                paths[-1].append(cur)

        # And remove the identical tail of each path
        while paths[0][-1] == paths[1][-1]:
            paths[0].pop()
            paths[1].pop()

        # What's left is the orbits we need to 
        # bounce to, so just count them
        return sum([len(x) for x in paths])


def test(log):
    values = log.decode_values("""
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
    """)

    ret, expected = calc(log, values, True), 42
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    values = log.decode_values("""
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        K)YOU
        I)SAN
    """)

    ret, expected = calc(log, values, False), 4
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Direct and indirect orbits: " + str(calc(log, values, True)))
    log("Min orbital transfers: " + str(calc(log, values, False)))

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

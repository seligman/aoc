#!/usr/bin/env python

def get_desc():
    return 6, 'Day 6: Universal Orbit Map'


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

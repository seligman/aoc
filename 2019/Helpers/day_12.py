#!/usr/bin/env python3

def get_desc():
    return 12, 'Day 12: The N-Body Problem'


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0, 0]

    def freeze(self):
        return tuple(self.pos + self.vel)


def get_lcm(vals):
    from fractions import gcd
    lcm = vals[0]
    for i in vals[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def calc(log, values, get_energy=None):
    import re
    import itertools
    r = re.compile("<x=(.*?), y=(.*?), z=(.*?)>")

    moons = [Moon([int(x) for x in r.search(cur).groups()]) for cur in values]

    if get_energy is not None:
        for _ in range(get_energy):
            for a, b in itertools.permutations(moons, 2):
                for i in [0, 1, 2]:
                    if a.pos[i] > b.pos[i]:
                        a.vel[i] -= 1
                    elif a.pos[i] < b.pos[i]:
                        a.vel[i] += 1
            for cur in moons:
                for i in [0, 1, 2]:
                    cur.pos[i] += cur.vel[i]

        energy = 0
        for cur in moons:
            energy += sum([abs(x) for x in cur.pos]) * sum([abs(x) for x in cur.vel])
        return energy
    else:
        vals = []
        for i in [0, 1, 2]:
            val = 0
            first = tuple([x.freeze() for x in moons])
            while True:
                val += 1
                for a, b in itertools.permutations(moons, 2):
                    if a.pos[i] > b.pos[i]:
                        a.vel[i] -= 1
                    elif a.pos[i] < b.pos[i]:
                        a.vel[i] += 1
                for cur in moons:
                    cur.pos[i] += cur.vel[i]
                if tuple([x.freeze() for x in moons]) == first:
                    vals.append(val)
                    break
        return get_lcm(vals)


def test(log):
    values = log.decode_values("""
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
    """)

    ret, expected = calc(log, values, 10), 179
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    ret, expected = calc(log, values), 2772
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log("Total energy: " + str(calc(log, values, get_energy=1000)))
    log("Steps taken: " + str(calc(log, values)))

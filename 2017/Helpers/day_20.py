#!/usr/bin/env python3

import re

def get_desc():
    return 20, 'Day 20: Particle Swarm'


class Particle:
    def __init__(self, m, i):
        vals = [int(x) for x in m.groups()]
        self.x, self.y, self.z = vals[0:3]
        self.vx, self.vy, self.vz = vals[3:6]
        self.ax, self.ay, self.az = vals[6:9]
        self.best = None
        self.last = None
        self.dist()
        self.i = i

    def tick(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def dist(self):
        calc_dist = abs(self.x) + abs(self.y) + abs(self.z)
        self.best = calc_dist
        return calc_dist


def calc(log, values):
    r = re.compile("p=<([0-9-]+),([0-9-]+),([0-9-]+)>, v=<([0-9-]+),([0-9-]+),([0-9-]+)>, a=<([0-9-]+),([0-9-]+),([0-9-]+)>")
    particles = []

    i = 0
    for cur in values:
        particles.append(Particle(r.search(cur), i))
        i += 1

    remaining_particles = {}
    for cur in particles:
        remaining_particles[cur.i] = cur

    for _ in range(1000):
        used = {}
        for cur in particles:
            cur.tick()
            cur.dist()
            key = (cur.x, cur.y, cur.z)
            if key not in used:
                used[key] = []
            used[key].append(cur)

        for key in used:
            value = used[key]
            if len(value) > 1:
                for cur in value:
                    if cur.i in remaining_particles:
                        del remaining_particles[cur.i]

    particles.sort(key=lambda x: x.best)

    log.show("Leftover particles: " + str(len(remaining_particles)))

    return particles[0].i


def test(log):
    values = [
        "p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>",
        "p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>",
    ]

    if calc(log, values) == 0:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))

#!/usr/bin/env python3

DAY_NUM = 24
DAY_DESC = 'Day 24: Never Tell Me The Odds'

import itertools
import numpy as np
from decimal import Decimal as D

class Hail:
    def __init__(self, inp):
        inp = inp.split(" @ ")
        pos = tuple(D(x.strip()) for x in inp[0].split(","))
        vel = tuple(D(x.strip()) for x in inp[1].split(","))
        self.px, self.py, self.pz = pos
        self.vx, self.vy, self.vz = vel
        self.XYslope = D('inf') if self.vx==0 else self.vy/self.vx
        self.ax, self.ay, self.az = 0,0,0
        
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'<{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}>'
    
    def intersectXY(self, other):
        if self.XYslope==other.XYslope:
            return None
        if self.XYslope == float('inf'):
            intX = self.px
            intY = other.XYslope * (intX - other.px) + other.py
        elif other.XYslope == float('inf'):
            intX = other.px
            intY = self.XYslope * (intX - self.px) + self.py
        else:
            intX = (self.py-other.py  - self.px*self.XYslope + other.px*other.XYslope)/(other.XYslope-self.XYslope)
            intY = self.py + self.XYslope*(intX-self.px)
        intX, intY = intX.quantize(D(".1")), intY.quantize(D(".1"))

        selfFuture = np.sign(intX-self.px) == np.sign(self.vx)
        otherFuture = np.sign(intX-other.px) == np.sign(other.vx)
        if not (selfFuture and otherFuture):
            return None
        return (intX,intY)
    
    def adjust(self, ax, ay, az):
        self.vx -= ax - self.ax
        self.vy -= ay - self.ay
        self.vz -= az - self.az
        assert type(self.vx) is D
        self.XYslope = D('inf') if self.vx==0 else self.vy/self.vx
        self.ax, self.ay, self.az = ax, ay, az
        
    def getT(self, p):
        if self.vx==0:
            return (p[1]-self.py)/self.vy
        return (p[0]-self.px)/self.vx
        
    def getZ(self, other, inter):
        tS = self.getT(inter)
        tO = other.getT(inter)
        if tS==tO:
            assert self.pz + tS*self.vz == other.pz + tO*other.vz
            return None
        return (self.pz - other.pz + tS*self.vz - tO*other.vz)/(tS - tO)

def calc(log, values, mode, lower, upper):
    hail = []
    for row in values:
        hail.append(Hail(row))

    if mode == 1:
        ret = 0
        for H1, H2 in itertools.combinations(hail, 2):
            p = H1.intersectXY(H2)
            if p is None:
                pass
            elif lower <= p[0] <= upper and lower <= p[1] <= upper:
                ret += 1
        return ret
    else:
        N = 0
        while True:
            for X in range(N+1):
                Y = N-X
                for negX in (-1,1):
                    for negY in (-1,1):
                        aX = X*negX
                        aY = Y*negY
                        H1 = hail[0]
                        H1.adjust(aX, aY, 0)
                        inter = None
                        for H2 in hail[1:]:
                            H2.adjust(aX, aY, 0)
                            p = H1.intersectXY(H2)
                            if p is None:
                                break
                            if inter is None:
                                inter = p
                                continue
                            if p != inter:
                                break
                        if p is None or p != inter:
                            continue
                        aZ = None
                        H1 = hail[0]
                        for H2 in hail[1:]:
                            nZ = H1.getZ(H2, inter)
                            if aZ is None:
                                aZ = nZ
                                continue
                            elif nZ != aZ:
                                return
                        if aZ == nZ:
                            H = hail[0]
                            Z = H.pz + H.getT(inter)*(H.vz-aZ)
                            return int(Z+inter[0]+inter[1])
                            
            N += 1
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
    log(f"Part 1: {calc(log, values, 1, 200000000000000, 400000000000000)}")
    log(f"Part 2: {calc(log, values, 2, 0, 0)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2023/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

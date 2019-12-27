#!/usr/bin/env python

import sys
from datetime import datetime, timedelta
import os

def main(lines):
    sys.path.insert(0, os.path.join('..', '..', 'Helpers'))

    from grid import Grid
    from dummylog import DummyLog
    from program import Program

    SIF = False

    Program.debug(lines)
    msg = datetime.utcnow()

    g = Grid(default=" ")
    p = Program([int(x) for x in lines.split(",")], DummyLog())
    width, height = None, None
    x, y = 0, 0
    while p.flag_running:
        p.tick()
        if width is None and SIF:
            if len(p.output) == 2:
                width, height = p.get_output(to_get=2)
                print(width, height)
        else:
            if len(p.output) == (1 if SIF else 3):
                if SIF:
                    i = p.get_output()
                else:
                    x, y, i = p.get_output(to_get=3)

                if datetime.utcnow() >= msg:
                    msg += timedelta(seconds=5)
                    print("x: %4d, y: %4d, %3d, '%s'" % (x, y, i, chr(i)))
                    
                g.set(x, y, chr(i))

                if SIF:
                    x += 1
                    if x >= width:
                        y += 1
                        x = 0

    g.show_grid(DummyLog(), dump_all=True)
    g.draw_grid(color_map={
        " ": (0, 0, 0),
        "a": (0, 0, 170),
        "b": (0, 170, 0),
        "c": (0, 170, 170),
        "d": (170, 0, 0),
        "e": (170, 0, 170),
        "f": (170, 85, 0),
        "g": (170, 170, 170),
        "h": (85, 85, 85),
        "i": (85, 85, 255),
        "j": (85, 255, 85),
        "k": (85, 255, 255),
        "l": (255, 85, 85),
        "m": (255, 85, 255),
        "n": (255, 255, 85),
        "o": (255, 255, 255),

        "9": (0, 0, 0),
        "0": (0, 0, 170),
        "1": (0, 170, 0),
        "2": (0, 170, 170),
        "3": (170, 0, 0),
        "4": (170, 0, 170),
        "5": (170, 85, 0),
        "6": (170, 170, 170),
        "7": (85, 85, 85),
        "8": (85, 85, 255),
    }, cell_size=(2 if SIF else 5), show_lines=(False if SIF else True))

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        main(f.read())

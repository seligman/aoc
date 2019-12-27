#!/usr/bin/env python

import re
from collections import deque

def get_desc():
    return 17, 'Day 17: Reservoir Research'


class Spigot:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.skip_down = False
        self.retried = False


def calc(log, values):
    offset = 500
    max_offset = 500
    r_x = re.compile("x=([0-9]+), y=([0-9]+)\\.\\.([0-9]+)")
    r_y = re.compile("y=([0-9]+), x=([0-9]+)\\.\\.([0-9]+)")
    rows = []

    min_y = None

    for cur in values:
        m = r_x.search(cur)
        if m is not None:
            x, y1, y2 = [int(temp) for temp in m.groups()]
            if min_y is None:
                min_y = y1
            else:
                min_y = min(min_y, y1)
            if (x - 5) < offset:
                for i in range(len(rows)):
                    rows[i] = (['.'] * (offset - (x - 5))) + rows[i]
                offset = (x - 5)
            if (x + 5) > max_offset:
                for i in range(len(rows)):
                    rows[i] += ['.'] * ((x + 5) - max_offset)
                max_offset = x + 5
            while y2 >= len(rows):
                rows.append(['.'] * (max_offset - offset))
            
            for y in range(y1, y2+1):
                rows[y][x - offset] = '#'
        else:
            y, x1, x2 = [int(temp) for temp in r_y.search(cur).groups()]
            if min_y is None:
                min_y = y
            else:
                min_y = min(min_y, y)
            if x1 < offset:
                for i in range(len(rows)):
                    rows[i] = (['.'] * (offset - (x1 - 5))) + rows[i]
                offset = (x1 - 5)
            if (x2 + 5) > max_offset:
                for i in range(len(rows)):
                    rows[i] += ['.'] * ((x2 + 5) - max_offset)
                max_offset = x2 + 5
            while y >= len(rows):
                rows.append(['.'] * (max_offset - offset))
            for x in range(x1, x2+1):
                rows[y][x - offset] = '#'

    spigots = deque([Spigot(500, 0)])

    drops = 0
    bail = 10000
    limit = 0
    stored_water = 0

    while len(spigots) > 0:
        bail -= 1
        if bail == 0:
            break

        cur = spigots.popleft()
        if cur.y > limit:
            limit = cur.y
        if cur.y == len(rows):
            pass
        else:
            if rows[cur.y][cur.x - offset] == ".":
                rows[cur.y][cur.x - offset] = '+'
                drops += 1

            if cur.y+1 == len(rows):
                pass
            elif rows[cur.y+1][cur.x - offset] in {'.', '+'}:
                if rows[cur.y+1][cur.x - offset] in {'.'}:
                    spigots.append(Spigot(cur.x, cur.y+1, parent=cur))
            else:
                hit_edge = 0
                to_muck = [cur.x - offset]
                to_spill = []
                for off in [1, -1]:
                    dir_off = off
                    while True:
                        if rows[cur.y + 1][cur.x + off - offset] in {'.', '+'}:
                            to_muck.append(cur.x + off - offset)
                            to_spill.append(cur.x + off)
                            break
                        else:
                            if rows[cur.y][cur.x + off - offset] in {'.', '+', 'x'}:
                                to_muck.append(cur.x + off - offset)
                                off += dir_off
                            else:
                                hit_edge += 1
                                break

                if hit_edge == 2:
                    for muck in to_muck:
                        if rows[cur.y][muck] in {".", "+"}:
                            if rows[cur.y][muck] == ".":
                                drops += 1
                            if rows[cur.y][muck] != 'x':
                                stored_water += 1
                                rows[cur.y][muck] = 'x'
                    cur = cur.parent
                    if rows[cur.y][cur.x - offset] == "+":
                        spigots.append(cur)
                else:
                    for muck in to_muck:
                        if rows[cur.y][muck] == ".":
                            drops += 1
                            rows[cur.y][muck] = '+'
                    for spill in to_spill:
                        if rows[cur.y+1][spill - offset] == '.':
                            rows[cur.y+1][spill - offset] = '+'
                            drops += 1
                            spigots.append(Spigot(spill, cur.y + 1, parent=cur))


    for z in spigots:
        rows[z.y][z.x - offset] = '*'

    log.show("Stored water: " + str(stored_water))

    return drops - min_y


def test(log):
    values = [
        "x=495, y=2..7",
        "y=7, x=495..501",
        "x=501, y=3..7",
        "x=498, y=2..4",
        "x=506, y=1..2",
        "x=498, y=10..13",
        "x=504, y=10..13",
        "y=13, x=498..504",
    ]

    if calc(log, values) == 57:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(log, values))

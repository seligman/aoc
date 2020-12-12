#!/usr/bin/env python3

def get_desc():
    return 12, 'Day 12: Rain Risk'

def calc(log, values, mode):
    pos = complex(0, 0)
    way = complex(10, -1)
    dirs = {
        'E': [complex(1, 0), 'N', 'S'],
        'S': [complex(0, 1), 'E', 'W'],
        'W': [complex(-1, 0), 'S', 'N'],
        'N': [complex(0, -1), 'W', 'E'],
    }

    if mode == 1:
        dir = 'E'
        for cur in values:
            cardinal = cur[0]
            if cardinal == 'L':
                for _ in range(0, int(cur[1:]), 90):
                    dir = dirs[dir][1]
                cardinal = "x"
            elif cardinal == 'R':
                for _ in range(0, int(cur[1:]), 90):
                    dir = dirs[dir][2]
                cardinal = "x"
            elif cardinal == 'F':
                cardinal = dir
            else:
                cardinal = cur[0]
            if cardinal != "x":
                pos += dirs[cardinal][0] * int(cur[1:])
    else:
        for cur in values:
            if cur[0] == "F":
                pos += way * int(cur[1:])
            elif cur[0] in dirs:
                way += dirs[cur[0]][0] * int(cur[1:])
            elif cur[0] == "R":
                for _ in range(0, int(cur[1:]), 90):
                    way = complex(-way.imag, way.real)
            elif cur[0] == "L":
                for _ in range(0, int(cur[1:]), 90):
                    way = complex(way.imag, -way.real)

    return int(abs(pos.real) + abs(pos.imag))

def test(log):
    values = log.decode_values("""
        F10
        N3
        F7
        R90
        F11
    """)

    log.test(calc(log, values, 1), 25)
    log.test(calc(log, values, 2), 286)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

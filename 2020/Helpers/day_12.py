#!/usr/bin/env python3

def get_desc():
    return 12, 'Day 12: Rain Risk'

def calc(log, values, mode):
    x, y = 0, 0
    wp_x, wp_y = 10, -1
    dirs = {
        'E': [1, 0, 'N', 'S'],
        'S': [0, 1, 'E', 'W'],
        'W': [-1, 0, 'S', 'N'],
        'N': [0, -1, 'W', 'E'],
    }

    if mode == 1:
        dir = 'E'
        for cur in values:
            cardinal = cur[0]
            if cardinal == 'L':
                for _ in range(0, int(cur[1:]), 90):
                    dir = dirs[dir][2]
                cardinal = "x"
            elif cardinal == 'R':
                for _ in range(0, int(cur[1:]), 90):
                    dir = dirs[dir][3]
                cardinal = "x"
            elif cardinal == 'F':
                cardinal = dir
            else:
                cardinal = cur[0]
            if cardinal != "x":
                x += dirs[cardinal][0] * int(cur[1:])
                y += dirs[cardinal][1] * int(cur[1:])
    else:
        for cur in values:
            if cur[0] == "F":
                x += wp_x * int(cur[1:])
                y += wp_y * int(cur[1:])
            elif cur[0] in dirs:
                wp_x += dirs[cur[0]][0] * int(cur[1:])
                wp_y += dirs[cur[0]][1] * int(cur[1:])
            elif cur[0] == "R":
                for _ in range(0, int(cur[1:]), 90):
                    wp_x, wp_y = -wp_y, wp_x
            elif cur[0] == "L":
                for _ in range(0, int(cur[1:]), 90):
                    wp_x, wp_y = wp_y, -wp_x

    return abs(x) + abs(y)

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

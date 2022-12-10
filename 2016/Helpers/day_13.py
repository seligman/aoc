#!/usr/bin/env python3

from collections import deque

DAY_NUM = 13
DAY_DESC = 'Day 13: A Maze of Twisty Little Cubicles'


def calc_point(x, y, num):
    num = x * x + 3 * x + 2 * x * y + y + y * y + num
    ret = 0
    while num > 0:
        if num & 1 == 1:
            ret += 1
        num >>= 1
    if ret % 2 == 0:
        return "."
    else:
        return "#"


def calc(values, target_x, target_y, target_dist):
    num = int(values[0])
    seen = set()
    todo = deque()

    todo.append([1, 1, 0])
    if target_dist is None:
        seen.add((1,1))

    ret = 0

    dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    while len(todo) > 0:
        cur = todo.pop()
        skip = False
        if target_x is not None:
            if cur[0] == target_x and cur[1] == target_y:
                return cur[2]
        else:
            if cur[2] == target_dist:
                skip = True

        if not skip:
            for off_x, off_y in dirs:
                x = off_x + cur[0]
                y = off_y + cur[1]
                if x >= 0 and y >= 0:
                    if (x, y) not in seen:
                        seen.add((x, y))
                        if calc_point(x, y, num) == ".":
                            todo.append((x, y, cur[2] + 1))
                            ret += 1

    return ret


def test(log):
    values = [
        "10",
    ]

    if calc(values, 7, 4, None) == 11:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 31, 39, None))
    log.show(calc(values, None, None, 50))

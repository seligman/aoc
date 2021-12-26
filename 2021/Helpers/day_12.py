#!/usr/bin/env python3

from collections import deque, defaultdict

DAY_NUM = 12
DAY_DESC = 'Day 12: Passage Pathing'

def calc(log, values, mode):
    paths = defaultdict(set)
    small_rooms = set()

    for cur in values:
        if len(cur.strip()) > 0:
            cur = cur.split("-")
            for x, y in ((cur[0], cur[1]), (cur[1], cur[0])):
                if x.lower() == x and x not in {"start", "end"}:
                    small_rooms.add(x)

                if y != "start":
                    paths[x].add(y)

    trails = 0
    todo = deque([(set(["start"]), False, "start")])
    while len(todo) > 0:
        trail, dupe, cur = todo.pop()
        for x in paths[cur]:
            if x == "end":
                trails += 1
            elif x in small_rooms:
                if x not in trail:
                    todo.append((trail | set([x]), dupe, x))
                elif mode == 2:
                    if not dupe:
                        todo.append((trail, True, x))
            else:
                todo.append((trail | set([x]), dupe, x))

    return trails

def test(log):
    values = log.decode_values("""
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
    """)

    log.test(calc(log, values, 1), 10)
    log.test(calc(log, values, 2), 36)

    values = log.decode_values("""
        fs-end
        he-DX
        fs-he
        start-DX
        pj-DX
        end-zg
        zg-sl
        zg-pj
        pj-he
        RW-he
        fs-DX
        pj-RW
        zg-RW
        start-pj
        he-WI
        zg-he
        pj-fs
        start-RW
    """)

    log.test(calc(log, values, 1), 226)
    log.test(calc(log, values, 2), 3509)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    cur = None
    for cur in sys.argv[1:] + ["input.txt", "day_##_input.txt", "Puzzles/day_##_input.txt", "../Puzzles/day_##_input.txt"]:
        cur = os.path.join(*cur.split("/")).replace("##", f"{DAY_NUM:02d}")
        if os.path.isfile(cur): fn = cur; break
    if cur is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = f.readlines()
    print(f"Running day {DAY_DESC}:")
    run(print, values)

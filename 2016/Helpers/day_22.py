#!/usr/bin/env python3

import re
from collections import deque

def get_desc():
    return 22, 'Day 22: Grid Computing'


def find_path(nodes, lx, ly, start, end, goal=None):
    for value in nodes.values():
        value['dist'] = None
        value['prev'] = None

    todo = deque()
    todo.append(start)
    nodes[start]['dist'] = 0

    while len(todo) > 0:
        n = todo.popleft()
        for x, y in [(n[0]+1, n[1]), (n[0]-1, n[1]), (n[0], n[1]+1), (n[0], n[1]-1)]:
            if 0 <= x < lx and 0 <= y < ly and nodes[(x,y)]['used'] < 100 and (x, y) != goal:
                if nodes[(x, y)]['dist'] is None or nodes[(x, y)]['dist'] > nodes[n]['dist'] + 1:
                    nodes[(x, y)]['dist'] = nodes[n]['dist'] + 1
                    nodes[(x, y)]['prev'] = n
                    todo.append((x, y))

                if (x, y) == end:
                    path = [(x, y)]
                    while nodes[path[-1]]['prev'] != None:
                        path.append(nodes[path[-1]]['prev'])
                    return path[-2::-1]


def calc(log, values):
    nodes = {}

    for cur in values:
        if cur.startswith("/"):
            x, y, _size, used, avail, _perc = map(int, re.findall(r'\d+', cur))
            nodes[(x, y)] = {'used': used, 'avail': avail}

    lx = max([x[0] for x in nodes])+1
    ly = max([x[1] for x in nodes])+1

    pairs = 0
    vals = list(nodes.values())
    for i in range(len(vals)):
        for j in range(i+1, len(vals)):
            if vals[i]['used'] != 0 and vals[i]['used'] <= vals[j]['avail']:
                pairs += 1 
            if vals[j]['used'] != 0 and vals[j]['used'] <= vals[i]['avail']:
                pairs += 1


    start = (0, 0)
    goal = (lx - 1, 0)
    empty = (None, None)
    for key in nodes:
        if nodes[key]['used'] == 0:
            empty = key
            break

    paths = find_path(nodes, lx, ly, goal, start)
    steps = 0
    
    while goal != start:
        target_path = find_path(nodes, lx, ly, empty, paths.pop(0), goal=goal)
        steps += len(target_path) + 1
        empty = goal
        goal = target_path[-1]

    log.show("Found the path in: " + str(steps))

    return pairs


def test(log):
    return True


def run(log, values):
    log.show(calc(log, values))

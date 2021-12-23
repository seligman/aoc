#!/usr/bin/env python3

import heapq

def get_desc():
    return 23, 'Day 23: Amphipod'

targets = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9
}

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class State:
    def __init__(self, dist, slugs, room_depth, stack):
        self.dist = dist
        self.slugs = slugs
        self.room_depth = room_depth
        self.stack = stack

    def is_solved(self):
        if all(x == targets[c] for c, x, _ in self.slugs): 
            return True
        return False

    def move_to(self, kind, x1, y1, x2, y2):
        return State(
            manhattan(x1, y1, x2, y2) * costs[kind] + self.dist,
            self.slugs ^ {(kind, x1, y1), (kind, x2, y2)},
            self.room_depth,
            self.stack[:]
        )

    def moves(self):
        moves = []
        for kind, x, y in self.slugs:
            if y == 1:
                target = targets[kind]
                if any(x2 == target and kind2 != kind for kind2, x2, _ in self.slugs): 
                    continue
                if any(y2 == 1 and (target < x2 < x or x < x2 < target) for _, x2, y2 in self.slugs): 
                    continue
                populace = {y2 for _, x2, y2 in self.slugs if x2 == target}
                target_y = min(populace)-1 if len(populace) > 0 else self.room_depth+1
                moves.append(self.move_to(kind, x, y, target, target_y))
            else:
                if any(x2 == x and y2 < y for _, x2, y2 in self.slugs): 
                    continue
                left = x
                right = x+1
                while left > 1 and not any (x2 == left - 1 and y2 == 1 for _, x2, y2 in self.slugs):
                    left -= 1
                while right < 12 and not any (x2 == right and y2 == 1 for _, x2, y2 in self.slugs):
                    right += 1
                for target in range(left, right):
                    if target in targets.values(): 
                        continue
                    moves.append(self.move_to(kind, x, y, target, 1))
        return moves

    def __hash__(self):
        return hash(self.slugs)

    def __eq__(self, other):
        return self.slugs == other.slugs

    def __lt__(self, other):
        return self.dist < other.dist

def calc(log, values, mode, draw=False):
    from grid import Grid
    if mode == 2:
        values.insert(3, "  #D#C#B#A#")
        values.insert(4, "  #D#B#A#C#")
        room_depth = 4
    else:
        room_depth = 2

    grid = Grid.from_text(values)
    state = State(0, frozenset((grid[x, y], x, y) for x, y in grid.grid.keys() if grid[x, y] not in "#. "), room_depth, [])

    todo = [state]
    heapq.heapify(todo)
    seen = set()

    while len(todo) > 0:
        node = heapq.heappop(todo)
        if node not in seen:
            seen.add(node)
            if node.is_solved():
                return node.dist
            else:
                for other in node.moves():
                    heapq.heappush(todo, other)

    return None

def test(log):
    values = log.decode_values("""
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########
    """)

    log.test(calc(log, values, 1), 12521)
    log.test(calc(log, values, 2), 44169)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

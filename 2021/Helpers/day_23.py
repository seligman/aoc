#!/usr/bin/env python3

import heapq

DAY_NUM = 23
DAY_DESC = 'Day 23: Amphipod'

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

class State:
    def __init__(self, dist, cells, room_depth, stack, step=None):
        self.dist = dist
        self.cells = cells
        self.room_depth = room_depth
        self.stack = stack
        self.step = step

    def is_solved(self):
        if all(x == targets[c] for c, x, _ in self.cells): 
            return True
        return False

    def move_to(self, kind, x1, y1, x2, y2):
        return State(
            (abs(x1 - x2) + abs(y1 - y2)) * costs[kind] + self.dist,
            self.cells ^ {(kind, x1, y1), (kind, x2, y2)},
            self.room_depth,
            self.stack[:],
            (x1, y1, x2, y2),
        )

    def moves(self):
        ret = []
        for kind, x, y in self.cells:
            if y == 1:
                target = targets[kind]
                if any(x2 == target and kind2 != kind for kind2, x2, _ in self.cells): 
                    continue
                if any(y2 == 1 and (target < x2 < x or x < x2 < target) for _, x2, y2 in self.cells): 
                    continue
                populace = {y2 for _, x2, y2 in self.cells if x2 == target}
                target_y = min(populace)-1 if len(populace) > 0 else self.room_depth+1
                ret.append(self.move_to(kind, x, y, target, target_y))
            else:
                if any(x2 == x and y2 < y for _, x2, y2 in self.cells): 
                    continue
                left = x
                right = x+1
                while left > 1 and not any (x2 == left - 1 and y2 == 1 for _, x2, y2 in self.cells):
                    left -= 1
                while right < 12 and not any (x2 == right and y2 == 1 for _, x2, y2 in self.cells):
                    right += 1
                for target in range(left, right):
                    if target in targets.values(): 
                        continue
                    ret.append(self.move_to(kind, x, y, target, 1))
        return ret

    def __hash__(self):
        return self.cells.__hash__()
    def __eq__(self, other):
        return self.cells.__eq__(other.cells)
    def __lt__(self, other):
        return self.dist.__lt__(other.dist)

def calc(log, values, mode, draw=False):
    from grid import Grid
    if mode == 2:
        values.insert(3, "  #D#C#B#A#")
        values.insert(4, "  #D#B#A#C#")
        room_depth = 4
    else:
        room_depth = 2

    grid = Grid.from_text(values)
    state = State(
        0, 
        frozenset((grid[x, y], x, y) for x, y in grid.grid.keys() if grid[x, y] not in "#. "), 
        room_depth, 
        [],
    )

    todo = [state]
    heapq.heapify(todo)
    seen = set()

    if draw:
        for _ in range(20):
            grid.save_frame()

    def swap(grid, x1, y1, x2, y2, cost, add):
        grid[x1, y1], grid[x2, y2] = grid[x2, y2], grid[x1, y1]
        cost[0] += add
        grid.save_frame(extra_text=[f"Cost {cost[0]}"])

    while len(todo) > 0:
        node = heapq.heappop(todo)
        if draw:
            node.stack.append((node.dist, node.step))
        if node not in seen:
            seen.add(node)
            if node.is_solved():
                if draw:
                    cost = [0]
                    for _, step in node.stack:
                        if step is not None:
                            (x1, y1, x2, y2) = step
                            add = costs[grid[x1, y1]]
                            while y2 < y1:
                                swap(grid, x1, y1, x1, y1 - 1, cost, add)
                                y1 -= 1
                            while x1 > x2:
                                swap(grid, x1, y1, x1 - 1, y1, cost, add)
                                x1 -= 1
                            while x1 < x2:
                                swap(grid, x1, y1, x1 + 1, y1, cost, add)
                                x1 += 1
                            while y2 > y1:
                                swap(grid, x1, y1, x1, y1 + 1, cost, add)
                                y1 += 1
                    grid.draw_frames(cell_size=(40, 40))
                return node.dist
            else:
                for other in node.moves():
                    heapq.heappush(todo, other)

    return None

def other_draw(describe, values):
    if describe:
        return "Draw the grids"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=10, final_secs=5)

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
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

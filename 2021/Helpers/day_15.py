#!/usr/bin/env python3

def get_desc():
    return 15, 'Day 15: Chiton'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)

    if mode == 2:
        w, h = grid.width(), grid.height()
        pts = [(x, y, int(grid[x, y])) for x, y in grid.grid]
        for ox, oy in [(x // 5, x % 5) for x in range(1, 25)]:
            for x, y, val in pts:
                grid[x + ox * w, y + oy * h] = str(((val - 1 + ox + oy) % 9) + 1)

    todo = [(0, 0, 0)]
    seen = set([(0, 0)])
    best = None
    while len(todo):
        todo.sort(key=lambda x: x[2])
        x, y, cost = todo.pop(0)
        if best is None or cost < best:
            for ox, oy in grid.neighbors(x, y, valid_only=True):
                if ox == grid.width() - 1 and oy == grid.height() - 1:
                    cost += int(grid[ox, oy])
                    if best is None or cost < best:
                        return cost
                if (ox, oy) not in seen:
                    seen.add((ox, oy))
                    todo.append((ox, oy, cost + int(grid[ox, oy])))

    return best

def test(log):
    values = log.decode_values("""
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
    """)

    log.test(calc(log, values, 1), 40)
    log.test(calc(log, values, 2), 315)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

#!/usr/bin/env python3

def get_desc():
    return 11, 'Day 11: Seating System'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)

    last_seen = ""
    dirs = [[-1,-1],[0,-1],[1,-1],[-1,1],[0,1],[1,1],[-1,0],[1,0]]

    while True:
        todo = []
        # g2 = grid.copy()
        for x in grid.x_range():
            for y in grid.y_range():
                occupied = 0
                if mode == 1:
                    for dir in dirs:
                        if grid.get(x + dir[0], y + dir[1]) == "#":
                            occupied += 1
                else:
                    for dir in dirs:
                        tx, ty = x + dir[0], y + dir[1]
                        while tx >= 0 and ty >= 0 and tx < grid.width() and ty < grid.height():
                            spot = grid.get(tx, ty)
                            if spot == "L":
                                break
                            if spot == "#":
                                occupied += 1
                                break
                            tx += dir[0]
                            ty += dir[1]

                spot = grid.get(x, y)
                if spot == "L":
                    if occupied == 0:
                        todo.append((x, y, "#"))
                elif spot == "#":
                    if occupied >= (4 if mode == 1 else 5):
                        todo.append((x, y, "L"))

        for x, y, spot in todo:
            grid.set(spot, x, y)
        dump = grid.dump_grid()
        if dump == last_seen:
            break
        last_seen = dump

    occupied = 0
    for x in grid.x_range():
        for y in grid.y_range():
            if grid.get(x, y) == "#":
                occupied += 1
    return occupied


def test(log):
    values = log.decode_values("""
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL
    """)

    log.test(calc(log, values, 1), 37)
    log.test(calc(log, values, 2), 26)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

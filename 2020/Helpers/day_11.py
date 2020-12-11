#!/usr/bin/env python3

def get_desc():
    return 11, 'Day 11: Seating System'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid.from_text(values)

    width = grid.width()
    height = grid.height()

    last_seen = ""
    dirs = [(x // 3 - 1, x % 3 - 1) for x in range(9) if x != 4]

    while True:
        todo = []
        for x in range(width):
            for y in range(height):
                occupied = 0
                if mode == 1:
                    for dx, dy in dirs:
                        if grid.get(x + dx, y + dy) == "#":
                            occupied += 1
                else:
                    for dx, dy in dirs:
                        tx, ty = x + dx, y + dy
                        while tx >= 0 and ty >= 0 and tx < width and ty < height:
                            spot = grid.get(tx, ty)
                            if spot == "L":
                                break
                            if spot == "#":
                                occupied += 1
                                break
                            tx, ty = tx + dx, ty + dy

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

    return len([x for x in grid.dump_grid() if x == "#"])


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

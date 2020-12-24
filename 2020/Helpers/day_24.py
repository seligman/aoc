#!/usr/bin/env python3

import re

def get_desc():
    return 24, 'Day 24: Lobby Layout'

def calc(log, values, mode):
    from grid import Grid
    grid = Grid(".")

    r = re.compile("(e|se|sw|w|nw|ne)")
    for row in values:
        x, y = 0, 0
        for m in r.finditer(row):
            hit = m.group(1)
            if hit == "e":
                x += 2
            elif hit == "w":
                x -= 2
            elif hit == "se":
                y += 1
                x += 1
            elif hit == "sw":
                y += 1
                x -= 1
            elif hit == "ne":
                y -= 1
                x += 1
            elif hit == "nw":
                y -= 1
                x -= 1
        grid[x, y] = "X" if grid[x, y] == "." else "."

    if mode == 1:
        return len([x for x in grid.grid.values() if x == "X"])

    dirs = [(-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1)]

    for _ in range(100):
        todo = []
        for y in grid.axis_range(1, 1):
            for x in grid.axis_range(0, 2):
                use = False
                if y % 2 == 0:
                    if x % 2 == 0:
                        use = True
                else:
                    if x % 2 == 1:
                        use = True
                if use:
                    black = 0
                    for xo, yo in dirs:
                        if grid[x + xo, y + yo] == "X":
                            black += 1
                    if grid[x, y] == "X" and (black == 0 or black > 2):
                        todo.append((x, y, "."))
                    if grid[x, y] == "." and black == 2:
                        todo.append((x, y, "X"))

        for x, y, val in todo:
            grid[x, y] = val

    return len([x for x in grid.grid.values() if x == "X"])

def test(log):
    values = log.decode_values("""
        sesenwnenenewseeswwswswwnenewsewsw
        neeenesenwnwwswnenewnwwsewnenwseswesw
        seswneswswsenwwnwse
        nwnwneseeswswnenewneswwnewseswneseene
        swweswneswnenwsewnwneneseenw
        eesenwseswswnenwswnwnwsewwnwsene
        sewnenenenesenwsewnenwwwse
        wenwwweseeeweswwwnwwe
        wsweesenenewnwwnwsenewsenwwsesesenwne
        neeswseenwwswnwswswnw
        nenwswwsewswnenenewsenwsenwnesesenew
        enewnwewneswsewnwswenweswnenwsenwsw
        sweneswneswneneenwnewenewwneswswnese
        swwesenesewenwneswnwwneseswwne
        enesenwswwswneneswsenwnewswseenwsese
        wnwnesenesenenwwnenwsewesewsesesew
        nenewswnwewswnenesenwnesewesw
        eneswnwswnwsenenwnwnwwseeswneewsenese
        neswnwewnwnwseenwseesewsenwsweewe
        wseweeenwnesenwwwswnew
    """)

    log.test(calc(log, values, 1), 10)
    log.test(calc(log, values, 2), 2208)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

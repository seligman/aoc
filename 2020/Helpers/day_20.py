#!/usr/bin/env python3

from collections import defaultdict

def get_desc():
    return 20, 'Day 20: Jurassic Jigsaw'

def calc(log, values, mode):
    # TODO: Delete or use these
    from grid import Grid
    grids = []
    temp = []
    name = ""
    for cur in values:
        if cur.startswith("Tile "):
            if len(temp) > 0:
                grids.append(Grid.from_text(temp))
                grids[-1].extra = name
            temp = []
            name = cur[5:-1]
        elif len(cur) > 0:
            temp.append(cur)
    if len(temp) > 0:
        grids.append(Grid.from_text(temp))
        grids[-1].extra = name
    side_len = grids[0].width()

    # for grid in grids.values():
    #     grid.x_1_edge = "".join(grid[0, y] for y in range(side_len))
    #     grid.x_2_edge = "".join(grid[side_len - 1, y] for y in range(side_len))
    #     grid.y_1_edge = "".join(grid[x, 0] for x in range(side_len))
    #     grid.y_2_edge = "".join(grid[x, side_len - 1] for x in range(side_len))

    edges = defaultdict(set)
    for grid in grids:
        grid.any = set(grid.any_side())
        for edge in grid.any:
            edges[edge].add(grid)

    temp = None
    ret = 1
    for grid in grids:
        shared = 0
        for edge in grid.any:
            if len(edges[edge]) > 1:
                shared += 1
        grid.extra2 = shared
        if shared == 4:
            ret *= int(grid.extra)
            if temp is None:
                temp = grid
    
    if mode == 1:
        return ret

    def get_corners(temp):
        all_temp = temp.any.copy()
        for grid_a in [x for x in grids if x.extra2 == 6]:
            if len(set(grid_a.any) & all_temp):
                for grid_b in [x for x in grids if x.extra2 == 6]:
                    if grid_a.extra != grid_b.extra and len(set(grid_b.any) & all_temp):
                        for _ in temp.rotate_all():
                            for _ in grid_a.rotate_all():
                                for _ in grid_b.rotate_all():
                                    if temp.get_column(-1) == grid_a.get_column(0) and temp.get_row(-1) == grid_b.get_row(0):
                                        return temp, grid_a, grid_b

    temp, grid_a, grid_b = get_corners(temp)

    layout = {
        (0, 0): temp,
        (1, 0): grid_a,
        (0, 1): grid_b,
    }
    used = set([x.extra for x in layout.values()])
    size = 1
    while size * size != len(grids):
        size += 1
    for x in range(size):
        for y in range(size):
            if (x, y) not in layout:
                for grid in grids:
                    valid = True
                    if grid.extra in used:
                        valid = False
                    if (x, y) in {(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)}:
                        if grid.extra2 != 4:
                            valid = False
                    elif x == 0 or y == 0 or x == size - 1 or y == size - 1:
                        if grid.extra2 != 6:
                            valid = False
                    else:
                        if grid.extra2 != 8:
                            valid = False
                    if valid:
                        good = True
                        if good and x > 0:
                            if grid.any & layout[(x - 1, y)].any == 0:
                                good = False
                        if good and y > 0:
                            if grid.any & layout[(x, y - 1)].any == 0:
                                good = False
                        if good:
                            for _ in grid.rotate_all():
                                good = True
                                if good and x > 0:
                                    if layout[(x - 1, y)].get_column(-1) != grid.get_column(0):
                                        good = False
                                if good and y > 0:
                                    if layout[(x, y - 1)].get_row(-1) != grid.get_row(0):
                                        good = False
                                if good:
                                    layout[(x, y)] = grid
                                    used.add(grid.extra)
                                    break
                    if (x, y) in layout:
                        break

    big = Grid(".")
    for x in range(size):
        for y in range(size):
            for xo in range(1, side_len - 1):
                for yo in range(1, side_len - 1):
                    big[x * (side_len - 2) + (xo - 1), y * (side_len - 2) + (yo - 1)] = layout[(x, y)][xo, yo]

    monster = Grid.from_text([
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ])

    for _ in big.rotate_all():
        any_hit = False
        for x in big.x_range():
            for y in big.x_range():
                hit = True
                for xo in monster.x_range():
                    for yo in monster.y_range():
                        if monster[xo, yo] == "#" and big[x + xo, y + yo] != "#":
                            hit = False
                            break
                    if not hit:
                        break
                if hit:
                    for xo in monster.x_range():
                        for yo in monster.y_range():
                            if monster[xo, yo] == "#":
                                big[x + xo, y + yo] = "O"
                    any_hit = True
        if any_hit:
            break

    ret = 0
    for x in big.x_range():
        for y in big.x_range():
            if big[x, y] == "#":
                ret += 1
    
    return ret


def test(log):
    values = log.decode_values("""
        Tile 2311:
        ..##.#..#.
        ##..#.....
        #...##..#.
        ####.#...#
        ##.##.###.
        ##...#.###
        .#.#.#..##
        ..#....#..
        ###...#.#.
        ..###..###

        Tile 1951:
        #.##...##.
        #.####...#
        .....#..##
        #...######
        .##.#....#
        .###.#####
        ###.##.##.
        .###....#.
        ..#.#..#.#
        #...##.#..

        Tile 1171:
        ####...##.
        #..##.#..#
        ##.#..#.#.
        .###.####.
        ..###.####
        .##....##.
        .#...####.
        #.##.####.
        ####..#...
        .....##...

        Tile 1427:
        ###.##.#..
        .#..#.##..
        .#.##.#..#
        #.#.#.##.#
        ....#...##
        ...##..##.
        ...#.#####
        .#.####.#.
        ..#..###.#
        ..##.#..#.

        Tile 1489:
        ##.#.#....
        ..##...#..
        .##..##...
        ..#...#...
        #####...#.
        #..#.#.#.#
        ...#.#.#..
        ##.#...##.
        ..##.##.##
        ###.##.#..

        Tile 2473:
        #....####.
        #..#.##...
        #.##..#...
        ######.#.#
        .#...#.#.#
        .#########
        .###.#..#.
        ########.#
        ##...##.#.
        ..###.#.#.

        Tile 2971:
        ..#.#....#
        #...###...
        #.#.###...
        ##.##..#..
        .#####..##
        .#..####.#
        #..#.#..#.
        ..####.###
        ..#.#.###.
        ...#.#.#.#

        Tile 2729:
        ...#.#.#.#
        ####.#....
        ..#.#.....
        ....#..#.#
        .##..##.#.
        .#.####...
        ####.#.#..
        ##.####...
        ##..#.##..
        #.##...##.

        Tile 3079:
        #.#.#####.
        .#..######
        ..#.......
        ######....
        ####.#..#.
        .#...#.##.
        #.#####.##
        ..#.###...
        ..#.......
        ..#.###...
    """)

    log.test(calc(log, values, 1), 20899048083289)
    log.test(calc(log, values, 2), 273)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

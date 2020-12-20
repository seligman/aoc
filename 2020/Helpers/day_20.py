#!/usr/bin/env python3

from collections import defaultdict

def get_desc():
    return 20, 'Day 20: Jurassic Jigsaw'

def get_spiral(size):
    x, y = -1, 0
    side = 1
    amount = size
    dir = 0

    while True:
        for _ in range(amount):
            if dir == 0:
                x += 1
            elif dir == 1:
                y += 1
            elif dir == 2:
                x -= 1
            elif dir == 3:
                y -= 1
            yield x, y
        dir = (dir + 1) % 4
        side += 1
        if side == 2:
            side = 0
            amount -= 1
            if amount == 0:
                break

def calc(log, values, mode, draw=False):
    from grid import Grid
    grids = []
    temp = []
    name = ""
    for cur in values:
        if cur.startswith("Tile "):
            if len(temp) > 0:
                grids.append(Grid.from_text(temp))
                grids[-1].extra['name'] = name
            temp = []
            name = cur[5:-1]
        elif len(cur) > 0:
            temp.append(cur)
    if len(temp) > 0:
        grids.append(Grid.from_text(temp))
        grids[-1].extra['name'] = name
    side_len = grids[0].width()

    edges = defaultdict(set)
    for grid in grids:
        for edge in grid.all_sides():
            edges[edge].add(grid)

    temp = None
    ret = 1
    for grid in grids:
        shared = 0
        for edge in grid.all_sides():
            if len(edges[edge]) > 1:
                shared += 1
        grid.extra['shared'] = shared
        if shared == 4:
            ret *= int(grid.extra['name'])
            if temp is None:
                temp = grid
    
    if mode == 1:
        return ret

    def get_corners(temp):
        all_temp = set(temp.all_sides())
        for grid_a in [x for x in grids if x.extra['shared'] == 6]:
            if len(set(grid_a.all_sides()) & all_temp):
                for grid_b in [x for x in grids if x.extra['shared'] == 6]:
                    if grid_a.extra['name'] != grid_b.extra['name'] and len(set(grid_b.all_sides()) & all_temp):
                        for _ in temp.enum_rotates():
                            for _ in grid_a.enum_rotates():
                                for _ in grid_b.enum_rotates():
                                    if temp.column(-1) == grid_a.column(0) and temp.row(-1) == grid_b.row(0):
                                        return temp, grid_a, grid_b

    size = 1
    while size * size != len(grids):
        size += 1

    temp, grid_a, grid_b = get_corners(temp)

    if draw:
        drawing = Grid(".")
        drawing[size * side_len, size * side_len] = "."
        drawing.save_frame()
        drawing.blit(temp, 0, 0)
        drawing.save_frame()
        drawing.blit(grid_a, side_len, 0)
        drawing.save_frame()
        drawing.blit(grid_b, 0, side_len)
        drawing.save_frame()

    layout = {
        (0, 0): temp,
        (1, 0): grid_a,
        (0, 1): grid_b,
    }
    used = set([x.extra['name'] for x in layout.values()])

    for x, y in get_spiral(size):
        if (x, y) not in layout:
            for grid in grids:
                valid = True
                if grid.extra['name'] in used:
                    valid = False
                if valid:
                    if (x, y) in {(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)}:
                        if grid.extra['shared'] != 4:
                            valid = False
                    elif x == 0 or y == 0 or x == size - 1 or y == size - 1:
                        if grid.extra['shared'] != 6:
                            valid = False
                    else:
                        if grid.extra['shared'] != 8:
                            valid = False

                if valid:
                    good = True
                    for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if (x + xo, y + yo) in layout:
                            if len(grid.all_sides() & layout[(x + xo, y + yo)].all_sides()) == 0:
                                good = False
                                break
                    if good:
                        for _ in grid.enum_rotates():
                            good = True
                            for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                if (x + xo, y + yo) in layout:
                                    if xo == -1:
                                        match = layout[(x - 1, y)].column(-1) == grid.column(0)
                                    if yo == -1:
                                        match = layout[(x, y - 1)].row(-1) == grid.row(0)
                                    if xo == 1:
                                        match = layout[(x + 1, y)].column(0) == grid.column(-1)
                                    if yo == 1:
                                        match = layout[(x, y + 1)].row(0) == grid.row(-1)
                                    if not match:
                                        good = False
                                        break
                            if good:
                                layout[(x, y)] = grid
                                if draw:
                                    drawing.blit(grid, x * side_len, y * side_len)
                                    drawing.save_frame()
                                used.add(grid.extra['name'])
                                break
                if (x, y) in layout:
                    break

    draw_map = set()

    big = Grid(".")
    for x in range(size):
        for y in range(size):
            for xo in range(1, side_len - 1):
                for yo in range(1, side_len - 1):
                    draw_map.add((xo + x * side_len, yo + y * side_len))
                    big[x * (side_len - 2) + (xo - 1), y * (side_len - 2) + (yo - 1)] = [layout[(x, y)][xo, yo], xo + x * side_len, yo + y * side_len]

    if draw:
        for x in drawing.x_range():
            for y in drawing.y_range():
                if (x, y) not in draw_map:
                    drawing[x, y] = "="
        drawing.save_frame()

    monster = Grid.from_text([
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ])

    todo = []

    for _ in big.enum_rotates():
        any_hit = False
        for x, y in get_spiral(max(big.width(), big.height())):
            hit = True
            for xo in monster.x_range():
                for yo in monster.y_range():
                    if monster[xo, yo] == "#" and big[x + xo, y + yo][0] != "#":
                        hit = False
                        break
                if not hit:
                    break
            if hit:
                if draw:
                    while len(todo) < 7:
                        todo.append([])
                    todo.append([])
                for xo in monster.x_range():
                    for yo in monster.y_range():
                        if monster[xo, yo] == "#":
                            big[x + xo, y + yo][0] = "O"
                            if draw:
                                draw_x, draw_y = big[x + xo, y + yo][1:]
                                drawing[draw_x, draw_y] = "1"
                                todo[-1].append((draw_x, draw_y, "7"))
                                todo[-2].append((draw_x, draw_y, "6"))
                                todo[-3].append((draw_x, draw_y, "5"))
                                todo[-4].append((draw_x, draw_y, "4"))
                                todo[-5].append((draw_x, draw_y, "3"))
                                todo[-6].append((draw_x, draw_y, "2"))
                if draw:
                    for draw_x, draw_y, val in todo.pop(0):
                        drawing[draw_x, draw_y] = val
                    for _ in range(2):
                        drawing.save_frame()
                any_hit = True
        if any_hit:
            break

    if draw:
        while len(todo) > 0:
            for draw_x, draw_y, val in todo.pop(0):
                drawing[draw_x, draw_y] = val
            for _ in range(2):
                drawing.save_frame()

        drawing.draw_frames(color_map={
            '.': (0, 0, 0),
            '#': (21, 21, 128),
            '=': (50, 50, 50),
            'O': (80, 40, 255),
            '1': (255, 255, 255),
            '2': (224, 224, 255),
            '3': (192, 192, 255),
            '4': (160, 160, 255),
            '5': (128, 128, 255),
            '6': (96, 96, 255),
            '7': (80, 40, 255),
        }, repeat_final=30)
        drawing.make_animation(output_name="animation_%02d" % (get_desc()[0],))

    ret = 0
    for x in big.x_range():
        for y in big.x_range():
            if big[x, y][0] == "#":
                ret += 1
    
    return ret

def other_draw(describe, values):
    if describe:
        return "Animate this"

    from dummylog import DummyLog
    calc(DummyLog(), values, 2, draw=2)

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

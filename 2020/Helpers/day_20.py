#!/usr/bin/env python3

from collections import defaultdict
import math

DAY_NUM = 20
DAY_DESC = 'Day 20: Jurassic Jigsaw'

def get_spiral(size):
    pt, dir, amount = complex(-1, 0), 0, size * 2
    dirs = [complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)]
    while amount > 0:
        for _ in range(amount // 2):
            pt += dirs[dir % 4]
            yield int(pt.real), int(pt.imag)
        dir, amount = dir + 1, amount - 1

def normalize(value):
    return min(value, value[::-1])

def enum_edges(grid):
    yield normalize(grid.row(0))
    yield normalize(grid.row(-1))
    yield normalize(grid.column(0))
    yield normalize(grid.column(-1))

def calc(log, values, mode, draw=False):
    from grid import Grid
    grids, temp, name = [], [], ""
    for cur in values:
        if cur.startswith("Tile "):
            if len(temp) > 0:
                grids.append(Grid.from_text(temp))
                grids[-1].extra = {"name": name, "shared": 0, "edges": set()}
            temp = []
            name = cur[5:-1]
        elif len(cur) > 0:
            temp.append(cur)
    if len(temp) > 0:
        grids.append(Grid.from_text(temp))
        grids[-1].extra = {"name": name, "shared": 0, "edges": set()}
    side_len = grids[0].width()
    size = int(math.sqrt(len(grids)))

    edges = defaultdict(set)
    for grid in grids:
        for edge in enum_edges(grid):
            edges[edge].add(grid)
            grid.extra['edges'].add(edge)

    for cur in edges.values():
        if len(cur) > 1:
            for grid in cur:
                grid.extra['shared'] += 1

    ret = 1
    temp = None
    for grid in grids:
        if grid.extra['shared'] == 2:
            ret *= int(grid.extra['name'])
            if temp is None:
                temp = grid
    if mode == 1:
        return ret

    bail = 2 if draw else 1
    for _ in temp.enum_rotates():
        if len(edges[normalize(temp.column(-1))]) == 2 and len(edges[normalize(temp.row(-1))]) == 2:
            bail -= 1
            if bail == 0:
                break

    if draw:
        drawing = Grid([None, (0,0,0)])
        drawing.save_frame()
        drawing.blit(temp, 0, 0, 
            color_map={'.': (0,0,0), '#': (21, 21, 128)},
            text_map={'.': None, '#': None},
        )
        drawing.save_frame()

    layout = {
        (0, 0): temp,
    }
    used = set([x.extra['name'] for x in layout.values()])

    def get_shared(grid):
        ret = set()
        for cur in grid.extra['edges']:
            for sub in edges[cur]:
                ret.add(sub)
        ret.remove(grid)
        return ret

    for x, y in get_spiral(size):
        if (x, y) not in layout:
            test = None
            for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (x + xo, y + yo) in layout:
                    temp = get_shared(layout[(x + xo, y + yo)])
                    if test is None:
                        test = temp
                    else:
                        test &= temp

            for grid in test:
                valid = True
                if grid.extra['name'] in used:
                    valid = False

                if valid and grid.extra['shared'] != (4 - (1 if x in {0, size -1} else 0) - (1 if y in {0, size -1} else 0)):
                    valid = False

                if valid:
                    for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if (x + xo, y + yo) in layout:
                            if len(grid.extra['edges'] & layout[(x + xo, y + yo)].extra['edges']) == 0:
                                valid = False
                                break
                
                if valid:
                    for _ in grid.enum_rotates():
                        valid = True
                        for xo, yo, side_type in [(-1, 0, 'column'), (1, 0, 'column'), (0, -1, 'row'), (0, 1, 'row')]:
                            if (x + xo, y + yo) in layout:
                                if grid.side(side_type, 0 if xo+yo < 0 else -1) != layout[(x + xo, y + yo)].side(side_type, -1 if xo+yo < 0 else 0):
                                    valid = False
                                    break

                        if valid:
                            layout[(x, y)] = grid
                            if draw:
                                drawing.blit(grid, x * side_len, y * side_len,
                                    color_map={'.': (0,0,0), '#': (21, 21, 128)},
                                    text_map={'.': None, '#': None},
                                )
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
                    drawing[x, y] = [None, (50, 50, 50)]
        drawing.save_frame()

    monster = Grid.from_text([
        r"                  . ",
        r"\    __    __    /O>",
        r" \  /  \  /  \  /   ",
    ])

    todo = []

    for _ in big.enum_rotates():
        any_hit = False
        for x, y in get_spiral(max(big.width(), big.height())):
            hit = True
            for xo in monster.x_range():
                for yo in monster.y_range():
                    if monster[xo, yo] != " " and big[x + xo, y + yo][0] != "#":
                        hit = False
                        break
                if not hit:
                    break
            if hit:
                if draw:
                    while len(todo) < 12:
                        todo.append([])
                    todo.append([])
                for xo in monster.x_range():
                    for yo in monster.y_range():
                        if monster[xo, yo] != " ":
                            big[x + xo, y + yo][0] = "O"
                            if draw:
                                draw_x, draw_y = big[x + xo, y + yo][1:]
                                drawing[draw_x, draw_y] = [monster[xo, yo], (255, 255, 255)]
                                todo[-11].append((draw_x, draw_y, [monster[xo, yo], (224, 224, 255)]))
                                todo[-10].append((draw_x, draw_y, [monster[xo, yo], (192, 192, 255)]))
                                todo[-9].append((draw_x, draw_y, [monster[xo, yo], (160, 160, 255)]))
                                todo[-8].append((draw_x, draw_y, [monster[xo, yo], (128, 128, 255)]))
                                todo[-7].append((draw_x, draw_y, [monster[xo, yo], (96, 96, 192)]))
                                todo[-6].append((draw_x, draw_y, [monster[xo, yo], (64, 64, 160)]))
                                todo[-5].append((draw_x, draw_y, [monster[xo, yo], (32, 32, 128)]))
                                todo[-4].append((draw_x, draw_y, [monster[xo, yo], (0, 0, 96)]))
                                todo[-3].append((draw_x, draw_y, [monster[xo, yo], (0, 0, 64)]))
                                todo[-2].append((draw_x, draw_y, [monster[xo, yo], (0, 0, 32)]))
                                todo[-1].append((draw_x, draw_y, [monster[xo, yo], (0, 0, 0)]))
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

        drawing.draw_frames(repeat_final=30, font_size=6)
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
    calc(DummyLog(), values, 2, draw=True)

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

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

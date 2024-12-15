#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Warehouse Woes'

def calc(log, values, mode):
    from grid import Grid, Point
    grid = []
    moves = None
    for cur in values:
        if len(cur) == 0:
            moves = []
        elif moves is None:
            grid.append(cur)
        else:
            moves.append(cur)
    
    if mode == 2:
        for i in range(len(grid)):
            temp = ""
            for cur in grid[i]:
                if cur in {"#", "."}:
                    temp += cur + cur
                elif cur == "O":
                    temp += "[]"
                elif cur == "@":
                    temp += "@."
                else:
                    raise Exception()
            grid[i] = temp

    grid = Grid.from_text(grid)
    for xy in grid.xy_range():
        if grid[xy] == "@":
            robot = Point(xy)
            grid[xy] = "."
            break
    
    for row in moves:
        for cur in row:
            x, y, up_down = {"^": (0, -1, True), "v": (0, 1, True), "<": (-1, 0, False), ">": (1, 0, False)}[cur]
            d = Point(x, y)
            to_move = []
            empty = 0
            if mode == 2 and up_down:
                temp = robot + Point(0, 0)
                row = [temp]
                while True:
                    all_empty = True
                    for cur in row:
                        if grid[cur + d] != ".":
                            all_empty = False
                    if all_empty:
                        empty += 1
                        break

                    any_wall = False
                    for cur in row:
                        if grid[cur + d] == "#":
                            any_wall = True
                    if any_wall:
                        break

                    hit = set()
                    for cur in row:
                        if grid[cur + d] == "[":
                            hit.add(cur + d)
                            hit.add(cur + d + Point(1, 0))
                        elif grid[cur + d] == "]":
                            hit.add(cur + d)
                            hit.add(cur + d - Point(1, 0))
                    row = []
                    for cur in hit:
                        row.append(cur)
                        to_move.append((cur, grid[cur]))
                    temp += d

            else:
                temp = robot + d
                while True:
                    if grid[temp] == ".":
                        empty += 1
                        break
                    elif grid[temp] == "O":
                        to_move.append((temp, grid[temp]))
                    elif grid[temp] in {"[", "]"}:
                        to_move.append((temp, grid[temp]))
                    else:
                        break
                    temp += d

            if empty > 0:
                robot += d
                for cur, _ in to_move:
                    grid[cur] = "."
                for cur, val in to_move:
                    grid[cur + d] = val

    ret = 0
    for xy in grid.xy_range():
        if grid[xy] in {"O", "["}:
            ret += xy[1] * 100 + xy[0]
    return ret

def test(log):
    values = log.decode_values("""
        ##########
        #..O..O.O#
        #......O.#
        #.OO..O.O#
        #..O@..O.#
        #O#..O...#
        #O..O..O.#
        #.OO.O.OO#
        #....O...#
        ##########

        <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
        vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
        ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
        <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
        ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
        ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
        >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
        <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
        ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
        v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """)

    log.test(calc(log, values, 1), '10092')
    log.test(calc(log, values, 2), '9021')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

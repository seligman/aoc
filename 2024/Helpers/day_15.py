#!/usr/bin/env python3

DAY_NUM = 15
DAY_DESC = 'Day 15: Warehouse Woes'

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def calc(log, values, mode, draw=False):
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

    if draw:
        shadow = Grid.from_text(grid)
        shadow.ensure_ratio(16/4.5)
        shadow.pad(2)
        shadow.save_frame()

    grid = Grid.from_text(grid)
    for xy in grid.xy_range():
        if grid[xy] == "@":
            robot = Point(xy)
            grid[xy] = "."
            break
    
    for row in moves:
        for cur in row:
            d, up_down = {
                "^": (Point(0, -1), True), 
                "v": (Point(0, 1), True), 
                "<": (Point(-1, 0), False), 
                ">": (Point(1, 0), False),
            }[cur]
            to_move = []
            to_push = [robot]
            while True:
                if all(grid[cur + d] == "." for cur in to_push):
                    break
                if any(grid[cur + d] == "#" for cur in to_push):
                    to_move = None
                    break

                hit = set()
                for cur in to_push:
                    if up_down and grid[cur + d] == "[":
                        hit.add(cur + d)
                        hit.add(cur + d + Point(1, 0))
                    elif up_down and grid[cur + d] == "]":
                        hit.add(cur + d)
                        hit.add(cur + d - Point(1, 0))
                    elif grid[cur + d] in {"O", "[", "]"}:
                        hit.add(cur + d)

                to_push = hit
                to_move.extend((cur, grid[cur]) for cur in hit)

            if to_move is not None:
                if draw:
                    shadow[robot] = "."
                robot += d
                for cur, _ in to_move:
                    grid[cur] = "."
                for cur, val in to_move:
                    grid[cur + d] = val
                if draw:
                    for cur, _ in to_move:
                        shadow[cur] = "."
                    for cur, val in to_move:
                        shadow[cur + d] = val
                    shadow[robot] = "star"
                    shadow.save_frame()

    ret = 0
    for xy in grid.xy_range():
        if grid[xy] in {"O", "["}:
            ret += xy[1] * 100 + xy[0]

    if draw:
        shadow.ease_frames(rate=15, secs=60)
        shadow.draw_frames(show_lines=False, cell_size=(10, 20))

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

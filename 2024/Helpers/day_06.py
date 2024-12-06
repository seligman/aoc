#!/usr/bin/env python3

DAY_NUM = 6
DAY_DESC = 'Day 6: Guard Gallivant'

def calc(log, values, mode, draw=False):
    from grid import Grid
    grid = Grid.from_text(values, default="X")
    if draw:
        shadow = Grid.from_text(values, default="X")
        trail = []
        skip = 0

    rots = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    rot = 0

    for x, y in grid.xy_range():
        if grid[x, y] == "^":
            start_x, start_y = x, y
            pos_x, pos_y = x, y
            if draw:
                shadow[x, y] = "*"
                trail.append((x, y))
            break
    
    seen = set()
    while True:
        nx, ny = pos_x + rots[rot][0], pos_y + rots[rot][1]
        if grid[nx, ny] == "#":
            rot = (rot + 1) % 4
        elif grid[nx, ny] in {".", "^"}:
            seen.add((nx, ny))
            pos_x, pos_y = nx, ny
            if draw:
                trail.append((nx, ny))
                while len(trail) > 25:
                    trail.pop(0)
                for i, xy in enumerate(trail):
                    perc = (i / (len(trail) - 1)) * 0.5 + 0.5
                    shadow[xy] = [" ", (int(255 * perc), int(215 * perc), 0)]
                skip += 1
                if skip % 4 == 0:
                    shadow.save_frame()
        elif grid[nx, ny] == "X":
            break

    if mode == 1:
        if draw:
            shadow.save_frame()
            shadow.draw_frames(show_lines=False)
        return len(seen)
    
    ret = 0
    for block_x, block_y in seen:
        grid[block_x, block_y] = "#"
        rot = 0
        pos_x, pos_y = start_x, start_y

        loop = set()
        while True:
            nx, ny = pos_x + rots[rot][0], pos_y + rots[rot][1]
            if grid[nx, ny] == "#":
                rot = (rot + 1) % 4
            elif grid[nx, ny] in {".", "^"}:
                key = (nx, ny, rot)
                if key in loop:
                    ret += 1
                    break
                loop.add(key)
                pos_x, pos_y = nx, ny
            elif grid[nx, ny] == "X":
                break

        grid[block_x, block_y] = "."
    return ret

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def test(log):
    values = log.decode_values("""
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """)

    log.test(calc(log, values, 1), '41')
    log.test(calc(log, values, 2), '6')

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

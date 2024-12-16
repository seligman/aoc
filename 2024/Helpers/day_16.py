#!/usr/bin/env python3

DAY_NUM = 16
DAY_DESC = 'Day 16: Reindeer Maze'

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
    grid = Grid.from_text(values)

    for xy in grid.xy_range():
        if grid[xy] == "S":
            grid[xy] = "."
            start = Point(xy)
        elif grid[xy] == "E":
            stop = Point(xy)
            grid[xy] = "."

    dirs = [Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]
    todo = [(start, 0, 0, set())]
    seen = set()
    target = None
    set_target = False

    to_show = set()

    scores = {}

    while len(todo) > 0:
        best = None
        best_i = None
        for i, (_, _, score, _) in enumerate(todo):
            if best is None or score < best:
                best = score
                best_i = i
        xy, d, score, path = todo.pop(best_i)
        if xy not in scores:
            scores[xy] = score
            if grid[xy] == "." and xy not in path:
                path = path | set([xy])
                if xy == stop:
                    if mode == 1:
                        return score
                todo.append((xy + dirs[d % 4], d, score + 1, path))
                todo.append((xy + dirs[(d+1) % 4], d+1, score + 1001, path))
                todo.append((xy + dirs[(d+3) % 4], d+3, score + 1001, path))



    if draw:
        all_paths = []

    todo = [(start, 0, 0, [])]
    while len(todo) > 0:
        xy, d, score, path = todo.pop(best_i)
        if grid[xy] == "." and score <= scores[xy] + 1001:
                path = path[:] + [xy]
                if xy == stop:
                    to_show |= set(path)
                    if draw:
                        all_paths.append(path)
                else:
                    todo.append((xy + dirs[d % 4], d, score + 1, path))
                    todo.append((xy + dirs[(d+1) % 4], d+1, score + 1001, path))
                    todo.append((xy + dirs[(d+3) % 4], d+3, score + 1001, path))

    if draw:
        grid[start] = "star"
        grid[stop] = "star"
        grid.ensure_ratio(16/9)
        grid.pad(2)
        grid.save_frame()

        all_paths = [list(x) for x in all_paths]
        last = []
        while len(all_paths[0]):
            for xy in last:
                grid[xy] = (" ", (90, 90, 200))

            for cur in all_paths:
                xy = cur.pop(0)
                grid[xy] = "star"
                last.append(xy)
            
            grid.save_frame()

        if draw:
            grid.ease_frames(rate=15, secs=10)
            grid.draw_frames(show_lines=False)

    return len(to_show) 

def test(log):
    values = log.decode_values("""
        ###############
        #.......#....E#
        #.#.###.#.###.#
        #.....#.#...#.#
        #.###.#####.#.#
        #.#.#.......#.#
        #.#.#####.###.#
        #...........#.#
        ###.#.#####.#.#
        #...#.....#.#.#
        #.#.#.###.#.#.#
        #.....#...#.#.#
        #.###.#.#.#.#.#
        #S..#.....#...#
        ###############
    """)

    log.test(calc(log, values, 1), '7036')
    log.test(calc(log, values, 2), '45')

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

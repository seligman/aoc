#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'Hoof It'

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
    import random
    grid = Grid.from_text(values)
    if draw:
        colors = []
        for _ in range(32):
            colors.append((random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))

        shadow = Grid.from_text(values, default=".")
        shadow.ensure_ratio(16/9)
        shadow.pad(2)

        def reset_shadow():
            nonlocal shadow, grid
            for xy in grid.xy_range():
                color = int(grid[xy])
                color = color / 9
                color = (int(255 * color), 0, int(255 * (1 - color)))
                shadow[xy] = [" ", color]
        
        def get_msg(heads, score):
            return [f"Trailheads: {heads:4d}, Score: {score:4d}"]
        reset_shadow()

    starts = set()
    for xy in grid.xy_range():
        if grid[xy] == "0":
            starts.add(Point(xy))
    
    ret = 0
    seen = 0
    
    for i, start in enumerate(starts):
        seen += 1
        if draw:
            shadow.save_frame(get_msg(seen, ret))
            shadow[start] = (" ", colors[i % len(colors)])
        todo = [(start, 1)]
        scores = set()
        scores_all = 0
        frame_at = 2

        while len(todo) > 0:
            xy, height = todo.pop(0)
            if draw:
                shadow[xy] = (" ", colors[i % len(colors)])
                if frame_at == height:
                    frame_at += 1
                    shadow.save_frame(get_msg(seen, ret))

            if height == 10:
                scores.add(xy)
                scores_all += 1
            for oxy in Grid.get_dirs(2, diagonal=False):
                temp = xy + Point(oxy)
                if grid[temp] == str(height):
                    todo.append((temp, height + 1))

        if mode == 1:
            ret += len(scores)
        else:
            ret += scores_all

    if draw:
        shadow.ease_frames(15, 60)
        shadow.draw_frames(show_lines=False)

    return ret

def test(log):
    values = log.decode_values("""
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
    """)

    log.test(calc(log, values, 1), '36')
    log.test(calc(log, values, 2), '81')

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

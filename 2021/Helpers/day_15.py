#!/usr/bin/env python3

from collections import defaultdict
import heapq

DAY_NUM = 15
DAY_DESC = 'Day 15: Chiton'

class Step:
    def __init__(self, xy, cost, trail):
        self.xy = xy
        self.cost = cost
        self.trail = trail
    def __eq__(self, other):
        return self.cost.__eq__(other.cost)
    def __lt__(self, other):
        return self.cost.__lt__(other.cost)

def calc(log, values, mode, draw=False, frames=300, show_all_trails=False, return_trail=False):
    colors = {
        1: (12, 7, 134),
        2: (74, 2, 160),
        3: (124, 2, 167),
        4: (168, 34, 150),
        5: (202, 70, 120),
        6: (229, 107, 92),
        7: (247, 147, 65),
        8: (253, 195, 40),
        9: (239, 248, 33),
        'noted': (90, 90, 90),
        'path': (255, 255, 255),
    }
    from grid import Grid
    grid = Grid.from_text(values)

    final_trail, total_steps = None, 0
    if draw:
        final_trail, total_steps = calc(log, values, mode, return_trail=True)
        final_trail = set(final_trail)

    for xy in grid.grid:
        grid.grid[xy] = int(grid.grid[xy])

    if mode == 2:
        w, h = grid.width(), grid.height()
        pts = [(x, y, int(grid[x, y])) for x, y in grid.grid]
        for ox, oy in [(x // 5, x % 5) for x in range(1, 25)]:
            for x, y, val in pts:
                grid[x + ox * w, y + oy * h] = ((val - 1 + ox + oy) % 9) + 1

    todo = [Step((0, 0), 0, [(0, 0)])]
    heapq.heapify(todo)

    seen = set([(0, 0)])
    cur_point = 0
    if draw:
        from animate import ease
        next_show = [int(ease(x / frames) * total_steps) for x in range(frames+1)]
    all_trails = defaultdict(int)
    if show_all_trails:
        for x in range(256):
            colors[f"gray_{x}"] = (x, x, x)
            colors[f"red_{x}"] = (x, 100, 100)

    while len(todo):
        state = heapq.heappop(todo)
        xy, cost, trail = state.xy, state.cost, state.trail
        for oxy in grid.neighbors(state.xy, valid_only=True):
            if oxy not in seen:
                seen.add(oxy)
                extra = grid[oxy]
                grid.grid[oxy] = 'noted'
                if draw:
                    show = False
                    if oxy == (grid.width() - 1, grid.height() - 1):
                        show = True
                    elif len(next_show) and cur_point >= next_show[0]:
                        next_show.pop(0)
                        show = True
                    if show:
                        log(f"Cur Point: {cur_point}, {len(next_show)} left.")
                        grid.save_frame()
                        temp = grid.frames[-1][0]
                        if show_all_trails:
                            if len(all_trails) > 0:
                                bright = max(all_trails.values())
                                for xy, val in all_trails.items():
                                    if xy in final_trail:
                                        temp[xy] = f"red_{int((val / bright) * 127 + 128)}"
                                    else:
                                        temp[xy] = f"gray_{int((val / bright) * 127 + 128)}"
                                all_trails = defaultdict(int)
                        else:
                            for xy in state.trail:
                                temp[xy] = 'path'
                    else:
                        if show_all_trails:
                            for xy in state.trail:
                                all_trails[xy] += 1
                cur_point += 1
                if oxy == (grid.width() - 1, grid.height() - 1):
                    if draw:
                        if show_all_trails:
                            grid.save_frame()
                            temp = grid.frames[-1][0]
                            for xy in state.trail:
                                temp[xy] = 'red_255'
                        grid.draw_frames(color_map=colors, show_lines=False, cell_size=(1, 1))
                    state.cost += extra
                    if return_trail:
                        return state.trail, cur_point
                    return state.cost
                cur_cost = state.cost + extra
                next_trail = None
                if draw or return_trail:
                    next_trail = state.trail + [oxy]
                heapq.heappush(todo, Step(oxy, cur_cost, next_trail))

def other_draw(describe, values):
    return draw_internal(describe, values, "Animate this")

def other_draw_long(describe, values):
    return draw_internal(describe, values, "Animate this with around 9000 frames", frames=9000, extra="_long")

def other_draw_trails(describe, values):
    return draw_internal(describe, values, "Animate this showing all of the trails", trails=True, extra="_trails")

def draw_internal(describe, values, desc, trails=False, frames=900, extra=""):
    if describe:
        return desc
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True, frames=frames, show_all_trails=trails)
    animate.create_mp4(DAY_NUM, rate=30, extra=extra)

def test(log):
    values = log.decode_values("""
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
    """)

    log.test(calc(log, values, 1), 40)
    log.test(calc(log, values, 2), 315)

def run(log, values):
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

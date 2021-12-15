#!/usr/bin/env python3

from animate import ease

def get_desc():
    return 15, 'Day 15: Chiton'

def calc(log, values, mode, draw=False, frames=300):
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

    for xy in grid.grid:
        grid.grid[xy] = int(grid.grid[xy])

    if mode == 2:
        w, h = grid.width(), grid.height()
        pts = [(x, y, int(grid[x, y])) for x, y in grid.grid]
        for ox, oy in [(x // 5, x % 5) for x in range(1, 25)]:
            for x, y, val in pts:
                grid[x + ox * w, y + oy * h] = ((val - 1 + ox + oy) % 9) + 1

    todo = [((0, 0), 0, [(0, 0)])]
    seen = set([(0, 0)])
    cur_point = 0
    # 249998 is how many cur_points a full run finds
    next_show = [int(ease(x / frames) * 249998) for x in range(frames+1)]
    while len(todo):
        todo.sort(key=lambda x: x[1])
        xy, cost, trail = todo.pop(0)
        for oxy in grid.neighbors(xy, valid_only=True):
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
                        temp = {}
                        for xy in trail:
                            temp[xy] = grid[xy]
                            grid[xy] = 'path'
                        grid.save_frame()
                        for xy, val in temp.items():
                            grid[xy] = val
                    cur_point += 1
                if oxy == (grid.width() - 1, grid.height() - 1):
                    if draw:
                        grid.draw_frames(color_map=colors, show_lines=False, cell_size=(1, 1))
                    cost += extra
                    return cost
                todo.append((oxy, cost + extra, trail + [oxy]))

def other_draw(describe, values):
    return draw_internal(describe, values, 300, "")

def other_draw_long(describe, values):
    return draw_internal(describe, values, 9000, "_long")

def draw_internal(describe, values, frames, extra):
    if describe:
        return f"Animate this with {frames} frames"
    from dummylog import DummyLog
    import animate

    animate.prep()
    calc(DummyLog(), values, 2, draw=True, frames=frames)
    animate.create_mp4(get_desc(), rate=30, extra=extra)

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
    log(calc(log, values, 1))
    log(calc(log, values, 2))

#!/usr/bin/env python

def get_desc():
    return 10, 'Day 10: Monitoring Station'


def calc(log, values, animate=False):
    import math
    from grid import Grid
    
    grid = Grid(default=".")
    y = 0
    for row in values:
        x = 0
        for cur in row:
            grid.set(x, y, cur)
            x += 1
        y += 1

    best_hits = 0
    best_xy = 0

    def get_angles(x, y, width, height):
        ret = {}
        for x1 in range(width):
            for y1 in range(height):
                if (x1, y1) != (x, y):
                    ang = math.atan2(x1 - x, y1 - y)
                    if ang not in ret:
                        ret[ang] = []
                    ret[ang].append((x1, y1))
        for key in ret:
            ret[key].sort(key=lambda z: (x-z[0])*(x-z[0])+(y-z[1])*(y-z[1]))
        return [(x, ret[x]) for x in sorted(ret, reverse=True)]

    for x in range(grid.width()):
        for y in range(grid.height()):
            if grid.get(x, y) == "#":
                hits = 0
                spin = get_angles(x, y, grid.width(), grid.height())
                for _, angle in spin:
                    for xo, yo in angle:
                        if grid.get(xo, yo) == "#":
                            hits += 1
                            break

                if hits > best_hits:
                    best_hits = hits
                    best_xy = (x, y)

    x, y = best_xy
    destroyed = 0
    
    if animate:
        grid.set(x, y, "Star")

    spin = get_angles(x, y, grid.width(), grid.height())
    to_clear = []
    xo, yo = x, y
    while destroyed < 200 or animate:
        clean = True
        next_dump = math.radians(180)
        for at, angle in spin:
            if at <= next_dump:
                if animate:
                    grid.save_frame(extra={
                        'angle': next_dump, 
                        'angle2': next_dump + math.radians(10), 
                        'x': xo, 
                        'y': yo,
                    })
                    for x, y in to_clear:
                        grid.set(x, y, ".")
                    to_clear = []
                next_dump -= math.radians(10)
            for x, y in angle:
                if grid.get(x, y) in {"#", "target"}:
                    destroyed += 1
                    grid.set(x, y, "star")
                    if animate:
                        to_clear.append((x, y))
                    if destroyed == 200:
                        log.show("Destroyed #200 at %d, %d == %d" % (x, y, x * 100 + y))
                    clean = False
                    break
        if clean:
            break

    if animate:
        Grid.clear_frames()
        grid.save_frame()
        def draw_line(d, extra):
            if extra is not None:
                pts = []
                pts.append((
                    math.sin(extra['angle']) * 1000.0 + extra['x_calc'],
                    math.cos(extra['angle']) * 1000.0 + extra['y_calc'],
                ))
                pts.append((
                    math.sin(extra['angle2']) * 1000.0 + extra['x_calc'],
                    math.cos(extra['angle2']) * 1000.0 + extra['y_calc'],
                ))
                pts.append((
                    extra['x_calc'],
                    extra['y_calc'],
                ))
                d.polygon(pts, fill=(128, 128, 128, 128))
        grid.draw_frames(repeat_final=30, extra_callback=draw_line)

    return best_hits

def other_animate(describe, values):
    if describe:
        return "Animate frames"
    
    from grid import Grid
    from dummylog import DummyLog
    calc(DummyLog(), values, animate=True)
    Grid.make_animation(output_name="animation_%02d" % (get_desc()[0],), file_format="mp4")
    print("Done, created animation...")


def test(log):
    values = log.decode_values("""
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
    """)

    ret, expected = calc(log, values), 210
    log.show("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def run(log, values):
    log.show(calc(log, values))

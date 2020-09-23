#!/usr/bin/env python

def get_desc():
    return 11, 'Day 11: Space Police'


def calc(log, values, mode, animate=False):
    from program import Program
    from grid import Grid
    from collections import deque
    ticker = [int(x) for x in values[0].split(",")]
    program = Program(ticker, log)

    x, y = 0, 0
    changed = 0
    dirs = deque([(0, -1), (1, 0), (0, 1), (-1, 0)])
    grid = Grid()
    if mode == 2:
        grid.set(1, 0, 0)

    while True:
        if len(program.output) > 0:
            paint, change_dir = program.get_output(2)
            dirs.rotate(-1 if change_dir == 1 else 1)

            if not grid.value_isset(x, y):
                changed += 1

            if animate:
                old = grid.get(x, y)
                grid.set("Star", x, y)
                grid.save_frame()
                grid.set(old, x, y)

            grid.set(paint, x, y)

            x += dirs[0][0]
            y += dirs[0][1]

        program.add_to_input(grid.get(x, y))
        program.tick_till_end()
        if not program.flag_running:
            break

    if mode == 2:
        log("")
        grid.show_grid(log)
        grid.decode_grid(log)
        log("")

    if animate:
        Grid.clear_frames()
        grid.draw_frames(repeat_final=40)

    return changed


def other_animate(describe, values):
    if describe:
        return "Animate frames"
    
    from grid import Grid
    from dummylog import DummyLog
    calc(DummyLog(), values, 2, animate=True)
    Grid.make_animation(output_name="animation_%02d" % (get_desc()[0],), file_format="mp4")
    print("Done, created animation...")


def test(log):
    return True


def run(log, values):
    log("Part 1: " + str(calc(log, values, 1)))
    calc(log, values, 2)

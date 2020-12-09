#!/usr/bin/env python3

def get_desc():
    return 15, 'Day 15: Oxygen System'


def calc(log, values, animate=False):
    from grid import Grid
    from program import Program
    from collections import deque

    grid = Grid("~")
    grid.set(".", 0, 0)

    # Let the program run it's initialization
    ticker = [int(x) for x in values[0].split(",")]
    program = Program(ticker, log)
    program.tick_till_end()

    todo = deque()
    todo.appendleft((program.ticker.copy(), 0, 0, 0))

    dirs = [(0, -1, 1), (0, 1, 2), (-1, 0, 3), (1, 0, 4)]
    sensor_x, sensor_y = None, None

    extra_text = ["", ""]

    last_steps = 0
    while len(todo):
        ticker, steps, x, y = todo.pop()
        if steps > last_steps:
            grid.save_frame(extra_text=extra_text[:])
            for key in grid.grid:
                if grid.grid[key] == "Robot":
                    grid.grid[key] = "."
            last_steps = steps
        for xo, yo, value in dirs:
            if (x + xo, y + yo) not in grid.grid:
                program = Program(ticker.copy(), log)
                program.add_to_input(value)
                program.tick_till_end()
                if program.last_output == 0:
                    grid.set("#", x + xo, y + yo)
                else:
                    grid.set("Robot", x + xo, y + yo)
                    todo.appendleft((program.ticker, steps + 1, x + xo, y + yo))
                    if sensor_x is None:
                        extra_text[0] = "Sensor: |%04d| steps" % (steps + 1,)
                    if program.last_output == 2 and sensor_x is None:
                        grid.set("Oxygen", x + xo, y + yo)
                        sensor_x, sensor_y = x + xo, y + yo
                        log("Steps to sensor: " + str(steps + 1))

    last_steps = 0
    todo.appendleft((sensor_x, sensor_y, 0))
    while len(todo):
        x, y, steps = todo.pop()
        if steps > last_steps:
            extra_text[1] = "Oxygen: |%04d| steps" % (steps,)
            grid.save_frame(extra_text=extra_text[:])
            last_steps = steps
        for xo, yo, _value in dirs:
            if grid.get(x + xo, y + yo) in {".", "Robot"}:
                grid.set("Flood", x + xo, y + yo)
                todo.appendleft((x + xo, y + yo, steps + 1))

    log("Steps to flood oxygen: " + str(last_steps))
    
    if animate:
        Grid.clear_frames()

        grid.draw_frames(color_map={
            "~": (64, 64, 64),
            '.': (0, 0, 0),
            '#': (255, 255, 255),
            'Robot': (192, 192, 0),
            'Oxygen': (32, 32, 255),
            'Flood': (32, 32, 192),
        }, repeat_final=30)

        Grid.make_animation(output_name="animation_%02d" % (get_desc()[0],), file_format="mp4")


def test(log):
    return True


def other_animate(describe, values):
    if describe:
        return "Animate the work"
    from dummylog import DummyLog
    calc(DummyLog(), values, animate=True)
    print("Done, created animation...")


def other_debug(describe, values):
    if describe:
        return "Debug program"

    from program import Program
    Program.debug(values[0])


def run(log, values):
    calc(log, values)

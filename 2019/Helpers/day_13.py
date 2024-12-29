#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Care Package'

def calc(log, values, play_game, animate=False):
    from program import Program
    from grid import Grid

    ticker = [int(x) for x in values[0].split(",")]
    program = Program(ticker, log)

    if play_game:
        program.ticker[0] = 2
    score = 0
    grid = Grid()

    if not play_game:
        program.tick_till_end()
        while len(program.output) >= 3:
            x, y, tile = program.get_output(3)
            if x != -1:
                grid.set(tile, x, y)
    elif not animate:
        while program.flag_running:
            program.tick_till_end()

            while len(program.output) >= 3:
                x, y, tile = program.get_output(3)
                if tile == 4:
                    ball = (x, y)
                if tile == 3:
                    paddle = (x, y)

                if x == -1:
                    score = tile

            if program.flag_input_dry:
                if ball[0] < paddle[0]:
                    program.add_to_input(-1)
                elif ball[0] > paddle[0]:
                    program.add_to_input(1)
                else:
                    program.add_to_input(0)
    else:
        ball = (0, 0)
        paddle = (0, 0)

        while program.flag_running:
            copy = program.make_copy()
            ball_trail = []
            while copy.flag_running:
                copy.tick()
                if copy.flag_input_dry:
                    copy.add_to_input(0)
                    ball_trail.append(ball)
                    if paddle is not None and len(ball_trail) > 2:
                        if ball_trail[-1][1] == paddle[1] - 1 and ball_trail[-2][1] == paddle[1] - 2:
                            break
                elif len(copy.output) == 3:
                    x, y, tile = copy.get_output(3)
                    if tile == 3:
                        paddle = (x, y)
                    elif tile == 4:
                        ball = (x, y)

            paddle_move = None
            steps = 0
            while program.flag_running:
                program.tick()

                while len(program.output) >= 3:
                    x, y, tile = program.get_output(3)
                    if tile == 4:
                        ball = (x, y)
                    if tile == 3:
                        paddle = (x, y)

                    if x == -1:
                        score = tile
                    else:
                        grid.set(tile, x, y)
                
                if not program.flag_running:
                    break

                if steps == len(ball_trail):
                    break

                if program.flag_input_dry:
                    grid.save_frame(extra_text=[
                        "SCORE: | %07d" % (score,)
                    ])

                    steps += 1
                    if paddle_move is None:
                        paddle_move = paddle[0] - ball_trail[-1][0]

                    if steps > 0 and copy.flag_running and paddle_move != 0:
                        if paddle_move > 0:
                            program.add_to_input(-1)
                            paddle_move -= 1
                        elif paddle_move < 0:
                            program.add_to_input(1)
                            paddle_move += 1
                    else:
                        program.add_to_input(0)

    if animate:
        grid.save_frame(extra_text=[
            "SCORE: | %07d |   HIGH SCORE !!" % (score,),
            "GAME OVER"
        ])
        Grid.clear_frames()
        grid.draw_frames(color_map={
            0: (0, 0, 0), 
            1: (255, 255, 255), 
            2: (128, 128, 128), 
            3: (255, 64, 64), 
            4: (128, 128, 255), 
        }, repeat_final=30 * 5)
        Grid.make_animation(file_format="mp4", output_name="animation_%02d" % (get_desc()[0],))

    if play_game:
        return score

    count = 0
    for cur in grid.grid:
        value = grid.grid[cur]
        if value in {2}:
            count += 1

    return count

def test(log):
    return True

def other_animate(describe, values):
    if describe:
        return "Animate frames"
    
    from dummylog import DummyLog
    calc(DummyLog(), values, True, animate=True)
    print("Done, created animation...")

def run(log, values):
    log("Part 1: " + str(calc(log, values, False)))
    log("Part 2: " + str(calc(log, values, True)))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2019/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

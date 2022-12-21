#!/usr/bin/env python3

# Animation: https://imgur.com/a/Z02NxRl
# Beep Beep:
#   Instructions: https://github.com/seligman/aoc/blob/master/2022/Puzzles/day_10_input_alt_01.txt
#   Animation:    https://imgur.com/a/ZoLPltM
# Christmas Tree:
#   Instructions: https://github.com/seligman/aoc/blob/master/2022/Puzzles/day_10_input_alt_02.txt
#   Animation:    https://imgur.com/a/OWCDnlP

DAY_NUM = 10
DAY_DESC = 'Day 10: Cathode-Ray Tube'

def calc(log, values, mode, draw=False, decode=False):
    from grid import Grid
    from program import Program
    grid = Grid()
    program = Program(values)
    ret = 0

    for _ in program.run():
        temp = program.cycles - 1
        if draw:
            grid[(temp % 40, temp // 40)] = "star"
            grid.save_frame((
                program.ins, 
                f"Cycle: {program.cycles}", 
                f"register X: {program.regs['x']}",
            ))

        if abs((temp % 40) - program.regs['x']) <= 1:
            grid[(temp % 40, temp // 40)] = "#"
        else:
            grid[(temp % 40, temp // 40)] = "."

        if (program.cycles + 20) % 40 == 0:
            ret += program.cycles * program.regs['x']

    if draw:
        grid.draw_frames()

    if mode == 2:
        log("The grid looks like:")
        grid.show_grid(log)
        if decode:
            return grid.decode_grid(log)

    return ret

def other_encode(describe, values):
    if describe:
        return "Encode a value into a program"

    valid = "ABCEFGHJKLOPRSUYZ "
    first = "BEFPR"

    to_encode = input("Enter string to encode: ").upper()

    if len(to_encode) > 8:
        raise Exception("Too long of a string, must be 8 chars or less")
    if len(to_encode) < 8:
        to_encode = to_encode + " " * (8 - len(to_encode))
    if to_encode[0] not in first:
        raise Exception(f"First character must be one of {first}")
    for x in to_encode:
        if x not in valid:
            raise Exception(f"Character {x} not valid, must be one of {valid}")

    save_instructions = input("Save instructions to: ")

    from grid import encode_grid, Grid
    from dummylog import DummyLog
    grid = encode_grid(to_encode, log=None)
    grid = Grid.from_text(grid)
    grid.show_grid(DummyLog())

    raster = ""
    for y in range(6):
        for x in range(40):
            if grid[(x, y)] == "#":
                raster += "#"
            else:
                raster += " "

    raster = raster[3:]
    values = ["noop"]

    val_x = 1
    target = val_x
    while len(raster):
        if raster[:3] == "###":
            target += 3
            if target > 40:
                target -= 40
            values.append(f"addx {target - val_x}")
            val_x = target
            values.append("noop")
            raster = raster[3:]
        elif raster[:2] == "##":
            target += 2
            if target > 39:
                target -= 40
            values.append(f"addx {target - val_x}")
            val_x = target
            raster = raster[2:]
        elif raster[:1] == "#":
            target += 1
            if target > 38:
                target -= 40
            values.append(f"addx {target - val_x}")
            val_x = target
            target += 1
            raster = raster[2:]
        else:
            raster = raster[1:]
            values.append("noop")
            target += 1

    with open(save_instructions, "wt") as f:
        for row in values:
            f.write(row + "\n")

    calc(DummyLog(), values, 2, decode=True)

def test(log):
    values = log.decode_values("""
        addx 15
        addx -11
        addx 6
        addx -3
        addx 5
        addx -1
        addx -8
        addx 13
        addx 4
        noop
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx -35
        addx 1
        addx 24
        addx -19
        addx 1
        addx 16
        addx -11
        noop
        noop
        addx 21
        addx -15
        noop
        noop
        addx -3
        addx 9
        addx 1
        addx -3
        addx 8
        addx 1
        addx 5
        noop
        noop
        noop
        noop
        noop
        addx -36
        noop
        addx 1
        addx 7
        noop
        noop
        noop
        addx 2
        addx 6
        noop
        noop
        noop
        noop
        noop
        addx 1
        noop
        noop
        addx 7
        addx 1
        noop
        addx -13
        addx 13
        addx 7
        noop
        addx 1
        addx -33
        noop
        noop
        noop
        addx 2
        noop
        noop
        noop
        addx 8
        noop
        addx -1
        addx 2
        addx 1
        noop
        addx 17
        addx -9
        addx 1
        addx 1
        addx -3
        addx 11
        noop
        noop
        addx 1
        noop
        addx 1
        noop
        noop
        addx -13
        addx -19
        addx 1
        addx 3
        addx 26
        addx -30
        addx 12
        addx -1
        addx 3
        addx 1
        noop
        noop
        noop
        addx -9
        addx 18
        addx 1
        addx 2
        noop
        noop
        addx 9
        noop
        noop
        noop
        addx -1
        addx 2
        addx -37
        addx 1
        addx 3
        noop
        addx 15
        addx -21
        addx 22
        addx -6
        addx 1
        noop
        addx 2
        addx 1
        noop
        addx -10
        noop
        noop
        addx 20
        addx 1
        addx 2
        addx 2
        addx -6
        addx -11
        noop
        noop
        noop
    """)

    log.test(calc(log, values, 1), 13140)
    calc(log, values, 2)

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=10, final_secs=5)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2, decode=True))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

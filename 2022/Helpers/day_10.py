#!/usr/bin/env python3

DAY_NUM = 10
DAY_DESC = 'Day 10: Cathode-Ray Tube'

def calc(log, values, mode):
    # TODO: Delete or use these
    from grid import Grid, Point
    grid = Grid()
    # grid = Grid.from_text(values)
    # from program import Program
    # program = Program(values)

    
    # TODO

    cycles = 0
    val = 1

    grab = 20
    ret = 0

    for row in values:
        inc = []
        if row.startswith("addx"):
            inc = [1, 1]
        if row.startswith("noop"):
            inc = [1]

        for _ in inc:
            if abs((cycles % 40) - val) <= 1:
                grid[(cycles % 40, cycles // 40)] = "#"
            else:
                grid[(cycles % 40, cycles // 40)] = "."
            cycles += 1
            if (cycles + 20) % 40 == 0:
                ret += cycles * val

        if row.startswith("addx"):
            val += int(row.split(" ")[1])

    if mode == 2:
        log("The grid looks like:")
        grid.show_grid(log)
        return grid.decode_grid(log)

    return ret

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

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip() for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

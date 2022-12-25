#!/usr/bin/env python3

DAY_NUM = 19
DAY_DESC = 'Day 19: Tractor Beam'


def calc(log, values):
    from program import Program
    ticker = Program.make_ticker(values)

    def getxy(x, y):
        prog = Program(ticker, log)
        prog.add_to_input(x)
        prog.add_to_input(y)
        prog.tick_till_end()
        return prog.get_output()

    try_y = 101
    x = 0
    skip_y = 256
    x_stack = []
    while True:
        x = max(x - 1, 0)
        while True:
            if getxy(x, try_y) == 1:
                break
            x += 1
        x_stack.append(x)
        if getxy(x + 99, try_y - 99) == 1:
            if skip_y == 1:
                log("The best 100x100 is: " + str(x * 10000 + (try_y - 99)))
                break
            else:
                try_y -= skip_y
                skip_y //= 2
                x_stack.pop()
                x = x_stack.pop()
        try_y += skip_y

    count = 0
    start_x = 0
    for y in range(50):
        bail = 5 # Because there are gaps at the start
        update_start = True
        for x in range(max(start_x - 1, 0), 50):
            if getxy(x, y) == 1:
                if update_start:
                    update_start = False
                    start_x = x
                count += 1
            else:
                bail -= 1
                if not update_start or bail == 0:
                    break

    log("The number in the 50x50 grid is: " + str(count))

    return count


def test(log):
    return True


def run(log, values):
    calc(log, values)

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

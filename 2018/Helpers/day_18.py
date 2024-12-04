#!/usr/bin/env python3

DAY_NUM = 18
DAY_DESC = 'Day 18: Settlers of The North Pole'


def calc(values, steps):
    # Helper reads the input file and stores it in values, steps is hard coded based on puzzle

    # Turn the list of strings into a list of chars, with padding on the edge
    values = [" " * len(values[0])] + values + [" " * len(values[0])]
    values = [list(" " + x + " ") for x in values]

    # Make a copy
    temp = [[x for x in y] for y in values]

    # Make a simple list of offsets around a point to make for/each eacher
    wrap = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                wrap.append((x, y))

    # Turn the string into ints, makes my head hurt slightly less
    conv = {".": 0, "|": 1, "#": 2, ' ': 0}

    for line in values:
        for i in range(len(line)):
            line[i] = conv[line[i]]

    # Look for loops, each time we don't find one, try a loop one iteration bigger
    loop_size = 1
    loop_left = loop_size
    loop_val = ""

    cur_step = 0

    while cur_step < steps:
        cur_step += 1

        # Calculate the next step, taking care to update each point, even if it doesn't change
        for y in range(1, len(values)-1):
            for x in range(1, len(values[0])-1):
                trees = 0
                lumber = 0
                for off in wrap:
                    temp_val = values[y+off[1]][x+off[0]]
                    if temp_val == 1:
                        trees += 1
                    elif temp_val == 2:
                        lumber += 1

                if values[y][x] == 0:
                    if trees >= 3:
                        temp[y][x] = 1
                    else:
                        temp[y][x] = 0
                elif values[y][x] == 1:
                    if lumber >= 3:
                        temp[y][x] = 2
                    else:
                        temp[y][x] = 1
                elif values[y][x] == 2:
                    if lumber == 0 or trees == 0:
                        temp[y][x] = 0
                    else:
                        temp[y][x] = 2

        # Check to see if we're looping
        loop_left -= 1
        if loop_left == 0:
            test = "\n".join(["".join(str(x)) for x in values])
            if test == loop_val:
                # We found a loop! We can skip ahead to the end based off our loop size
                cur_step += ((steps - cur_step) // loop_size) * loop_size
            else:
                # No loop, try again with one slightly larger cycle
                loop_size += 1
                loop_val = test
                loop_left = loop_size

        # Swap out the temp array and the live array
        temp, values = values, temp

    # Stupid simple way to count the number of lumber and trees
    lumber = sum(sum((1 if y == 2 else 0) for y in x) for x in values)
    trees = sum(sum((1 if y == 1 else 0) for y in x) for x in values)

    # All done, return the result!
    return lumber * trees


def test(log):
    values = [
        ".#.#...|#.",
        ".....#|##|",
        ".|..|...#.",
        "..|#.....#",
        "#.#|||#|#|",
        "...#.||...",
        ".|....|...",
        "||...#|.#|",
        "|.||||..|.",
        "...#.|..|.",
    ]

    if calc(values, 10) == 1147:
        return True
    else:
        return False


def run(log, values):
    log(calc(values, 10))
    log(calc(values, 1000000000))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2018/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

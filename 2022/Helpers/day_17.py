#!/usr/bin/env python3

DAY_NUM = 17
DAY_DESC = 'Day 17: Pyroclastic Flow'

from collections import deque

def calc(log, values, mode):
    from grid import Grid, Point

    grid = Grid()

    steps = deque()
    for row in values:
        for x in row.strip():
            steps.append(x)

    step = 0
    rotates = 0
    seen = {}

    bail = -1
    max_steps = 2022 if mode == 1 else 1000000000000
    add = 0
    offset = 0

    for step in range(max_steps): # (2022):
        if bail > 0:
            bail -= 1
            if bail == 0:
                break

        if len(grid.grid) == 0:
            y = -3
        else:
            y = min(grid.y_range()) - 4

        step += offset
        if (step % 5) == 0:
            shape = [(2, 0), (3, 0), (4, 0), (5, 0)]
        elif (step % 5) == 1:
            shape = [(3, 0), (2, -1), (3, -1), (4, -1), (3, -2)]
        elif (step % 5) == 2:
            shape = [(2, 0), (3, 0), (4, 0), (4, -1), (4, -2)]
        elif (step % 5) == 3:
            shape = [(2, 0), (2, -1), (2, -2), (2, -3)]
        elif (step % 5) == 4:
            shape = [(2, 0), (3, 0), (2, -1), (3, -1)]
        
        shape = [Point(*pt) for pt in shape]
        shape = [pt + (0, y) for pt in shape]

        key = (step % 5, rotates % len(steps))

        if key not in seen:
            seen[key] = []
        
        if len(grid.grid) > 0 and bail < 0:
            if len(seen[key]) == 6:
                steps_taken = seen[key][2+2] - seen[key][0+2]
                lines_added = seen[key][3+2] - seen[key][1+2]

                remaining_cycles = (max_steps - step) // steps_taken
                bail = (max_steps - step) % steps_taken + 1
                add += lines_added * int(remaining_cycles)
                offset = -1
                seen = {}
                continue
            else:
                seen[key].append(step)
                seen[key].append(max(grid.y_range()) - min(grid.y_range()))

        while True:
            rotates += 1
            temp = steps.popleft()
            steps.append(temp)

            if temp == ">":
                dir = (1, 0)
            else:
                dir = (-1, 0)
            
            hit = False
            for pt in shape:
                if not(0 <= (pt + dir).x <= 6) or grid[pt + dir] == "#":
                    hit = True
                    break
            if not hit:
                shape = [pt + dir for pt in shape]
                
            hit = False
            for pt in shape:
                pt += (0, 1)
                if grid[pt] == "#" or pt.y > 0:
                    hit = True
                    break

            if hit:# or step == 3:
                for pt in shape:
                    grid[pt] = "#"
                break
            else:
                shape = [pt + (0, 1) for pt in shape]

    return max(grid.y_range()) - min(grid.y_range()) + add + 1

def test(log):
    values = log.decode_values("""
        >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    """)

    log.test(calc(log, values, 1), 3068)
    log.test(calc(log, values, 2), 1514285714288)

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
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

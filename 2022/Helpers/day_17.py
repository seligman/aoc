#!/usr/bin/env python3

# Animation: https://youtu.be/dMAxp1nmmiI

DAY_NUM = 17
DAY_DESC = 'Day 17: Pyroclastic Flow'

from collections import deque

_frame = 0
_target_off = 1
_off = 1
_source_code = None
def save_frame(grid, shape, blocks):
    from grid import Grid
    from PIL import Image, ImageDraw

    global _frame, _target_off, _off, _source_code
    if _target_off < _off:
        _off -= 0.25

    temp = Grid()
    if _source_code is None:
        _source_code = temp.get_font(10)
    if _off == 1:
        for x in range(-1, 8):
            temp[(x, 1)] = "#"

    if len(grid.grid) == 0:
        max_height = 0
    else:
        max_height = (-min(grid.y_range())) + 1
    for y in range(int(_off), int(_off)-40, -1):
        temp[(-1, y)] = "#"
        temp[(7, y)] = "#"

        for x in range(7):
            if grid[(x, y)] == "#":
                _target_off = min(_target_off, y + 25)
                temp[(x, y)] = "#"

    if shape is not None:
        for pt in shape:
            if pt.y > int(_off) - 40 and pt.y <= int(_off):
                temp[pt] = "Star"

    temp[(20, int(_off))] = 0

    im = temp.draw_grid(return_image=True)
    im2 = Image.new('RGB', (im.width, im.height - 40))
    im2.paste(im, (0, -20-10-int((_off - int(_off)) * 10)))
    dr = ImageDraw.Draw(im2)
    dr.text((125, 10), f"Blocks: {blocks:2,}\nHeight: {max_height:2,}", (255, 255, 255), _source_code)
    del dr

    im2.save(f"frame_{_frame:05d}.png")
    if _frame % 250 == 0:
        print(f"Saved frame {_frame}, with {blocks} blocks")
    _frame += 1

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def calc(log, values, mode, draw=False):
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
    blocks = 0

    for step in range(max_steps):
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

            if draw:
                save_frame(grid, shape, blocks)
                
            hit = False
            for pt in shape:
                pt += (0, 1)
                if grid[pt] == "#" or pt.y > 0:
                    hit = True
                    break

            if hit:
                for pt in shape:
                    grid[pt] = "#"
                blocks += 1
                if draw:
                    save_frame(grid, None, blocks)
                break
            else:
                if draw:
                    save_frame(grid, shape, blocks)
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

#!/usr/bin/env python3

# Animation: https://youtu.be/dMAxp1nmmiI
# Speed Up: https://youtu.be/Hrsan4LFvDo

DAY_NUM = 17
DAY_DESC = 'Day 17: Pyroclastic Flow'

from collections import deque, namedtuple

class DrawHelper:
    def __init__(self, grid, fast):
        self.frame = 0
        self.target_off = 1
        self.off = 1
        self.source_code = grid.get_font(10)
        self.skip = 0
        self.fast = fast
        self.speed = 0.25

    def save_frame(self, grid, shape, blocks, final_frame=False):
        if not final_frame:
            if self.skip > 0:
                self.skip -= 1
                return
        from grid import Grid
        from PIL import Image, ImageDraw

        if self.target_off < self.off:
            self.off -= self.speed

        temp = Grid()
        if self.off == 1:
            for x in range(-1, 8):
                temp[(x, 1)] = "#"

        if len(grid.grid) == 0:
            max_height = 0
        else:
            max_height = -grid.axis_min(1) + 1
        for y in range(int(self.off), int(self.off)-40, -1):
            temp[(-1, y)] = "#"
            temp[(7, y)] = "#"

            for x in range(7):
                if grid[(x, y)] == "#":
                    self.target_off = min(self.target_off, y + 25)
                    temp[(x, y)] = "#"

        if shape is not None:
            for pt in shape:
                if pt.y > int(self.off) - 40 and pt.y <= int(self.off):
                    temp[pt] = "Star"

        temp[(20, int(self.off))] = 0

        im = temp.draw_grid(return_image=True)
        im2 = Image.new('RGB', (im.width, im.height - 40))
        im2.paste(im, (0, -20-10-int((self.off - int(self.off)) * 10)))
        dr = ImageDraw.Draw(im2)
        dr.text((125, 10), f"Blocks: {blocks:2,}\nHeight: {max_height:2,}", (255, 255, 255), self.source_code)
        del dr

        im2.save(f"frame_{self.frame:05d}.png")
        if self.frame % 250 == 0:
            print(f"Saved frame {self.frame}, with {blocks} blocks")
        if self.fast:
            if blocks >= (2): self.skip, self.speed = 1, 0.5
            if blocks >= (2 + 4): self.skip, self.speed = 2, 1
            if blocks >= (2 + 4 + 8): self.skip, self.speed = 4, 2
            if blocks >= (2 + 4 + 8 + 16): self.skip, self.speed = 8, 4
            if blocks >= (2 + 4 + 8 + 16 + 32): self.skip, self.speed = 16, 8
            if blocks >= (2022 - (2 + 4 + 8 + 16 + 32)): self.skip, self.speed = 8, 4
            if blocks >= (2022 - (2 + 4 + 8 + 16)): self.skip, self.speed = 4, 2
            if blocks >= (2022 - (2 + 4 + 8)): self.skip, self.speed = 2, 1
            if blocks >= (2022 - (2 + 4)): self.skip, self.speed = 1, 0.5
            if blocks >= (2022 - (2)): self.skip, self.speed = 0, 0.25
        self.frame += 1

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True, fast_mode=False)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=5)

def other_draw_fast(describe, values):
    if describe:
        return "Draw this, speeding up"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 1, draw=True, fast_mode=True)
    animate.create_mp4(DAY_NUM, rate=30, final_secs=15)

def calc(log, values, mode, draw=False, fast_mode=False):
    from grid import Grid, Point

    grid = Grid()
    steps = deque()

    for row in values:
        for x in row.strip():
            steps.append(x)

    step = 0
    rotates = 0
    seen = {}
    cycles = {}
    SeenItem = namedtuple('SeenItem', ['height', 'step'])

    bail = -1
    max_steps = 2022 if mode == 1 else 1000000000000
    add = 0
    offset = 0
    blocks = 0
    cur_height = 0
    if draw:
        helper = DrawHelper(grid, fast_mode)

    for step in range(max_steps):
        if bail > 0:
            bail -= 1
            if bail == 0:
                break

        if len(grid.grid) == 0:
            y = -3
        else:
            y = grid.axis_min(1) - 4

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
        
        shape = [Point(px, py + y) for px, py in shape]

        if bail < 0 and len(grid.grid) > 0:
            key = (step % 5, rotates % len(steps))
            temp = seen.get(key, None)
            if temp is None:
                seen[key] = SeenItem(cur_height, step)
            else:
                cycle = (step - temp.step, cur_height - temp.height)
                cycles[cycle] = cycles.get(cycle, 0) + 1
                if cycles[cycle] < 50:
                    temp = None
                    seen[key] = SeenItem(cur_height, step)

            if temp is not None:
                lines_added = cur_height - temp.height
                steps_taken = step - temp.step
                remaining_cycles = (max_steps - step) // steps_taken
                bail = (max_steps - step) % steps_taken + 1
                add += lines_added * int(remaining_cycles)
                offset = -1
                seen = {}
                continue

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
                helper.save_frame(grid, shape, blocks)
                
            hit = False
            for pt in shape:
                pt += (0, 1)
                if grid[pt] == "#" or pt.y > 0:
                    hit = True
                    break

            if hit:
                for pt in shape:
                    grid[pt] = "#"
                    cur_height = max(-pt.y, cur_height)
                blocks += 1
                if draw:
                    helper.save_frame(grid, None, blocks)
                break
            else:
                if draw:
                    helper.save_frame(grid, shape, blocks)
                shape = [pt + (0, 1) for pt in shape]

    if draw:
        helper.save_frame(grid, None, blocks, True)
    return -grid.axis_min(1) + add + 1

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

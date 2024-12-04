#!/usr/bin/env python3

DAY_NUM = 2
DAY_DESC = 'Day 2: Dive!'

def calc(log, values, mode, draw=False):
    if draw:
        from PIL import Image, ImageDraw

    pos = 0
    depth = 0
    aim = 0

    if draw:
        im = Image.new('RGB', (10 + 2000 // 20, 10 + 800000 // 1000), color=(0,0,0))
        d = ImageDraw.Draw(im, 'RGBA')
        frame = 0
        old_x, old_y = None, None
        skip = 0

    for cur in values:
        dir, amt = cur.split()
        amt = int(amt)
        if mode == 1:
            if dir == "forward":
                pos += amt
            elif dir == "down":
                depth += amt
            elif dir == "up":
                depth -= amt
            else:
                raise Exception()
        else:
            if dir == "forward":
                pos += amt
                depth += aim * amt
                if draw:
                    new_x, new_y = ((pos // 20) + 5), ((depth // 1000) + 5)
                    if old_x is not None:
                        d.line((old_x, old_y, new_x, new_y), fill=(255, 255, 255))
                    old_x, old_y = new_x, new_y
                    if skip == 0:
                        frame += 1
                        im.save(f"frame_{frame:05d}.png")
                        skip = 3
                    else:
                        skip -= 1
            elif dir == "down":
                aim += amt
            elif dir == "up":
                aim -= amt
            else:
                raise Exception()

    if draw:
        frame += 1
        im.save(f"frame_{frame:05d}.png")

    return depth * pos

def other_draw(describe, values):
    if describe:
        return "Animate this"
    draw_internal(values)

def draw_internal(values):
    import animate
    from dummylog import DummyLog

    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM)
    
def test(log):
    values = log.decode_values("""
        forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2
    """)

    log.test(calc(log, values, 1), 150)
    log.test(calc(log, values, 2), 900)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2021/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

#!/usr/bin/env python3

def get_desc():
    return 2, 'Day 2: Dive!'

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
    import os
    from dummylog import DummyLog

    for cur in os.listdir('.'):
        if cur.startswith("frame_") and cur.endswith(".png"):
            os.unlink(cur)

    calc(DummyLog(), values, 2, draw=True)

    import subprocess
    import os
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", "10", 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", f"animation_{get_desc()[0]:02d}.mp4"),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)
    
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
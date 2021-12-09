#!/usr/bin/env python3

import os
import subprocess
import math

def show_colors(count):
    count = int(count)
    import matplotlib.pyplot as plt
    x = plt.get_cmap("plasma").colors
    print("colors = {")
    for i in range(count):
        cur = x[int(i / (count - 1) * (len(x) - 1))]
        print(f"    '{i}': ({int(cur[0] * 255)}, {int(cur[1] * 255)}, {int(cur[2] * 255)}),")
    print("}")

def prep():
    for cur in os.listdir('.'):
        if cur.startswith("frame_") and cur.endswith(".png"):
            os.unlink(cur)

def ease(value):
    value = max(0, min(1, value))
    if value < 0.5:
        return 4 * (value ** 3)
    else:
        return 1 - math.pow(-2 * value + 2, 3) / 2

def rotate(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def create_mp4(desc, extra="", keep_files=False, rate=10):
    cmd = [
        "ffmpeg", "-y",
        "-hide_banner",
        "-f", "image2",
        "-framerate", str(rate), 
        "-i", "frame_%05d.png", 
        "-c:v", "libx264", 
        "-profile:v", "main", 
        "-pix_fmt", "yuv420p", 
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-an", 
        "-movflags", "+faststart",
        os.path.join("animations", f"animation_{desc[0]:02d}{extra}.mp4"),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)

    if not keep_files:
        prep()

def main():
    import sys
    cmds = [
        ("colors", " <num>", "Dump out colors from heat map", 1, show_colors),
    ]
    show_help = True
    for cmd, _args_desc, _desc, args, func in cmds:
        if len(sys.argv) == 2 + args and sys.argv[1].lower().replace("-", "_") == cmd:
            show_help = False
            func(*sys.argv[2:2+args])

    if show_help:
        print("Usage:")
        max_len = max(len(x[0] + x[1]) for x in cmds)
        for cmd, args_desc, desc, _args, _func in cmds:
            print(f"  {cmd}{args_desc}{' '*(max_len - len(cmd + args_desc))} - {desc}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import subprocess
import math

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

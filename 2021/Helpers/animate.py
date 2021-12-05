#!/usr/bin/env python3

import os
import subprocess

def prep():
    for cur in os.listdir('.'):
        if cur.startswith("frame_") and cur.endswith(".png"):
            os.unlink(cur)

def create_mp4(desc, extra="", keep_files=False):
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
        os.path.join("animations", f"animation_{desc[0]:02d}{extra}.mp4"),
    ]
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)

    if not keep_files:
        prep()

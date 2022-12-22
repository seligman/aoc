#!/usr/bin/env python3

import code
import undetected_chromedriver as uc
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
from datetime import datetime, timedelta
import subprocess
from PIL import Image, ImageDraw
import time

def save_screenshot(msg, driver, path, to_grab, files):
    original_size = driver.get_window_size()
    required_width = max(driver.execute_script('return document.body.parentNode.scrollWidth'), 900)
    required_height = max(driver.execute_script('return document.body.parentNode.scrollHeight'), 900)
    driver.set_window_size(required_width, required_height)
    body = driver.find_element(By.TAG_NAME, "body")
    next = None
    start = datetime.utcnow()
    for i in range(to_grab):
        if next is not None:
            now = datetime.utcnow()
            if now < next:
                time.sleep((next - now).total_seconds())
        files.append(os.path.join(path, f"temp_{i:04d}.png"))
        now = datetime.utcnow()
        print(f"{(now - start).total_seconds():8.4f}: {msg}: Saving {files[-1]}...")
        if next is None:
            next = start + timedelta(seconds=0.1)
        else:
            next += timedelta(seconds=0.1)
        body.screenshot(files[-1])
    driver.set_window_size(original_size['width'], original_size['height'])


def main():
    files = [
        "favicon.png",
        "highcontrast.css",
        "html5.js",
        "SourceCodePro.css",
        "SourceCodePro.ttf",
        "style.css",
    ]
    for cur in files:
        if not os.path.isfile(os.path.join("aoc", cur)):
            with open(os.path.join("..", "Puzzles", cur), "rb") as f_src:
                with open(os.path.join("aoc", cur), "wb") as f_dest:
                    f_dest.write(f_src.read())

    print("Loading main page...")
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.set_window_size(1000, 1000)
    now = datetime.utcnow()

    todo = []
    for cur in sorted(os.listdir("aoc")):
        if cur.startswith("index_") and cur.endswith(".html"):
            todo.append({"fn": cur, "first": False, "last": False})

    todo[0]['first'] = True
    todo[-1]['last'] = True

    if not os.path.isdir("screenshots"):
        os.mkdir("screenshots")
    for cur in list(os.listdir("screenshots")):
        os.unlink(os.path.join("screenshots", cur))

    frame_number = 0
    for cur in todo:
        print(f"Working on {cur['fn']}")
        
        if cur['first']:
            steps = [
                {"dupes": 10, "frames": 1, "extra": "00:00:05", "hide_stars": None},
                {"dupes": 10, "frames": 1, "extra": "00:00:04", "hide_stars": None},
                {"dupes": 10, "frames": 1, "extra": "00:00:03", "hide_stars": None},
                {"dupes": 10, "frames": 1, "extra": "00:00:02", "hide_stars": None},
                {"dupes": 10, "frames": 1, "extra": "00:00:01", "hide_stars": None},
            ]
        elif cur['last']:
            steps = [
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": (1, 2)},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": (2, )},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": None},
                {"dupes": 1, "frames": 100, "extra": "", "hide_stars": None},
            ]
        else:
            steps = [
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": (1, 2)},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": (2, )},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": None},
            ]

        for step in steps:
            files = []
            driver.get("about:blank")
            with open(os.path.join(os.path.split(__file__)[0], "aoc", cur['fn']), "rt") as f:
                html = f.read()
            if step['hide_stars'] is not None:
                if 1 in step['hide_stars']:
                    html = html.replace('<span class="calendar-mark-complete">*</span>', '', 1)
                if 2 in step['hide_stars']:
                    html = html.replace('<span class="calendar-mark-verycomplete">*</span>', '', 1)
            with open(os.path.join(os.path.split(__file__)[0], "aoc", "_temp_.html"), "wt") as f:
                f.write(html)

            driver.get(os.path.join(os.path.split(__file__)[0], "aoc", "_temp_.html#" + step['extra']))

            save_screenshot(f"{cur['fn']} {step['extra']} {step['hide_stars']}", driver, "screenshots", step['frames'], files)
            
            os.unlink(os.path.join(os.path.split(__file__)[0], "aoc", "_temp_.html"))

            crop_x = 700
            crop_y = 23 * 27
            for fn in files:
                im = Image.open(fn)
                im_crop = Image.new("RGB", (crop_x, crop_y), (15, 15, 35))
                im_crop.paste(im)
                for _ in range(step['dupes']):
                    im_crop.save(os.path.join("screenshots", f"frame_{frame_number:05d}.png"))
                    frame_number += 1
                im.close()

            for fn in files:
                os.unlink(fn)
        
    print("Close the driver")
    driver.close()

    if os.path.isfile(os.path.join("animated.mp4")):
        os.unlink(os.path.join("animated.mp4"))
    
    subprocess.check_call([
        "ffmpeg", 
        "-framerate", "10",
        "-i", os.path.join("screenshots", "frame_%05d.png"), 
        os.path.join("animated.mp4"),
    ])


if __name__ == "__main__":
    main()

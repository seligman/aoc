#!/usr/bin/env python3

import code
import undetected_chromedriver as uc
uc.install()
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
from slack import WebClient
from PIL import Image, ImageDraw
import time

def save_screenshot(driver, path, images, files):
    original_size = driver.get_window_size()
    required_width = max(driver.execute_script('return document.body.parentNode.scrollWidth'), 900)
    required_height = max(driver.execute_script('return document.body.parentNode.scrollHeight'), 900)
    driver.set_window_size(required_width, required_height)
    body = driver.find_element(By.TAG_NAME, "body")
    next = None
    start = datetime.utcnow()
    for i in range(images):
        if next is not None:
            now = datetime.utcnow()
            if now < next:
                time.sleep((next - now).total_seconds())
        files.append(path % (i,))
        now = datetime.utcnow()
        print(f"{(now - start).total_seconds():8.4f}: Saving {files[-1]}...")
        if next is None:
            next = start + timedelta(seconds=0.1)
        else:
            next += timedelta(seconds=0.1)
        body.screenshot(path % (i,))
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
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1000, 1000)
    now = datetime.utcnow()

    frame = 0
    todo = []
    for cur in sorted(os.listdir("aoc")):
        if cur.startswith("index_") and cur.endswith(".html"):
            todo.append(cur)

    if not os.path.isdir("screenshots"):
        os.mkdir("screenshots")
    for cur in list(os.listdir("screenshots")):
        os.unlink(os.path.join("screenshots", cur))

    for curi, cur in enumerate(todo):
        print(f"Working on {cur}")
        
        frames = 1
        dupes = 10
        extras = [""]
        if curi == 0:
            dupes = 10
            extras = ["00:00:05", "00:00:04", "00:00:03", "00:00:02", "00:00:01"]
        if curi == len(todo) - 1:
            frames = 100
            dupes = 1
        
        for extra in extras:
            files = []
            driver.get("about:blank")
            driver.get(os.path.join(os.path.split(__file__)[0], "aoc", cur + "#" + extra))
            save_screenshot(driver, os.path.join("screenshots", f"temp_{curi:03d}_%03d.png"), frames, files)
            
            crop_x = 700
            crop_y = 580
            for fn in files:
                im = Image.open(fn)
                im_crop = Image.new("RGB", (crop_x, crop_y), (15, 15, 35))
                im_crop.paste(im)
                for _ in range(dupes):
                    im_crop.save(os.path.join("screenshots", f"frame_{frame:05d}.png"))
                    frame += 1
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

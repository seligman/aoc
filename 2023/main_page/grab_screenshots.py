#!/usr/bin/env python3

from datetime import datetime, timedelta
from urllib.parse import urljoin
from urllib.request import urlopen, urlretrieve
import code
import json
import os
import re
import subprocess
import sys
import time
import shutil
if sys.version_info >= (3, 11): from datetime import UTC
else: import datetime as datetime_fix; UTC=datetime_fix.timezone.utc

def save_screenshot(msg, driver, path, to_grab, files):
    from selenium.webdriver.common.by import By # type: ignore
    from selenium.webdriver.common.keys import Keys # type: ignore

    original_size = driver.get_window_size()
    required_width = max(driver.execute_script('return document.body.parentNode.scrollWidth'), 900)
    required_height = max(driver.execute_script('return document.body.parentNode.scrollHeight'), 900)
    driver.set_window_size(required_width, required_height)
    body = driver.find_element(By.TAG_NAME, "body")
    next = None
    start = datetime.now(UTC).replace(tzinfo=None)
    for i in range(to_grab):
        if next is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            if now < next:
                time.sleep((next - now).total_seconds())
        files.append(os.path.join(path, f"temp_{i:04d}.png"))
        now = datetime.now(UTC).replace(tzinfo=None)
        print(f"{(now - start).total_seconds():8.4f}: {msg}: Saving {files[-1]}...")
        if next is None:
            next = start + timedelta(seconds=0.1)
        else:
            next += timedelta(seconds=0.1)
        body.screenshot(files[-1])
    driver.set_window_size(original_size['width'], original_size['height'])

def make_animation():
    if 'VIRTUAL_ENV' not in os.environ:
        if not os.path.isdir(".venv"):
            subprocess.check_call(["python3", "-m", "venv", ".venv"])
        os.environ['VIRTUAL_ENV_PROMPT'] = '(.venv) '
        os.environ['VIRTUAL_ENV'] = os.path.join(os.getcwd(), ".venv")
        for cur in ["Scripts", "bin"]:
            if os.path.isdir(os.path.join(os.getcwd(), ".venv", cur)):
                venv_path = os.path.join(os.getcwd(), ".venv", cur)
                break
        for cur in ["python", "python.exe"]:
            if os.path.isfile(os.path.join(venv_path, cur)):
                venv_file = os.path.join(venv_path, cur)
                break
        os.environ['PATH'] = venv_path + (";" if ";" in os.environ['PATH'] else ":") + os.environ['PATH']
        exit(subprocess.call([venv_file, __file__] + sys.argv[1:]))

    try:
        from selenium import webdriver # type: ignore
    except:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

    make_animation_worker()

def clean_up():
    for dn in ["screenshots", ".venv"]:
        if os.path.isdir(dn):
            print("$ rm -rf " + dn)
            shutil.rmtree(dn)
    for fn in ["animated.mp4"]:
        if os.path.isfile(fn):
            print("$ rm " + fn)
            os.unlink(fn)

def make_animation_worker():
    from selenium import webdriver # type: ignore
    import chromedriver_binary # type: ignore
    import undetected_chromedriver as uc # type: ignore
    from PIL import Image, ImageDraw # type: ignore

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
    now = datetime.now(UTC).replace(tzinfo=None)

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
                {"dupes": 1, "frames": 600, "extra": "", "hide_stars": None},
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
            html = re.sub('<p>.*?AI.*?</p>', '', html)
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

def main():
    cmds = {
        "animate": ("Create animation", make_animation),
        "cleanup": ("Clean up temp files", clean_up),
    }
    for cur in sys.argv[1:]:
        if cur in cmds:
            cmds[cur][1]()
            exit(0)
    
    print("Usage:")
    for cmd, (desc, func) in cmds.items():
        print(f"  {cmd} = {desc}")

if __name__ == "__main__":
    main()

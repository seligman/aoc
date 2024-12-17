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
    make_animation_runner(False)

def make_animation_runner(single_frame):
    if 'VIRTUAL_ENV' not in os.environ:
        need_install = False
        if not os.path.isdir(".venv"):
            subprocess.check_call(["python3", "-m", "venv", ".venv"])
            need_install = True
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
        if need_install:
            subprocess.call(["pip", "install", "-r", "requirements.txt"])
        exit(subprocess.call([venv_file, __file__] + sys.argv[1:]))

    make_animation_worker(single_frame)
    if single_frame:
        dest = os.path.join("..", "Puzzles", "main_page.png")
        dest2 = os.path.join("..", "Puzzles", "main_page_small.png")
        from PIL import Image, ImageDraw # type: ignore
        im = Image.open(os.path.join("screenshots", "frame_00000.png"))
        subprocess.check_call(["p4", "edit", dest])
        subprocess.check_call(["p4", "edit", dest2])
        im.save(dest, "PNG")
        print(f"Wrote {im.width}x{im.height} to {dest}")
        im = im.resize((im.width // 2, im.height // 2), Image.Resampling.BICUBIC)
        im.save(dest2, "PNG")
        print(f"Wrote {im.width}x{im.height} to {dest2}")

        with open(os.path.join("..", "README.md")) as f:
            for row in f:
                m = re.search('width="(?P<width>[0-9]+)" height="(?P<height>[0-9]+)"', row)
                if m is not None:
                    if int(m["width"]) != im.width or int(m["height"]) != im.height:
                        print("Warning: Need to change README.md size!")
                    else:
                        print("README.md has the correct size in it")
                    break

def update_preview():
    make_animation_runner(True)

def clean_up():
    for dn in ["screenshots", ".venv"]:
        if os.path.isdir(dn):
            print("$ rm -rf " + dn)
            shutil.rmtree(dn)
    for fn in ["animated.mp4"]:
        if os.path.isfile(fn):
            print("$ rm " + fn)
            os.unlink(fn)

def make_animation_worker(single_frame):
    from selenium import webdriver # type: ignore
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
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1000, 1000)
    now = datetime.now(UTC).replace(tzinfo=None)

    todo = []
    for cur in sorted(os.listdir("aoc")):
        if cur.startswith("index_") and cur.endswith(".html"):
            todo.append({"fn": cur, "first": False, "last": False, 'single': False})

    todo[0]['first'] = True
    todo[-1]['last'] = True

    if not os.path.isdir("screenshots"):
        os.mkdir("screenshots")
    for cur in list(os.listdir("screenshots")):
        os.unlink(os.path.join("screenshots", cur))

    frame_number = 0

    if single_frame:
        todo = todo[-1:]
        todo[0]['single'] = True

    day = 1
    for cur in todo:
        print(f"Working on {cur['fn']}")

        if cur['single']: 
            steps = [
                {"dupes": 1, "frames": 1, "extra": "", "hide_stars": []},
            ]
        elif cur['first']:
            steps = [
                {"dupes": 10, "frames": 1, "extra": "00:00:05", "hide_stars": []},
                {"dupes": 10, "frames": 1, "extra": "00:00:04", "hide_stars": []},
                {"dupes": 10, "frames": 1, "extra": "00:00:03", "hide_stars": []},
                {"dupes": 10, "frames": 1, "extra": "00:00:02", "hide_stars": []},
                {"dupes": 10, "frames": 1, "extra": "00:00:01", "hide_stars": []},
            ]
        elif cur['last']:
            steps = [
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": [(day, 1), (day, 2)]},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": [(day, 2)]},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": []},
                {"dupes": 1, "frames": 600, "extra": "", "hide_stars": []},
            ]
            day += 1
        else:
            steps = [
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": [(day, 1), (day, 2)]},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": [(day, 2)]},
                {"dupes": 3, "frames": 1, "extra": "", "hide_stars": []},
            ]
            day += 1

        for step in steps:
            files = []
            driver.get("about:blank")
            with open(os.path.join(os.path.split(__file__)[0], "aoc", cur['fn']), "rt") as f:
                html = f.read()
            for hide_day, hide_star in step['hide_stars']:
                html = html.split("\n")
                for i in range(len(html)):
                    if re.search('<span class="calendar-day"> *' + str(hide_day) + ' *</span>', html[i]) is not None:
                        if hide_star == 1:
                            html[i] = html[i].replace('<span class="calendar-mark-complete">*</span>', '', 1)
                        if hide_star == 2:
                            html[i] = html[i].replace('<span class="calendar-mark-complete">*</span>', '', 1)
                html = "\n".join(html)

            html = re.sub('<p>.*?AI.*?</p>', '', html)
            with open(os.path.join(os.path.split(__file__)[0], "aoc", "_temp_.html"), "wt") as f:
                f.write(html)

            driver.get("file://" + os.path.join(os.path.split(__file__)[0], "aoc", "_temp_.html#" + step['extra']))
            # driver.get("https://www.google.com/")

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
    
    if single_frame:
        time.sleep(1)
    else:
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
        "preview": ("Update preview images", update_preview),
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

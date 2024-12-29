#!/usr/bin/env python3

from PIL import Image
import os
import re
from collections import defaultdict

files = []
dn = os.path.join(os.path.split(__file__)[0], "..")
for year in sorted(os.listdir(dn)):
    if re.search("^[0-9]{4}$", year) is not None:
        files.append({
            "fn": f"../{year}/Puzzles/main_page.png",
            "year": year,
        })

histogram = defaultdict(int)
for cur in files:
    print(f"Loading for {cur['year']}")
    im = Image.open(cur['fn'])
    cur["width"] = im.width
    cur["height"] = im.height
    for x in range(im.width):
        for y in range(im.height):
            histogram[im.getpixel((x, y))] += 1
    im.close()
histogram = list((v, k) for k, v in histogram.items())
histogram.sort()

max_width = 800
thumb_width = 185
padding = 10

x, y = padding, 0
for cur in files:
    cur["thumb_width"] = thumb_width
    cur["thumb_height"] = round((thumb_width / cur["width"]) * cur["height"])
    if x + cur["thumb_width"] + padding > max_width:
        x = padding
        y += 1
    cur["x"] = x
    cur["row"] = y
    x += thumb_width + padding

row_number = 0
y = padding
while True:
    row = [x for x in files if x["row"] == row_number]
    if len(row) == 0:
        break
    max_height = max(x["thumb_height"] for x in row)
    for cur in row:
        cur["y"] = y + round((max_height / 2) - (cur["thumb_height"] / 2))
    y += max_height + padding
    row_number += 1

im = Image.new(
    'RGB', 
    (
        max(x['x'] + x['thumb_width'] for x in files) + padding, 
        max(x['y'] + x['thumb_height'] for x in files) + padding,
    ), 
    histogram[-1][1],
)
for cur in files:
    im2 = Image.open(cur['fn'])
    im2 = im2.resize((cur['thumb_width'], cur['thumb_height']), Image.Resampling.LANCZOS)
    im.paste(im2, (cur["x"], cur["y"]))
im.save(os.path.join(dn, "other", "all_images.png"))
print("Created all_images.png")

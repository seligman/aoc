#!/usr/bin/env python3

import os

i = 0
while True:
    fn = os.path.join("aoc", f"index_{i:02d}.html")
    if not os.path.isfile(fn):
        break
    i += 1

print("Using " + fn)

sfn = os.path.join("..", "Puzzles", "index.html")
temp = ""
with open(sfn) as f:
    for row in f:
        skip = False
        if row.startswith('interval = setInterval(update_countdown,1000);'):
            skip = True
        if row.startswith('update_countdown();'):
            skip = True
        if not skip:
            temp += row

with open(fn, "wt") as f:
    f.write(temp)

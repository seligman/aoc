#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Disk Fragmenter'

def calc(log, values, mode, draw=False):
    from grid import Grid, Point
    import random

    disk = []
    is_free = False
    val = 0
    for x in values[0]:
        x = int(x)
        if x > 0:
            if is_free:
                disk.append({"val": -1, "size": x, "skip": False})
            else:
                disk.append({"val": val, "size": x, "skip": False})
                val += 1
        is_free = not is_free

    free_at = 0
    scan_at = len(disk) - 1

    if draw:
        random.seed(42)
        length = sum(x['size'] for x in disk)
        height = int(5 + ((3 * (length ** (1/2))) / 4))
        width = int(height * (16 / 9))
        grid = Grid(default=".")
        frames = []
        colors = []
        for _ in range(32):
            colors.append((random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))

    if mode == 1:
        while True:
            while disk[free_at]["val"] >= 0 or disk[free_at]["size"] == 0:
                free_at += 1
            while disk[scan_at]["val"] < 0 or disk[scan_at]["size"] == 0:
                scan_at -= 1
            if scan_at <= free_at:
                break
            
            if disk[free_at]["size"] == disk[scan_at]["size"]:
                disk[free_at]["val"] = disk[scan_at]["val"]
                disk[scan_at]["size"] = 0
            elif disk[free_at]["size"] < disk[scan_at]["size"]:
                disk[free_at]["val"] = disk[scan_at]["val"]
                disk[scan_at]["size"] -= disk[free_at]["size"]
            else:
                left = disk[free_at]["size"] - disk[scan_at]["size"]
                disk[free_at]["val"] = disk[scan_at]["val"]
                disk[free_at]["size"] = disk[scan_at]["size"]
                disk[scan_at]["size"] = 0
                disk.insert(free_at + 1, {"size": left, "val": -1})
                scan_at += 1
    else:
        free_list = []
        for i, cur in enumerate(disk):
            if cur['val'] == -1:
                free_list.append(i)

        while True:
            while (disk[scan_at]["val"] < 0 or disk[scan_at]["size"] == 0) or disk[scan_at]["skip"]:
                scan_at -= 1
                if scan_at < 0:
                    break
            
            if scan_at < 0:
                break
            free_at = None
            for test in free_list:
                if disk[test]["size"] >= disk[scan_at]["size"]:
                    free_at = test
                    break

            if free_at is not None and free_at < scan_at:
                target = disk[scan_at]["val"]
                if disk[free_at]["size"] == disk[scan_at]["size"]:
                    disk[free_at]["val"] = disk[scan_at]["val"]
                    disk[scan_at]["val"] = -1
                    free_list.remove(free_at)
                else:
                    left = disk[free_at]["size"] - disk[scan_at]["size"]
                    disk[free_at]["val"] = disk[scan_at]["val"]
                    disk[free_at]["size"] = disk[scan_at]["size"]
                    disk[scan_at]["val"] = -1
                    disk.insert(free_at + 1, {"size": left, "val": -1, "skip": False})
                    scan_at += 1
                    free_list = [x+1 if x >= free_at else x for x in free_list]
                
                if draw:
                    frame = []
                    for cur in disk:
                        if cur["size"] > 0:
                            if cur["val"] == -1:
                                frame.append({"free": cur["size"]})
                            else:
                                frame.append({"size": cur["size"], "is_hit": cur["val"] == target, "id": cur["val"]})
                    frames.append(frame)
                    if len(frames) % 500 == 0:
                        log(f"Prep for {len(frames):,} frames")
            else:
                disk[scan_at]["skip"] = True

    if draw:
        grid.ease_frames(rate=15, secs=30, frames=frames)
        for frame in frames:
            pos = 0
            grid.grid.clear()
            grid[width - 1, height - 1] = "."
            for cur in frame:
                if 'free' in cur:
                    for _ in range(cur['free']):
                        grid[pos % width, pos // width] = "."
                        pos += 1
                else:
                    for _ in range(cur['size']):
                        grid[pos % width, pos // width] = "Star" if cur['is_hit'] else ("#", colors[cur['id'] % len(colors)])
                        pos += 1
            grid.save_frame()
            if len(grid.frames) % 25 == 0:
                print(f"Saved frame {len(grid.frames)} of {len(frames)}")

        grid.draw_frames(show_lines=False)

    pos = 0
    ret = 0
    for cur in disk:
        if cur["val"] > 0 and cur["size"] > 0:
            for i in range(cur["size"]):
                ret += (pos + i) * cur["val"]
        pos += cur["size"]

    return ret

def other_draw(describe, values):
    if describe:
        return "Draw this"
    from dummylog import DummyLog
    import animate
    animate.prep()
    calc(DummyLog(), values, 2, draw=True)
    animate.create_mp4(DAY_NUM, rate=15, final_secs=5)

def test(log):
    values = log.decode_values("""
        2333133121414131402
    """)

    log.test(calc(log, values, 1), '1928')
    log.test(calc(log, values, 2), '2858')

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in ["", "Puzzles", "../Puzzles", "../../private/inputs/2024/Puzzles"]:
                cur = os.path.join(*(dn.split("/") + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

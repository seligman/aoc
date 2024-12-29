#!/usr/bin/env python3

DAY_NUM = 9
DAY_DESC = 'Day 9: Disk Fragmenter'

import random, dataclasses

@dataclasses.dataclass(slots=True)
class Entry:
    size: int
    val: int = -1
    skip: bool = False

def calc(log, values, mode, draw=False):
    from grid import Grid
    disk = []
    is_free = False
    val = 0
    for x in values[0]:
        x = int(x)
        if x > 0:
            disk.append(Entry(x, -1 if is_free else val))
            if not is_free:
                val += 1
        is_free = not is_free

    free_at = 0
    scan_at = len(disk) - 1

    if draw:
        random.seed(42)
        length = sum(x.size for x in disk)
        height = int(5 + ((3 * (length ** (1/2))) / 4))
        width = int(height * (16 / 9))
        grid = Grid(default=".")
        frames = []
        colors = []
        for _ in range(32):
            colors.append((random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))

    if mode == 1:
        while True:
            while disk[free_at].val >= 0 or disk[free_at].size == 0:
                free_at += 1
            while disk[scan_at].val < 0 or disk[scan_at].size == 0:
                scan_at -= 1
            if scan_at <= free_at:
                break
            
            # Note: This drops blocks as we work through them, since we don't need them
            if disk[free_at].size == disk[scan_at].size:
                # Free block is exactly the right size, fill it
                disk[free_at].val = disk[scan_at].val
                disk[scan_at].size = 0
            elif disk[free_at].size < disk[scan_at].size:
                # Free block is too small, fill out what we can, shrink the rest
                disk[free_at].val = disk[scan_at].val
                disk[scan_at].size -= disk[free_at].size
            else:
                # Free block is too big, fill it and add a free block after it
                # for the left over space
                left = disk[free_at].size - disk[scan_at].size
                disk[free_at].val = disk[scan_at].val
                disk[free_at].size = disk[scan_at].size
                disk[scan_at].size = 0
                disk.insert(free_at + 1, Entry(left))
                scan_at += 1
    else:
        free_list = []
        # Build a list of all free blocks
        for i, cur in enumerate(disk):
            if cur.val == -1:
                free_list.append(i)

        while True:
            # Find block to move
            while (disk[scan_at].val < 0 or disk[scan_at].size == 0) or disk[scan_at].skip:
                scan_at -= 1
                if scan_at < 0:
                    break
            
            if scan_at < 0:
                # We ran out of work to do
                break

            # Find first free block we can use
            free_at = None
            for test in free_list:
                if disk[test].size >= disk[scan_at].size:
                    free_at = test
                    break

            if free_at is not None and free_at < scan_at:
                target = disk[scan_at].val
                if disk[free_at].size == disk[scan_at].size:
                    # Free block is the exact size, just swap things
                    disk[free_at].val = disk[scan_at].val
                    disk[scan_at].val = -1
                    free_list.remove(free_at)
                else:
                    # Free block is too big, replace it and add
                    # a free block for the extra space
                    left = disk[free_at].size - disk[scan_at].size
                    disk[free_at].val = disk[scan_at].val
                    disk[free_at].size = disk[scan_at].size
                    disk[scan_at].val = -1
                    disk.insert(free_at + 1, Entry(left))
                    scan_at += 1
                    # Move all the free blocks down one in the list from this block on
                    free_list = [x+1 if x >= free_at else x for x in free_list]
                
                if draw:
                    frame = []
                    for cur in disk:
                        if cur.size > 0:
                            frame.append(Entry(cur.size, cur.val))
                            if cur.val == target:
                                frame[-1].skip = True
                    frames.append(frame)
                    if len(frames) % 500 == 0:
                        log(f"Prep for {len(frames):,} frames")
            else:
                # Nowhere to fit block, skip this one
                disk[scan_at].skip = True

    if draw:
        grid.ease_frames(rate=15, secs=30, frames=frames)
        for frame in frames:
            pos = 0
            grid.grid.clear()
            grid[width - 1, height - 1] = "."
            for cur in frame:
                for _ in range(cur.size):
                    xy = pos % width, pos // width
                    if cur.val == -1:
                        grid[xy] = "."
                    elif cur.skip:
                        grid[xy] = "Star"
                    else:
                        grid[xy] = ("#", colors[cur.val % len(colors)])
                    pos += 1
            grid.save_frame()
            if len(grid.frames) % 25 == 0:
                print(f"Saved frame {len(grid.frames)} of {len(frames)}")

        grid.draw_frames(show_lines=False)

    # Calculate the CRC
    pos = 0
    ret = 0
    for cur in disk:
        if cur.val > 0:
            ret += ((pos * cur.size) + int(cur.size * (cur.size - 1) / 2)) * cur.val
        pos += cur.size

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
    log(f"Part 1: {calc(log, values, 1)}")
    log(f"Part 2: {calc(log, values, 2)}")

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

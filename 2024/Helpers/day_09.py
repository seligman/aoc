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
                disk.append({"free": x})
            else:
                disk.append({"id": val, "size": x})
                val += 1
        is_free = not is_free

    if draw:
        length = 0
        for x in disk:
            length += x.get('free', 0) + x.get('size', 0)
        height = int(5 + ((3 * (length ** (1/2))) / 4))
        width = int(height * (16 / 9))
        grid = Grid(default=".")
        frames = []
        random.seed(42)
        colors = []
        for _ in range(32):
            colors.append((random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))

    head = None
    tail = None
    last = None
    for cur in disk:
        if head is None:
            head = cur
        if last is not None:
            last['next'] = cur
        cur['prev'] = last
        cur['next'] = None
        last = cur
        tail = cur

    if mode == 1:
        while True:
            temp = head
            free = None
            while temp is not None:
                if temp.get("free", 0) > 0:
                    free = temp
                    break
                temp = temp['next']
            
            temp = tail
            to_move = None
            while temp is not None:
                if temp.get("size", 0) > 0:
                    to_move = temp
                    break
                temp = temp['prev']
                if temp == free:
                    break
            
            if to_move is None or free is None:
                break

            x = min(to_move['size'], free['free'])
            to_move['size'] -= x
            move_id = to_move['id']
            if 'id' not in free:
                free['id'] = to_move['id']
                free['free'] -= x
                free['size'] = x
            elif free['id'] == to_move['id']:
                free['size'] += x
                free['free'] -= x
            else:
                temp = {
                    "free": free['free'] - x,
                    "id": to_move['id'],
                    "size": x,
                }
                free['free'] = 0
                cur_next = free['next']
                free['next'] = temp
                temp['next'] = cur_next
                cur_next['prev'] = temp
                temp['prev'] = free
    else:
        while True:
            temp = tail
            to_move = None
            while temp is not None:
                temp['not_free'] = True
                if temp.get("size", 0) > 0 and not temp.get('skip', False):
                    to_move = temp
                    to_move['skip'] = True
                    break
                temp = temp['prev']
            while temp is not None:
                temp['not_free'] = False
                temp = temp['prev']

            if to_move is None:
                break

            free = None
            temp = head
            while temp is not None:
                if not temp['not_free'] and temp.get('free', 0) >= to_move['size']:
                    free = temp
                    break
                temp = temp['next']
                if temp == to_move:
                    break

            if free is not None:
                val = to_move['id']
                size = to_move['size']
                to_move['free'] = to_move['size']
                del to_move['size']
                del to_move['id']

                if free['free'] > size:
                    left = free['free'] - size
                    free['id'] = val
                    free['size'] = size
                    free['free'] = 0

                    temp = {"free": left}
                    cur_next = free['next']
                    free['next'] = temp
                    temp['next'] = cur_next
                    cur_next['prev'] = temp
                    temp['prev'] = free

                else:
                    free['id'] = val
                    free['size'] = size
                    free['free'] = 0

                if draw:
                    frame = []
                    temp = head
                    pos = 0
                    while temp is not None:
                        if temp.get('size', 0) > 0:
                            frame.append({"size": temp['size'], "pos": pos, "is_hit": temp['id'] == val, "id": temp['id']})
                            pos += temp['size']
                        if temp.get('free', 0) > 0:
                            frame.append({"free": temp['free'], "pos": pos})
                            pos += temp['free']
                        temp = temp['next']
                    frames.append(frame)
                    if len(frames) % 500 == 0:
                        log(f"Saved {len(frames):,} frames")

        temp = head
        while temp is not None:
            temp = temp['next']

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

    temp = head
    ret = 0
    pos = 0
    while temp != None:
        if 'id' in temp:
            val = temp['id']
            for i in range(temp.get('size', 0)):
                ret += pos * val
                pos += 1
        else:
            pos += temp['free']
        temp = temp['next']

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

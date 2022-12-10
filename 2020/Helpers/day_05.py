#!/usr/bin/env python3

from collections import defaultdict

DAY_NUM = 5
DAY_DESC = 'Day 5: Binary Boarding'

def calc(log, values, mode, draw=False):
    neighbors = defaultdict(int)
    seats = set()

    if draw:
        from grid import Grid
        grid = Grid()
        for x in range(8):
            for y in range(111):
                grid[x, y] = '.'

    for value in values:
        row, row_part = 127, 64
        seat, seat_part = 7, 4
        for cur in value:
            if cur in {"F", "B"}:
                row += row_part * {"F": -1, "B": 1}[cur]
                row_part //= 2
            elif cur in {"L", "R"}:
                seat += seat_part * {"L": -1, "R": 1}[cur]
                seat_part //= 2

        if draw:
            grid[seat // 2, row // 2] = "#"
            grid.save_frame()

        seat_id = (row // 2) * 8 + (seat // 2)

        seats.add(seat_id)
        neighbors[seat_id - 1] += 1
        neighbors[seat_id + 1] += 1

    if draw:
        me = [x for x in neighbors if neighbors[x] == 2 and x not in seats][0]

        grid[me % 8, me // 8] = "target"
        grid.save_frame()

        grid.draw_frames(repeat_final=30)
        Grid.make_animation(file_format="mp4", output_name="animation_%02d" % (get_desc()[0],))

    if mode == 1:
        return max(seats)
    else:
        return [x for x in neighbors if neighbors[x] == 2 and x not in seats][0]

def other_draw(describe, values):
    if describe:
        return "Animate this"
    else:
        from dummylog import DummyLog
        calc(DummyLog(), values, 1, draw=True)


def test(log):
    values = log.decode_values("""
        FBFBBFFRLR
    """)
    log.test(calc(log, values, 1), 357)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)

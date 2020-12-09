#!/usr/bin/env python3

def get_desc():
    return 8, 'Day 8: Space Image Format'


def calc(log, values, width, height):
    from collections import defaultdict
    from grid import Grid

    # Break the input string into a series of layers
    value = values[0]
    layers = []
    while len(value) > 0:
        layers.append(value[:width * height])
        value = value[width * height:]

    best_layer, best_count = None, None
    # Count up the layer with the most "0"s in it.
    for i in range(len(layers)):
        counts = defaultdict(int)
        for x in layers[i]:
            counts[x] += 1
        if best_count is None or counts["0"] < best_count:
            best_count = counts["0"]
            best_layer = counts

    # Merge all of the layers
    grid = Grid(default=".")
    for layer in layers:
        for i in range(width * height):
            x, y = i % width, i // width
            if grid.get(x, y) == "." and layer[i] in {"1", "0"}:
                # "Turn "1" into "#" to make it easier to read
                grid.set("#" if layer[i] == "1" else " ", x, y)

    # Show the output, don't try to decode these giant letters
    log("")
    grid.show_grid(log)
    grid.decode_grid(log)
    # grid.draw_grid()
    log("")

    # And return the number of "1" * "2" on the best layer
    return best_layer["1"] * best_layer["2"]


def test(log):
    values = log.decode_values("""
        123456789012
    """)

    ret, expected = calc(log, values, 3, 2), 1
    log("Test returned %s, expected %s" % (str(ret), str(expected)))
    if ret != expected:
        return False

    return True


def other_glyphs(describe, values):
    if describe:
        return "Dump out all glyphs"

    from grid import Grid, DECODE_GLYPHS

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    dump = 'glyphs = {\n'

    grid = Grid()
    x_off = 0
    for cur in letters:
        grid_letter = Grid()
        value = 0
        for key in DECODE_GLYPHS:
            if DECODE_GLYPHS[key] == cur:
                value = key
        if value > 0:
            for y in range(5, -1, -1):
                for x in range(4, -1, -1):
                    if value % 2 == 1:
                        grid_letter.set(1, x, y)
                        grid.set(1, x + x_off, y)
                    value = value // 2
            for y in range(6):
                dump += '    "'
                for x in range(5):
                    dump += '.' if grid_letter.get(x, y) == 0 else "#"
                if y == 5:
                    dump += '":   "' + cur + '",\n\n'
                else:
                    dump += '" +\n'
        
        x_off += 6
    grid.draw_grid()
    dump += "}\n"

    with open("glyphs.txt", "w") as f:
        f.write(dump)
    print("Created glyphs.txt and frame_00000.png")


def run(log, values):
    log("Part 1: " + str(calc(log, values, 25, 6)))

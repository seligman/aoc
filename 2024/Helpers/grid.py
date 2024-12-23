#!/usr/bin/env python3

# BLOCK = u"\u2588"
# SPACE = u" "
BLOCK = "#"
SPACE = " "
LINE_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)
DEFAULT_COLOR_MAP = {
    0: (0, 0, 0),
    ' ': (0, 0, 0),
    '.': (0, 0, 0),
    1: (255, 255, 255),
    '#': (255, 255, 255),
    'Star': (255, 255, 0),
    'star': (255, 255, 0),
    'Target': (192, 192, 255),
    'target': (192, 192, 255),
    'Gray': (192, 192, 192),
    'DarkGray': (96, 96, 96),
}
DEFAULT_DISP_MAP = {
    ' ': SPACE,
    0: SPACE,
    '.': SPACE,
    '#': BLOCK,
    1: BLOCK,
}


DECODE_GLYPHS = {
    422148690: "A",
    959335004: "B",
    422068812: "C",
    1024344606: "E",
    1024344592: "F",
    422074958: "G",
    623856210: "H",
    203491916: "J",
    625758866: "K",
    554189342: "L",
    422136396: "O",
    959017488: "P",
    959017618: "R",
    243537966: "S",
    623462988: "U",
    588583044: "Y",
    1008869918: "Z",
    0: " "
}

def encode_grid(value, log=print):
    if log is None:
        log = lambda x: None
    reversed = {y: x for x, y in DECODE_GLYPHS.items()}
    code = 1
    ret = []
    for y in range(1,7):
        line = ""
        for cur in value:
            for x in range(5):
                code = 2 ** (((4-x) + (6-y) * 5))
                if (reversed.get(cur, 0) & code) > 0:
                    line += "#"
                else:
                    line += " "
        if log is not None:
            log('"' + line + '",')
        ret.append(line)
    return ret

def decode_grid(x_min, x_max, y_min, y_max, get_cell, log=print):
    if log is None:
        log = lambda x: None
    spaces = {" ", ".", 0}
    start_x = x_min
    while start_x <= x_max:
        end = False
        for y in range(y_min, y_max + 1):
            if get_cell(start_x, y) not in spaces:
                end = True
                break
        if end:
            break
        else:
            start_x += 1

    start_y = y_min
    while start_y <= y_max:
        end = False
        for x in range(x_min, x_max + 1):
            if get_cell(x, start_y) not in spaces:
                end = True
                break
        if end:
            break
        else:
            start_y += 1

    ret = ""

    for off_y in range(y_min, y_max + 1, 7):
        if len(ret) > 0:
            ret += "/"
        for off_x in range(start_x, x_max + 1, 5):
            disp = []
            code = 0
            for y in range(6):
                disp.append("")
                for x in range(5):
                    disp[-1] += " " if get_cell(x + off_x, y + off_y) in spaces else "#"
                    code *= 2
                    code += 0 if get_cell(x + off_x, y + off_y) in spaces else 1
            if code in DECODE_GLYPHS:
                ret += DECODE_GLYPHS[code]
            else:
                ret += "?"
                for cur in disp:
                    log("Unknown Glyph: " + cur)
                log("Code: " + str(code))

    log("That decodes to: " + ret)
    return ret

def decode_example_function():
    # This turns some letters into a grid of strings:
    encode_grid("HELLO")

    # And this does the reverse:
    grid = [
        "#  # #### #    #     ##  ",
        "#  # #    #    #    #  # ",
        "#### ###  #    #    #  # ",
        "#  # #    #    #    #  # ",
        "#  # #    #    #    #  # ",
        "#  # #### #### ####  ##  ",
    ]
    decode_grid(0, len(grid[0]) - 1, 0, len(grid) - 1, lambda x, y: grid[y][x])


class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x=0, y=0):
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y
    
    @property
    def tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other[0], self.y - other[1])

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other[0], self.y + other[1])

    def __repr__(self):
        return f"{self.x},{self.y}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def line_to(self, other, include_perc=False):
        if self.x == other.x and not include_perc:
            for y in range(min(self.y, other.y), max(self.y, other.y) + 1):
                yield Point(self.x, y)
        elif self.y == other.y and not include_perc:
            for x in range(min(self.x, other.x), max(self.x, other.x) + 1):
                yield Point(x, self.y)
        else:
            points = max(abs(self.x - other.x), abs(self.y - other.y)) + 1
            for i in range(points):
                perc = i / (points - 1)
                if include_perc:
                    yield Point(round((1 - perc) * self.x + perc * other.x), round((1 - perc) * self.y + perc * other.y)), perc
                else:
                    yield Point(round((1 - perc) * self.x + perc * other.x), round((1 - perc) * self.y + perc * other.y))

class Grid:
    def __init__(self, default=0):
        self.grid = {}
        self.default = default
        self.frame = 0
        self.frames = []
        self.fonts = None
        self.values = None
        self.extra = {}
        self._ranges = {}
        self.pass_to_quick = False

    def side(self, side_type, i):
        if side_type in {'column', 0}:
            return self.column(i)
        elif side_type in {'row', 1}:
            return self.row(i)
        else:
            raise Exception()

    def column(self, x):
        if x < 0:
            x = self.width() + x
        return "".join([self[x, y] for y in self.y_range()])

    def row(self, y):
        if y < 0:
            y = self.height() + y
        return "".join([self[x, y] for x in self.x_range()])

    def enum_rotates(self):
        for _ in range(2):
            self.flip_x()
            for _ in range(4):
                self.rotate()
                yield self

    def copy(self):
        ret = Grid()
        ret.grid = self.grid.copy()
        ret.frames = self.frames
        ret.extra = self.extra.copy()
        return ret

    def rotate(self):
        temp = {}
        for x in self.x_range():
            for y in self.y_range():
                temp[(x, y)] = self[x, y]

        width = self.width() - 1
        for x in self.x_range():
            for y in self.y_range():
                self[(y, width - x)] = temp[(x, y)]

    def flip_x(self):
        temp = {}
        for x in self.x_range():
            for y in self.y_range():
                temp[(x, y)] = self[x, y]
        width = self.width() - 1
        for x in self.x_range():
            for y in self.y_range():
                self[(width - x, y)] = temp[(x, y)]

    def flip_y(self):
        temp = {}
        for x in self.x_range():
            for y in self.y_range():
                temp[(x, y)] = self[x, y]
        height = self.height() - 1
        for x in self.x_range():
            for y in self.y_range():
                self[(x, height - y)] = temp[(x, y)]

    @staticmethod
    def cardinal(compass, x=0, y=0):
        if compass == "e":
            x += 1
        elif compass == "w":
            x -= 1
        elif compass == "s":
            y += 1
        elif compass == "n":
            y -= 1
        else:
            raise Exception()
        return x, y

    @staticmethod
    def cardinal_hex(compass, x=0, y=0):
        if compass == "e":
            x += 2
        elif compass == "w":
            x -= 2
        elif compass == "se":
            y += 1
            x += 1
        elif compass == "sw":
            y += 1
            x -= 1
        elif compass == "ne":
            y -= 1
            x += 1
        elif compass == "nw":
            y -= 1
            x -= 1
        else:
            raise Exception()
        return x, y

    @staticmethod
    def get_dirs_hex(offset=None):
        ret = [(-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1)]
        if offset is not None:
            ret = [(x + offset[0], y + offset[1]) for x, y in ret]
        return ret

    @staticmethod
    def get_dirs(axis_count, offset=None, diagonal=True):
        ret = []

        if diagonal:
            temp = [-1] * axis_count
            found = True
            while found:
                if sum([abs(x) for x in temp]) > 0:
                    ret.append(tuple(temp))
                found = False
                i = len(temp) - 1
                while True:
                    temp[i] += 1
                    if temp[i] == 2:
                        temp[i] = -1
                        i -= 1
                        if i == -1:
                            break
                    else:
                        found = True
                        break
        else:
            temp = [0] * axis_count
            for i in range(axis_count):
                temp[i] = -1
                ret.append(tuple(temp))
                temp[i] = 1
                ret.append(tuple(temp))
                temp[i] = 0

        if offset is not None:
            ret = [tuple(a+b for a,b in zip(pt, offset)) for pt in ret]

        return ret

    def blit(self, source, x, y, color_map=None, text_map=None):
        for xo in source.x_range():
            for yo in source.y_range():
                value = source[xo, yo]
                if isinstance(value, list):
                    raise Exception()
                if color_map is not None:
                    value = [value, color_map[value]]
                    if text_map is not None:
                        value[0] = text_map[value[0]]
                else:
                    if text_map is not None:
                        value = text_map[value]
                self[x + xo, y + yo] = value

    @staticmethod
    def from_text(values, axis=2, default=0):
        grid = Grid(default=default)
        if isinstance(values, str):
            if "\n" in values:
                values = values.split("\n")
            else:
                values = [values]
        y = 0
        for row in values:
            x = 0
            for cur in row:
                if axis == 1:
                    grid.set(cur, x)
                elif axis == 2:
                    grid.set(cur, x, y)
                else:
                    raise Exception()
                x += 1
            y += 1
        return grid

    @staticmethod
    def make_animation(frame_rate=30, file_format="mp4", output_name="animation"):
        import os
        import subprocess
        output_name = os.path.join("animations", output_name + "." + file_format)

        if os.path.isfile(output_name):
            os.unlink(output_name)

        cmd = [
            "ffmpeg", "-y",
            "-hide_banner",
            "-f", "image2",
            "-framerate", str(frame_rate), 
            "-i", "frame_%05d.png", 
            "-c:v", "libx264", 
            "-profile:v", "main", 
            "-pix_fmt", "yuv420p", 
            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
            "-an", 
            "-movflags", "+faststart",
            output_name,
        ]
        print("$ " + " ".join(cmd))
        subprocess.check_call(cmd)

    def __getitem__(self, key):
        if isinstance(key, Point):
            return self.grid.get(key.tuple, self.default)
        elif isinstance(key, tuple):
            return self.grid.get(key, self.default)
        else:
            return self.grid.get((key,), self.default)

    def __delitem__(self, key):
        if isinstance(key, Point):
            del self.grid[key.tuple]
        elif isinstance(key, tuple):
            del self.grid[key]
        else:
            del self.grid[(key,)]

    def __iter__(self):
        return self.grid.values().__iter__()

    def __contains__(self, key):
        if isinstance(key, Point):
            return key.tuple in self.grid
        elif isinstance(key, tuple):
            return key in self.grid
        else:
            return (key,) in self.grid

    def pad(self, num_to_pad, value=None):
        if value is None:
            value = self.default
        min_x, max_x = self.axis_min(0), self.axis_max(0)
        min_y, max_y = self.axis_min(1), self.axis_max(1)
        self[min_x - num_to_pad, min_y - num_to_pad] = value
        self[max_x + num_to_pad, max_y + num_to_pad] = value

    def ensure_ratio(self, ratio, value=None):
        if value is None:
            value = self.default
        if self.width() / self.height() < ratio:
            target = (int((ratio * self.height()) + 0.5) - self.width()) // 2
            min_x, max_x = self.axis_min(0), self.axis_max(0)
            self[max_x + target, 0] = value
            self[min_x - target, 0] = value
        elif self.width() / self.height() > ratio:
            target = (int((self.width() / ratio) + 0.5) - self.height()) // 2
            min_y, max_y = self.axis_min(1), self.axis_max(1)
            self[0, max_y + target] = value
            self[0, min_y - target] = value

    def set_text(self, x, y, text, color=None):
        for xo in range(len(text)):
            if color is None:
                self[x + xo, y] = text[xo]
            else:
                self[x + xo, y] = [text[xo], color]

    def get(self, *coords):
        return self.grid.get(coords, self.default)

    def axis_min(self, axis):
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = (min([x[axis] for x in self.grid]), max([x[axis] for x in self.grid]))
        return self._ranges[axis][0]

    def axis_max(self, axis):
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = (min([x[axis] for x in self.grid]), max([x[axis] for x in self.grid]))
        return self._ranges[axis][1]

    def axis_size(self, axis):
        return self.axis_max(axis) - self.axis_min(axis) + 1

    def width(self):
        return self.axis_size(0)

    def height(self):
        return self.axis_size(1)

    def axis_range(self, axis, pad=0):
        return range(self.axis_min(axis) - pad, self.axis_max(axis) + 1 + pad)

    def x_range_hex(self, y, pad=0):
        if y % 2 == 0:
            return [x for x in self.x_range(pad=pad) if x % 2 == 0]
        else:
            return [x for x in self.x_range(pad=pad) if x % 2 == 1]

    def xy_range(self, pad=0):
        for x in self.axis_range(0, pad=pad):
            for y in self.axis_range(1, pad=pad):
                yield x, y

    def axises_range(self, axis_count, axis_start=0, pad=0):
        if axis_count == 1:
            for x in self.axis_range(axis_start, pad=pad):
                yield (x,)
        else:
            for x in self.axis_range(axis_start, pad=pad):
                for y in self.axises_range(axis_count-1, axis_start+1, pad=pad):
                    yield (x,) + y

    def x_range(self, pad=0):
        return self.axis_range(0, pad=pad)

    def y_range(self, pad=0):
        return self.axis_range(1, pad=pad)

    def __setitem__(self, key, value):
        self._ranges = {}
        if isinstance(key, Point):
            self.grid[key.tuple] = value
        elif isinstance(key, tuple):
            self.grid[key] = value
        else:
            self.grid[(key,)] = value

    def set(self, value, *coords):
        self._ranges = {}
        self.grid[coords] = value

    def value_isset(self, *coords):
        return coords in self.grid

    def decode_grid(self, log):
        return decode_grid(
            self.axis_min(0),
            self.axis_max(0),
            self.axis_min(1),
            self.axis_max(1),
            lambda x, y: self[x, y],
            log=log
        )
            
    def dump_grid(self):
        return "".join([str(self.grid[x]) for x in sorted(self.grid)])

    def show_grid(self, log, disp_map=DEFAULT_DISP_MAP, dump_all=False):
        for y in self.y_range():
            line = ""
            for x in self.x_range():
                if dump_all:
                    line += str(self.grid.get((x, y), self.default))
                else:
                    line += disp_map[self.grid.get((x, y), self.default)]
            log(line)

    def show_grid_hex(self, log, disp_map=DEFAULT_DISP_MAP, dump_all=False):
        for y in self.y_range():
            line = ""
            for x in self.x_range():
                if (y % 2 == 0 and x % 2 == 1) or (y % 2 == 1 and x % 2 == 0):
                    line += ' '
                else:
                    if dump_all:
                        line += self.grid.get((x, y), self.default)
                    else:
                        line += disp_map[self.grid.get((x, y), self.default)]
            log(line)

    def dump_grid_hex(self):
        ret = []
        for y in self.y_range():
            line = ""
            for x in self.x_range():
                if (y % 2 == 0 and x % 2 == 1) or (y % 2 == 1 and x % 2 == 0):
                    line += ' '
                else:
                    line += self.grid.get((x, y), self.default)
            ret.append(line)
        return "|".join(ret)

    def get_grid_hex_size(self):
        return {
                'width': max(len(self.x_range_hex(0)), len(self.x_range_hex(1))),
                'height': self.height(),
                'x_min': self.axis_min(0),
                'y_min': self.axis_min(1),
            }

    def draw_grid_hex(self, image_copies=1, hex_size=10, color_map=DEFAULT_COLOR_MAP, size=None, background_color=BACKGROUND_COLOR, outline=BACKGROUND_COLOR, show_all=False, scale=1.0):
        from PIL import Image, ImageDraw

        hex = (
            ( 0.5773502691896257,  1.3333333333333333),
            ( 1.1547005383792515,  1.0000000000000000),
            ( 1.1547005383792515,  0.3333333333333333),
            ( 0.5773502691896257,  0.0000000000000000),
            ( 0.0000000000000000,  0.3333333333333333),
            ( 0.0000000000000000,  1.0000000000000000),
        )
        hex_width = 1.1547005383792515

        if size is None:
            size = self.get_grid_hex_size()
        image_width = int(size['width'] * (hex_size * hex_width) + 0.5)
        image_height = int(size['height'] * hex_size + hex_size / 3 + 0.5)
        
        im = Image.new('RGB', (image_width, image_height), background_color)
        dr = ImageDraw.Draw(im)

        for y in range(size['y_min'] - 2, size['y_min'] + size['height'] + 4) if show_all else self.y_range():
            if show_all:
                temp_x_range = list(range(size['x_min'] - 4, size['x_min'] + size['width'] * 2 + 8))
                if y % 2 == 0:
                    temp_x_range = [x for x in temp_x_range if x % 2 == 0]
                else:
                    temp_x_range = [x for x in temp_x_range if x % 2 == 1]
            else:
                temp_x_range = list(self.x_range_hex(y))
            for x in temp_x_range:
                if show_all or (x, y) in self.grid:
                    cell_y = y - size['y_min']
                    cell_x = (x - size['x_min']) / 2
                    temp = [(cell_x * (hex_width * hex_size) + x * hex_size, cell_y * (hex_size) + y * hex_size) for x, y in hex]
                    min_x = min([x[0] for x in temp])
                    max_x = min([x[0] for x in temp])
                    min_y = min([x[1] for x in temp])
                    max_y = min([x[1] for x in temp])
                    if max_x >= -50 and max_y >= -50 and min_x <= image_width + 50 and min_y <= image_height + 50:
                        color = color_map[self[x, y]]
                        dr.polygon(temp, fill=color, outline=outline)

        if scale != 0.0:
            im = im.resize((int(image_width * scale), int(image_height * scale)), resample=Image.LANCZOS)

        for _ in range(image_copies):
            im.save("frame_%05d.png" % (self.frame,))
            self.frame += 1

    def remove_last_frame(self):
        self.frames.pop(-1)

    def save_frame(self, extra_text=None, extra=None, final_frame=False):
        temp = {k: (v[:] if isinstance(v, list) else v) for k, v in self.grid.items()}
        if self.pass_to_quick:
            self.quick_frame += 1
            self.queue.put({
                "grid": temp,
                "ranges": self._ranges,
                "msg": "Working, on frame %5d of %5d" % (self.quick_frame, 0),
                "frame": self.quick_frame - 1,
                "args": {
                    "color_map": self.quick_args['color_map'], 
                    "cell_size": self.quick_args['cell_size'], 
                    "extra_text": extra_text, 
                    "extra_text_rows": self.quick_args['max_rows'], 
                    "image_copies": 1 + self.quick_args['repeat_final'] if final_frame else 1,
                    "extra": extra,
                    "extra_callback": self.quick_args['extra_callback'],
                    "show_lines": self.quick_args['show_lines'],
                    "font_size": self.quick_args['font_size'],
                    "scale": self.quick_args['scale'],
                }
            })
        else:
            self.frames.append((temp, extra_text, extra))

    def neighbors(self, *args, diagonals=False, valid_only=False):
        if isinstance(args[0], tuple):
            x, y = args[0]
        else:
            x, y = args
        if diagonals:
            offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        else:
            offsets = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for ox, oy in offsets:
            ox = ox + x
            oy = oy + y
            if not valid_only or (ox, oy) in self.grid:
                yield ox, oy

    @staticmethod
    def clear_frames():
        import os
        import re
        for cur in os.listdir("."):
            if re.search("frame_[0-9]{5}\\.png", cur):
                os.unlink(cur)

    def draw_frames_quickly(self, color_map=DEFAULT_COLOR_MAP, cell_size=(10, 10), repeat_final=0, font_size=10, extra_callback=None, show_lines=True, use_multiproc=True, scale=None):
        import multiprocessing
        queue = multiprocessing.Queue(multiprocessing.cpu_count() * 2)
        procs = [multiprocessing.Process(target=draw_frames_worker, args=(i, queue,)) for i in range(multiprocessing.cpu_count())]
        [x.start() for x in procs]
        self.pass_to_quick = True
        self.quick_frame = 0
        self.procs = procs
        self.queue = queue
        max_rows = 0
        for _grid, extra_text, _extra in self.frames:
            if extra_text is not None:
                max_rows = max(max_rows, len(extra_text))
        self.quick_args = {
            "color_map": color_map, 
            "cell_size": cell_size, 
            "repeat_final": repeat_final, 
            "font_size": font_size, 
            "extra_callback": extra_callback, 
            "show_lines": show_lines, 
            "use_multiproc": use_multiproc, 
            "scale": scale,
            "max_rows": max_rows,
        }

    def finish_quick_draw(self):
        for _ in self.procs:
            self.queue.put(None)
        [x.join() for x in self.procs]

    def ease_frames(self, rate=10, secs=5, frames=None):
        if frames is None:
            target = self.frames
        else:
            target = frames

        import math

        target_count = rate * secs

        def ease(x):
            x = min(1, max(0, x))
            return -(math.cos(math.pi * x) - 1) / 2 # sine
            # return (8 * x * x * x * x) if (x < 0.5) else (1 - ((-2 * x + 2) ** 4) / 2) # cubic

        hits = [int((ease(x / target_count) * (len(target) - 1)) + 0.5) for x in range(target_count + 1)]

        if frames is None:
            self.frames = [self.frames[x] for x in hits]
        else:
            temp = [target[x] for x in hits]
            frames.clear()
            frames.extend(temp)

    def draw_frames(self, color_map=DEFAULT_COLOR_MAP, cell_size=(10, 10), repeat_final=0, font_size=10, text_xy=None, extra_callback=None, show_lines=True, use_multiproc=True, scale=None):
        from datetime import datetime, timedelta
        import multiprocessing
        import sys
        if sys.version_info >= (3, 11): from datetime import UTC
        else: import datetime as datetime_fix; UTC=datetime_fix.timezone.utc

        msg = datetime.now(UTC).replace(tzinfo=None)
        print("Creating animation...")
        temp = self.grid
        self._ranges = {}
        self.width()
        self.height()

        max_rows = 0
        for _grid, extra_text, _extra in self.frames:
            if extra_text is not None:
                max_rows = max(max_rows, len(extra_text))

        todo = []

        for i, (grid, extra_text, extra) in enumerate(self.frames):
            i += 1
            todo.append({
                "grid": grid,
                "ranges": self._ranges,
                "msg": "Working, on frame %5d of %5d" % (i, len(self.frames)),
                "frame": i - 1,
                "args": {
                    "color_map": color_map, 
                    "cell_size": cell_size, 
                    "extra_text": extra_text, 
                    "extra_text_rows": max_rows, 
                    "image_copies": 1 + repeat_final if i == len(self.frames) else 1,
                    "extra": extra,
                    "extra_callback": extra_callback,
                    "show_lines": show_lines,
                    "font_size": font_size,
                    "scale": scale,
                    "text_xy": text_xy,
                }
            })

        if use_multiproc:
            with multiprocessing.Pool() as pool:
                left = len(todo)
                for result in pool.imap_unordered(draw_frames_helper, todo):
                    if datetime.now(UTC).replace(tzinfo=None) >= msg:
                        while datetime.now(UTC).replace(tzinfo=None) >= msg:
                            msg += timedelta(seconds=5)
                        print(f"{result}, {left:5d} left")
                    left -= 1
        else:
            for cur in todo:
                if datetime.now(UTC).replace(tzinfo=None) >= msg:
                    while datetime.now(UTC).replace(tzinfo=None) >= msg:
                        msg += timedelta(seconds=5)
                    print(cur["msg"])
                self.grid = cur["grid"]
                self._ranges = cur["ranges"]
                self.draw_grid(**(cur["args"]))

        print("Done with drawing")
        self.grid = temp

    def get_font(self, font_size):
        from PIL import Image, ImageDraw, ImageFont
        import os
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))
        return source_code

    def get_font_size(self, font_size):
        from PIL import Image, ImageDraw, ImageFont
        import os
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))
        w, h = 0, 0
        for x in range(32, 126):
            test = source_code.getbbox(chr(x))
            w, h = max(w, test[2]), max(h, test[3])
        return w, h

    def draw_grid(self, color_map=DEFAULT_COLOR_MAP, cell_size=(10, 10), extra_text=None, extra_text_rows=0, 
        font_size=14, image_copies=1, extra=None, extra_callback=None, text_xy=None, show_lines=True, default_color=(64, 64, 64), return_image=False, scale=None):
        from PIL import Image, ImageDraw, ImageFont
        import os
        width = self.width()
        height = self.height()

        for_text = 0
        if self.fonts is None:
            source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
            segmented = os.path.join('Helpers', 'Font-DSEG14Classic-Bold.ttf')
            if os.path.isfile(source_code) and os.path.isfile(segmented):
                self.fonts = [
                    ImageFont.truetype(source_code, int(float(font_size) * 1.5)),
                    ImageFont.truetype(segmented, font_size),
                ]

        if extra_text is not None or extra_text_rows > 0:
            fnt_source = self.fonts[0]
            fnt_segment = self.fonts[1]

            fnt_height = max(fnt_source.getbbox("0")[3], fnt_segment.getbbox("0")[3])
            fnt_diff = fnt_source.getbbox("0")[3] - fnt_segment.getbbox("0")[3]
            if text_xy is None:
                if extra_text_rows is None:
                    for_text = fnt_height * (len(extra_text) + 1)
                else:
                    for_text = fnt_height * (extra_text_rows + 1)

        border = 5

        im = Image.new('RGB', (
            width * (cell_size[0] + 1) + 1 + (border * 2), 
            height * (cell_size[1] + 1) + 1 + (border * 2) + for_text,
        ), color=BACKGROUND_COLOR)

        offset = height * (cell_size[1] + 1) + 1 + (border * 2)

        d = ImageDraw.Draw(im, 'RGBA')

        if show_lines:
            d.rectangle(
                (
                    (border, border), 
                    (border + width * (cell_size[0] + 1), border + height * (cell_size[0] + 1))
                ), 
                LINE_COLOR, 
                LINE_COLOR,
            )

        for x in range(width):
            for y in range(height):
                color = self.grid.get((x + self.axis_min(0), y + self.axis_min(1)), self.default)
                use = True
                if not show_lines:
                    if color == 0:
                        use = False
                if use:
                    text = None
                    text_color = (255, 255, 255)
                    if isinstance(color, list) or isinstance(color, tuple):
                        if len(color) == 2:
                            text, color = color
                        else:
                            text, color, text_color = color
                    else:
                        if color in color_map:
                            color = color_map[color]
                        else:
                            text = color
                            color = default_color
                    d.rectangle(
                        (
                            (border + x * (cell_size[0] + 1) + 1, border + y * (cell_size[1] + 1) + 1), 
                            (border + x * (cell_size[0] + 1) + cell_size[0] + (0 if show_lines else 1), border + y * (cell_size[1] + 1) + cell_size[1] + (0 if show_lines else 1))
                        ),
                        color, color
                    )
                    if text is not None:
                        for part in text.split("\b"):
                            w = d.textlength(part, font=self.fonts[0])
                            h = self.fonts[0].size
                            d.text((
                                border + x * (cell_size[0] + 1) + 1 + (cell_size[0] - w) / 2, 
                                border + y * (cell_size[1] + 1) + 1 + (cell_size[1] - h) / 2), 
                                part, fill=text_color, font=self.fonts[0])

        if extra_text is not None:
            y = offset if text_xy is None else text_xy[1]
            for row in extra_text:
                swap = True
                x = 10 if text_xy is None else text_xy[0]
                for part in row.split("|"):
                    swap = not swap
                    d.text((x, y + (fnt_diff if swap else 0)), part, (255, 255, 255), font=fnt_segment if swap else fnt_source)
                    x += (fnt_segment if swap else fnt_source).getbbox(part)[2]
                y += fnt_height

        if extra_callback is not None:
            if extra is not None:
                if 'x' in extra and 'y' in extra:
                    extra['x_calc'], extra['y_calc'] = (
                        border + extra['x'] * (cell_size[0] + 1) + 1 + cell_size[0] / 2, 
                        border + extra['y'] * (cell_size[1] + 1) + 1 + cell_size[1] / 2,
                    )
            extra_callback(d, extra)
        del d

        if scale is not None:
            im = im.resize((int(im.width * scale), int(im.height * scale)), resample=Image.LANCZOS)

        if return_image:
            return im

        for _ in range(image_copies):
            im.save("frame_%05d.png" % (self.frame,))
            self.frame += 1

def draw_frames_worker(worker_id, queue):
    while True:
        job = queue.get()
        if job is None:
            break
        msg = draw_frames_helper(job)
        if worker_id == 0:
            print(msg)

def draw_frames_helper(cur):
    grid = Grid()
    grid.grid = cur["grid"]
    grid._ranges = cur["ranges"]
    grid.frame = cur["frame"]
    grid.draw_grid(**cur["args"])
    return cur["msg"]

def get_ints(line):
    ret = [""]
    for x in line:
        if len(ret[-1]) == 0 and x == "-":
            ret[-1] = "-"
        elif "0" <= x <= "9":
            ret[-1] += x
        else:
            if len(ret[-1]) > 0:
                ret.append("")
    if len(ret[-1]) == 0:
        ret.pop(-1)
    return list(map(int, ret))

def get_floats(line):
    ret = [""]
    for x in line:
        if x == "-" and len(ret[-1]) == 0:
            ret[-1] = "-"
        elif "0" <= x <= "9":
            ret[-1] += x
        elif x == "." and "." not in ret[-1]:
            ret[-1] += x
        else:
            if len(ret[-1]) > 0:
                ret.append("")
    if len(ret[-1]) == 0:
        ret.pop(-1)
    return list(map(float, ret))

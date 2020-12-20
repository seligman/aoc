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
        self._all_sides = None
        self._all_rotations = None

    def column(self, x):
        if x < 0:
            x = self.width() + x
        return "".join([self[x, y] for y in self.y_range()])

    def row(self, y):
        if y < 0:
            y = self.height() + y
        return "".join([self[x, y] for x in self.x_range()])

    def all_sides(self):
        if self._all_sides is None:
            self._all_sides = set([
                self.column(0),
                self.column(-1),
                self.row(0),
                self.row(-1),
                self.column(0)[::-1],
                self.column(-1)[::-1],
                self.row(0)[::-1],
                self.row(-1)[::-1],
            ])
        return self._all_sides

    def enum_rotates(self):
        if self._all_rotations is None:
            temp = []
            for _ in range(2):
                self.flip_x()
                for _ in range(4):
                    self.rotate()
                    temp.append(self.grid.copy())
            self._all_rotations = temp
        for cur in self._all_rotations:
            self.grid = cur
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
    def get_dirs(axis_count):
        ret = []
        temp = [-1] * axis_count
        found = True
        while found:
            if sum([abs(x) for x in temp]) > 0:
                ret.append(temp[:])
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
        return ret

    def blit(self, source, x, y):
        for xo in source.x_range():
            for yo in source.y_range():
                self[x + xo, y + yo] = source[xo, yo]

    @staticmethod
    def from_text(values, axis=2):
        grid = Grid()
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
        if isinstance(key, tuple):
            return self.grid.get(key, self.default)
        else:
            return self.grid.get((key,), self.default)

    def __delitem__(self, key):
        if isinstance(key, tuple):
            del self.grid[key]
        else:
            del self.grid[(key,)]

    def __iter__(self):
        return self.grid.values().__iter__()

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

    def x_range(self):
        return self.axis_range(0)

    def y_range(self):
        return self.axis_range(1)

    def __setitem__(self, key, value):
        self._ranges = {}
        self._all_rotations = None
        if isinstance(key, tuple):
            self.grid[key] = value
        else:
            self.grid[(key,)] = value

    def set(self, value, *coords):
        self._ranges = {}
        self._all_rotations = None
        self.grid[coords] = value

    def value_isset(self, *coords):
        return coords in self.grid

    def decode_grid(self, log):
        spaces = {" ", ".", 0}
        start_x = self.axis_min(0)
        while start_x <= self.axis_max(0):
            end = False
            for y in self.y_range():
                if self.get(start_x, y) not in spaces:
                    end = True
                    break
            if end:
                break
            else:
                start_x += 1

        start_y = self.axis_min(1)
        while start_y <= self.axis_max(1):
            end = False
            for x in self.x_range():
                if self.get(x, start_y) not in spaces:
                    end = True
                    break
            if end:
                break
            else:
                start_y += 1

        ret = ""

        for off_y in range(start_y, self.axis_max(1) + 1, 7):
            if len(ret) > 0:
                ret += "/"
            for off_x in range(start_x, self.axis_max(0) + 1, 5):
                disp = []
                code = 0
                for y in range(6):
                    disp.append("")
                    for x in range(5):
                        disp[-1] += " " if self.get(x + off_x, y + off_y) in spaces else "#"
                        code *= 2
                        code += 0 if self.get(x + off_x, y + off_y) in spaces else 1
                if code in DECODE_GLYPHS:
                    ret += DECODE_GLYPHS[code]
                else:
                    ret += "?"
                    for cur in disp:
                        log("Unknown Glyph: " + cur)
                    log("Code: " + str(code))

        log("That decodes to: " + ret)
            
    def dump_grid(self):
        return "".join([self.grid[x] for x in sorted(self.grid)])

    def show_grid(self, log, disp_map=DEFAULT_DISP_MAP, dump_all=False):
        for y in self.y_range():
            line = ""
            for x in self.x_range():
                if dump_all:
                    line += self.grid.get((x, y), self.default)
                else:
                    line += disp_map[self.grid.get((x, y), self.default)]
            log(line)

    def save_frame(self, extra_text=None, extra=None):
        self.frames.append((self.grid.copy(), extra_text, extra))

    @staticmethod
    def clear_frames():
        import os
        import re
        for cur in os.listdir("."):
            if re.search("frame_[0-9]{5}\\.png", cur):
                os.unlink(cur)

    def draw_frames(self, color_map=DEFAULT_COLOR_MAP, cell_size=(10, 10), repeat_final=0, font_size=10, extra_callback=None, show_lines=True):
        from datetime import datetime, timedelta

        msg = datetime.utcnow()
        print("Creating animation...")
        temp = self.grid
        self._ranges = {}
        self._all_rotations = None
        self.width()
        self.height()

        max_rows = 0
        for _grid, extra_text, _extra in self.frames:
            if extra_text is not None:
                max_rows = max(max_rows, len(extra_text))

        i = 0
        for grid, extra_text, extra in self.frames:
            i += 1
            if datetime.utcnow() >= msg:
                msg += timedelta(seconds=1)
                print("Working, on frame %5d of %5d" % (i, len(self.frames)))
            self.grid = grid
            self.draw_grid(
                color_map=color_map, 
                cell_size=cell_size, 
                extra_text=extra_text, 
                extra_text_rows=max_rows, 
                image_copies=1 + repeat_final if i == len(self.frames) else 1,
                extra=extra,
                extra_callback=extra_callback,
                show_lines=show_lines
            )

        print("Done with drawing")
        self.grid = temp

    def get_font_size(self, font_size):
        from PIL import Image, ImageDraw, ImageFont
        import os
        source_code = os.path.join('Helpers', 'Font-SourceCodePro-Bold.ttf')
        source_code = ImageFont.truetype(source_code, int(float(font_size) * 1.5))
        w, h = 0, 0
        for x in range(32, 126):
            test = source_code.getsize(chr(x))
            w, h = max(w, test[0]), max(h, test[1])
        return w, h

    def draw_grid(self, color_map=DEFAULT_COLOR_MAP, cell_size=(10, 10), extra_text=None, extra_text_rows=0, 
        font_size=14, image_copies=1, extra=None, extra_callback=None, text_xy=None, show_lines=True, default_color=(64, 64, 64)):
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

            fnt_height = max(fnt_source.getsize("0")[1], fnt_segment.getsize("0")[1])
            fnt_diff = fnt_source.getsize("0")[1] - fnt_segment.getsize("0")[1]
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
                    if isinstance(color, list):
                        text, color = color
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
                        w, h = d.textsize(text, font=self.fonts[0])
                        d.text((
                            border + x * (cell_size[0] + 1) + 1 + (cell_size[0] - w) / 2, 
                            border + y * (cell_size[1] + 1) + 1 + (cell_size[1] - h) / 2), 
                            text, fill=(255, 255, 255), font=self.fonts[0])

        if extra_text is not None:
            y = offset if text_xy is None else text_xy[1]
            for row in extra_text:
                swap = True
                x = 10 if text_xy is None else text_xy[0]
                for part in row.split("|"):
                    swap = not swap
                    d.text((x, y + (fnt_diff if swap else 0)), part, (255, 255, 255), font=fnt_segment if swap else fnt_source)
                    x += (fnt_segment if swap else fnt_source).getsize(part)[0]
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

        for _ in range(image_copies):
            im.save("frame_%05d.png" % (self.frame,))
            self.frame += 1


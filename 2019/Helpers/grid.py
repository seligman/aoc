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
        self._ranges = {}

    @staticmethod
    def from_text(values):
        grid = Grid()
        y = 0
        for row in values:
            x = 0
            for cur in row:
                grid.set(cur, x, y)
                x += 1
            y += 1
        return grid

    @staticmethod
    def make_animation(frame_rate=30, file_format="gif", output_name="animation"):
        import os
        import subprocess

        if os.path.isfile(output_name + "." + file_format):
            os.unlink(output_name + "." + file_format)

        cmd = [
            "ffmpeg", 
            "-hide_banner",
            "-f", "image2",
            "-framerate", str(frame_rate), 
            "-i", "frame_%05d.png", 
            output_name + "." + file_format,
        ]
        print("$ " + " ".join(cmd))
        subprocess.check_call(cmd)

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

    def axis_range(self, axis):
        return range(self.axis_min(axis), self.axis_max(axis) + 1)

    def x_range(self):
        return self.axis_range(0)

    def y_range(self):
        return self.axis_range(1)

    def set(self, value, *coords):
        self._ranges = {}
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

    def draw_frames(self, color_map=DEFAULT_COLOR_MAP, cell_size=10, repeat_final=0, font_size=10, extra_callback=None):
        from datetime import datetime, timedelta

        msg = datetime.utcnow()
        print("Creating animation...")
        temp = self.grid

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
                extra_callback=extra_callback
            )

        print("Done with drawing")
        self.grid = temp

    def draw_grid(self, color_map=DEFAULT_COLOR_MAP, cell_size=10, extra_text=None, extra_text_rows=None, 
        font_size=14, image_copies=1, extra=None, extra_callback=None, text_xy=None, show_lines=True):
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
            width * (cell_size + 1) + 1 + (border * 2), 
            height * (cell_size + 1) + 1 + (border * 2) + for_text,
        ), color=BACKGROUND_COLOR)

        offset = height * (cell_size + 1) + 1 + (border * 2)

        d = ImageDraw.Draw(im, 'RGBA')

        d.rectangle(
            (
                (border, border), 
                (border + width * (cell_size + 1), border + height * (cell_size + 1))
            ), 
            LINE_COLOR, 
            LINE_COLOR,
        )

        for x in range(width):
            for y in range(height):
                color = self.grid.get((x + self.axis_min(0), y + self.axis_min(1)), self.default)
                text = None
                if isinstance(color, list):
                    temp = color_map[color[0]]
                    color = (
                        max(0, min(255, temp[0] + color[1])), 
                        max(0, min(255, temp[1] + color[1])), 
                        max(0, min(255, temp[2] + color[1])), 
                    )
                else:
                    if color in color_map:
                        color = color_map[color]
                    else:
                        text = color
                        color = (64, 64, 64)
                d.rectangle(
                    (
                        (border + x * (cell_size + 1) + 1, border + y * (cell_size + 1) + 1), 
                        (border + x * (cell_size + 1) + cell_size + (0 if show_lines else 1), border + y * (cell_size + 1) + cell_size + (0 if show_lines else 1))
                    ),
                    color, color
                )
                if text is not None:
                    w, h = d.textsize(text)
                    d.text((border + x * (cell_size + 1) + 1 + (cell_size - w) / 2, border + y * (cell_size + 1) + 1 + (cell_size - h) / 2), text, fill=(255, 255, 255))

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
                        border + extra['x'] * (cell_size + 1) + 1 + cell_size / 2, 
                        border + extra['y'] * (cell_size + 1) + 1 + cell_size / 2,
                    )
            extra_callback(d, extra)
        del d

        for _ in range(image_copies):
            im.save("frame_%05d.png" % (self.frame,))
            self.frame += 1


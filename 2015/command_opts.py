#!/usr/bin/env python3

import os
import sys
import inspect
import textwrap

VERSION = 5
_g_options = []


class OptMethod:
    def __init__(self, help):
        self.func = None
        self.func_names = []
        self.help = help
        self.args = []
        self.hidden = False
        self.other = None
        self.aka = None
        self.special = None
        self.module_name = ""

    def create_clones(self):
        if len(self.func_names) >= 1:
            ret = OptMethod(self.help)
            ret.func = self.func
            ret.args = self.args
            ret.hidden = self.hidden
            ret.other = self.func_names[0]
            ret.aka = self.func_names[1:]
            ret.special = self.special
            ret.module_name = self.module_name
            yield ret


def opt(*args, **kargs):
    global _g_options
    method = OptMethod(args[0])
    _g_options.append(method)

    if 'hidden' in kargs and kargs['hidden']:
        method.hidden = True

    if 'name' in kargs:
        method.func_names.append(kargs['name'])

    if 'names' in kargs:
        method.func_names.extend(kargs['names'])

    if 'sort' in kargs:
        method.special = kargs['sort']

    def real_opts(func):
        if len(method.func_names) == 0:
            method.func_names.append(func.__name__)

        method.module_name = func.__module__
        method.func = func
        method.args += inspect.getargspec(func)[0]

        if inspect.getargspec(func)[3] is not None:
            for i in range(len(inspect.getargspec(func)[3])):
                i = -(i + 1)
                method.args[i] = "(" + method.args[i] + ")"

        def wrapper(*args2, **kwargs):
            return func(*args2, **kwargs)
        return wrapper

    return real_opts


def main_entry(order_by='none', include_other=False, program_desc=None, default_action=None):
    global _g_options
    temp = sys.argv[1:]
    good = False

    if not include_other:
        _g_options = [x for x in _g_options if x.module_name == "__main__"]

    all_names = set()
    for arg in _g_options:
        for name_arg in arg.func_names:
            if name_arg in all_names:
                raise Exception("The name %s is used more than once!" % (name_arg,))
            else:
                all_names.add(name_arg)

    # Run through and crack each arg and run it in turn
    while temp:
        handled = False
        good = True
        for arg in _g_options:
            found = False
            for func_name in arg.func_names:
                if temp[0].replace("-", "_") == func_name:
                    params = len(arg.args)
                    while True:
                        if len(temp) - 1 >= params:
                            arg.func(*(temp[1:params + 1]))
                            temp = temp[params + 1:]
                            handled = True
                            break
                        else:
                            if arg.args[params-1].startswith("("):
                                params -= 1
                            else:
                                break
                    found = True
                    break
            if found:
                break

        if not handled:
            good = False
            break

    # Something wasn't right, so dump the help
    if not good:
        if default_action is not None:
            # Look for an explicit help request
            help_found = False
            for cur in sys.argv[1:]:
                if cur.lower() in {"-h", "/h", "--help", "-?", "/?"}:
                    help_found = True
                    break
            if not help_found:
                default_action()
                return

        options = []
        for cur in _g_options:
            for sub in cur.create_clones():
                options.append(sub)

        max_len = 0
        for arg in options:
            if not arg.hidden:
                optional = " ".join(arg.args)
                if len(arg.other) + len(optional) <= 25:
                    max_len = max(len(arg.other) + len(optional), max_len)

        dec_len = 70
        for arg in options:
            if not arg.hidden:
                optional = " ".join(arg.args)
                if len(arg.other) + len(optional) <= max_len:
                    dec_len = max(dec_len, len("%s %s%s = %s" % (
                        arg.other,
                        optional,
                        " " * (max_len - (len(arg.other) + len(optional))),
                        arg.help)))
                else:
                    dec_len = max(dec_len, len("%s %s%s" % (
                        arg.other,
                        optional,
                        " " * (max_len - (len(arg.other) + len(optional))))))
                    dec_len = max(dec_len, len("%s  = %s" % (
                        " " * max_len,
                        arg.help)))

        if program_desc is not None:
            program_desc = textwrap.dedent(program_desc)
            program_desc = program_desc.strip(" \r\n")
            program_desc = program_desc.replace("\r\n", "\n")
            program_desc = program_desc.split("\n")
            for cur in program_desc:
                dec_len = max(dec_len, len(cur))
            print("-" * dec_len)
            for cur in program_desc:
                print(cur)

        print("-" * dec_len)

        if order_by == 'func':
            options.sort(key=lambda x: x.other)
        elif order_by == 'desc':
            options.sort(key=lambda x: x.help)
        elif order_by == 'special':
            options.sort(key=lambda x: x.special)
        elif order_by == 'none':
            pass
        else:
            raise Exception("Sort expected to be one of 'func', 'desc', 'special', 'none'")

        for arg in options:
            if not arg.hidden:
                optional = " ".join(arg.args)
                if len(arg.other) + len(optional) <= max_len:
                    print("%s %s%s = %s" % (
                        arg.other,
                        optional,
                        " " * (max_len - (len(arg.other) + len(optional))),
                        arg.help))
                else:
                    print("%s %s%s" % (
                        arg.other,
                        optional,
                        " " * (max_len - (len(arg.other) + len(optional)))))
                    print("%s  = %s" % (
                        " " * max_len,
                        arg.help))
                if len(arg.aka) > 0:
                    print("%s Or: %s" % (" " * (max_len + 3), ", ".join(arg.aka)))

        print("-" * dec_len)
        sys.exit(1)


_need_enable = True
_simple_mode = False
def enable_ansi():
    global _need_enable
    global _simple_mode
    if _need_enable:
        _need_enable = False
        if os.name == "nt":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            if kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) == 0:
                _simple_mode = True


_getch = None
def getch():
    global _getch
    if _getch is None:
        if os.name == "nt":
            _getch = _getch_windows
        else:
            _getch = _getch_unix
    return _getch()


def _getch_unix():
    #pylint: disable=import-error
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def _getch_windows():
    import msvcrt
    return msvcrt.getch()


def getkey():
    def safe_getch():
        temp = getch()
        if not isinstance(temp, str):
            temp = "".join(map(chr, temp))
        return temp
    ret = safe_getch()
    if ret == "\x03":
        raise KeyboardInterrupt()
    elif ret == "\x08" or ret == "\x7f":
        return "back"
    elif ret == "\x0d":
        ret = "enter"
    elif ret == "\xe0":
        ret = safe_getch()
        ret = {
            "\x48": "up",
            "\x50": "down",
            "\x4b": "left",
            "\x4d": "right",
        }.get(ret, ret)
    elif ret == "\x1b":
        ret = safe_getch()
        if ret == "\x5b" or ret == "\x4f":
            ret = safe_getch()
            ret = {
                "\x41": "up",
                "\x42": "down",
                "\x44": "left",
                "\x43": "right",
            }.get(ret, ret)

    return ret


def _show_item(options, menu_item, hide_colors=False):
    sel_color = ""
    sel_unset = " " * (options["max_len"] - len(menu_item["desc"]))
    chevron = False

    if menu_item["index"] is None:
        index = ""
    else:
        index = str(menu_item["index"]) + "]"
        if menu_item["index"] == options["entry"]:
            chevron = True
            if not hide_colors:
                sel_color = "\033[7m"
                sel_unset += "\033[0m"

    sys.stdout.write(" %3s%s%s%s%s%s" % (
        index, 
        sel_color, 
        ">" if chevron else " ",
        menu_item["desc"], 
        "<" if chevron else " ",
        sel_unset, 
    ))
    

def _update_picker(options, hide_colors=False):
    global _simple_mode
    if _simple_mode:
        return

    last_entry_item, entry_item = None, None
    for menu_item in options["options"]:
        if menu_item["index"] == options["last_entry"]:
            last_entry_item = menu_item
        if menu_item["index"] == options["entry"]:
            entry_item = menu_item

    if last_entry_item != entry_item or hide_colors:
        for menu_item in [last_entry_item, entry_item]:
            if menu_item is not None:
                sys.stdout.write("\033" + ("[s" if os.name != "posix" else "7") + "\r\033[%dA" % (options["rows"] - menu_item["row"],))
                if menu_item["col"] > 0:
                    sys.stdout.write("\033[%dC" % (menu_item["col"] * (options["max_len"] + 6)))
                _show_item(options, menu_item, hide_colors=hide_colors)
                sys.stdout.write("\033" + ("[u" if os.name != "posix" else "8"))
            
    sys.stdout.flush()


def _make_options(options, cols, rotate):
    row, col = 0, 0
    ret = {
        "items": [],
        "options": [],
        "max_len": 10,
        "rows": 1,
        "cols": 1,
    }

    if rotate:
        opts = len(options)
        if opts % cols == 0:
            rows = opts / cols
        else:
            rows = (opts - (opts % cols)) / cols + 1

    for cur in options:
        item = {
                "index": None,
                "row": row,
                "col": col,
                "desc": cur[0],
                "command": None,
            }
        ret["max_len"] = max(ret["max_len"], len(item["desc"]))
        ret["items"].append(item)

        if len(cur) == 2:
            ret["options"].append(item)
            item["command"] = cur[1]
            item["index"] = str(len(ret["options"]))

        ret["rows"] = max(ret["rows"], row + 1)
        ret["cols"] = max(ret["cols"], col + 1)

        if rotate:
            row += 1
            if row >= rows:
                row = 0
                col += 1
        else:
            col += 1
            if col >= cols:
                col = 0
                row += 1

    for cur in ret["items"]:
        if cur["desc"] == "-":
            cur["desc"] = "-" * ret["max_len"]

    return ret


def show_menu(options, force_valid=False, cols=1, rotate=False):
    options = _make_options(options, cols, rotate)
    options["header"] = "Select option: "
    options["entry"] = ""

    enable_ansi()

    by_grid = {}
    by_grid_all = {}
    by_index = {}
    for cur in options["items"]:
        by_grid_all[(cur["row"], cur["col"])] = cur
        if cur["index"] is not None:
            by_grid[(cur["row"], cur["col"])] = cur
            by_index[cur["index"]] = cur

    for row in range(options["rows"]):
        for col in range(options["cols"]):
            if (row, col) in by_grid_all:
                _show_item(options, by_grid_all[(row, col)])
        sys.stdout.write("\n")

    sys.stdout.write(options["header"] + options["entry"])
    sys.stdout.flush()

    while True:
        key = getkey()
        if len(key) > 1 or key in {"w", "s", "a", "d"}:
            if key in {"up", "down", "left", "right", "w", "s", "a", "d"}:
                if key in {"up", "w"}:
                    dir_row, dir_col = -1, 0
                elif key in {"down", "s"}:
                    dir_row, dir_col = 1, 0
                elif key in {"left", "a"}:
                    dir_row, dir_col = 0, -1
                elif key in {"right", "d"}:
                    dir_row, dir_col = 0, 1

                options["last_entry"] = options["entry"]
                try:
                    if options["entry"] not in by_index:
                        row = max((-dir_row) * (options["rows"] - 1), 0)
                        col = max((-dir_col) * (options["cols"] - 1), 0)

                        while True:
                            if (row, col) in by_grid:
                                options["entry"] = by_grid[(row, col)]["index"]
                                break
                            row += dir_row
                            col += dir_col
                            if row < 0 or col < 0 or col >= options["cols"] or row >= options["rows"]:
                                options["entry"] = "1"
                                break
                    else:
                        row, col = by_index[options["entry"]]["row"], by_index[options["entry"]]["col"]
                        while True:
                            row += dir_row
                            col += dir_col
                            if row < 0 or col < 0 or col >= options["cols"] or row >= options["rows"]:
                                break
                            if (row, col) in by_grid:
                                options["entry"] = by_grid[(row, col)]["index"]
                                break
                except:
                    options["entry"] = "1"
                pad = max(0, len(options["last_entry"]) - len(options["entry"]))
                sys.stdout.write("\b" * len(options["last_entry"]) + options["entry"] + " " * pad + "\b" * pad)
                _update_picker(options)
            elif key == "back":
                if len(options["entry"]) > 0:
                    options["last_entry"] = options["entry"]
                    options["entry"] = options["entry"][:-1]
                    sys.stdout.write("\b \b")
                    _update_picker(options)
            elif key == "enter":
                options["last_entry"] = options["entry"]

                finish = True
                if force_valid:
                    finish = False
                    if options["entry"] in by_index:
                        finish = True

                if finish:
                    _update_picker(options, hide_colors=True)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
        else:
            options["last_entry"] = options["entry"]
            options["entry"] += key
            sys.stdout.write(key)
            _update_picker(options)

    if options["entry"] in by_index:
        return by_index[options["entry"]]["command"]
    else:
        return None


if __name__ == "__main__":
    print(textwrap.dedent("""
        # --------------------------------------------------------------------------
        # This module is not meant to be run directly.  To use it, add code like
        # this to a script to have this module parse the command line directly
        # and call the function the user wants to invoke:
        # --------------------------------------------------------------------------
        
        #!/usr/bin/env python3

        from command_opts import opt, main_entry

        @opt("Example function!")
        def example():
            print("You passed 'example' on the command line!")

        if __name__ == "__main__":
            main_entry('func')
        
        # --------------------------------------------------------------------------
    """))
    sys.exit(1)

#!/usr/bin/env python

from command_opts import opt, main_entry
import utils
import os
import subprocess
import requests
import re
import textwrap
import time
import sys
import codecs
from advent_year import YEAR_NUMBER

ALT_DATA_FILE = None
SOURCE_CONTROL = "p4"


class Logger:
    def __init__(self):
        self.rows = []

    def show(self, value):
        global _print_catcher
        if _print_catcher is not None:
            _print_catcher.safe = True
        try:
            if isinstance(value, unicode):
                value = value.replace(u"\r\n", u"\n")
                for cur in value.split(u"\n"):
                    cur += u"\n"
                    self.rows.append(cur.encode("utf-8"))
                    sys.stdout.write(cur)
                sys.stdout.flush()
            else:
                value = str(value)
                value = value.replace("\r\n", "\n")
                for cur in value.split("\n"):
                    cur += "\n"
                    self.rows.append(cur)
                    sys.stdout.write(cur)
                sys.stdout.flush()
        except:
            value = str(value)
            value = value.replace("\r\n", "\n")
            for cur in value.split("\n"):
                cur += "\n"
                self.rows.append(cur)
                sys.stdout.write(cur)
            sys.stdout.flush()
        if _print_catcher is not None:
            _print_catcher.safe = False

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for cur in self.rows:
                f.write(cur)

    def compare_to_file(self, filename):
        if len(self.rows) == 0:
            return False
        i = 0
        with open(filename) as f:
            for cur in f:
                if i >= len(self.rows):
                    return False
                if self.rows[i] != cur:
                    return False
                i += 1
        if i != len(self.rows):
            return False
        return True

    def decode_values(self, values):
        ret = []
        for cur in values.split("\n"):
            cur = cur.strip()
            if len(cur) > 0:
                ret.append(cur)
        return ret


def edit_file(filename):
    if SOURCE_CONTROL is not None:
        if SOURCE_CONTROL == "p4":
            cmd = ["p4", "edit", filename]
            print("$ " + " ".join(cmd))
            subprocess.check_call(cmd)
        elif SOURCE_CONTROL == "git":
            pass
        else:
            raise Exception()


def add_file(filename):
    if SOURCE_CONTROL is not None:
        if SOURCE_CONTROL == "p4":
            cmd = ["p4", "add", filename]
            print("$ " + " ".join(cmd))
            subprocess.check_call(cmd)
        elif SOURCE_CONTROL == "git":
            pass
        else:
            raise Exception()


def revert_file(filename):
    if SOURCE_CONTROL is not None:
        if SOURCE_CONTROL == "p4":
            cmd = ["p4", "revert", filename]
            print("$ " + " ".join(cmd))
            subprocess.check_call(cmd)
        elif SOURCE_CONTROL == "git":
            pass
        else:
            raise Exception()

@opt("Update all advent.py files")
def update_selfs():
    with open("advent.py", "rb") as f:
        source_data = f.read()

    for year in os.listdir(".."):
        year = os.path.join("..", year)
        if os.path.isdir(year):
            dest = os.path.join(year, "advent.py")
            with open(dest, "rb") as f:
                dest_data = f.read()
            if dest_data == source_data:
                print("%s is already up to date" % (dest,))
            else:
                print("Updating %s..." % (dest,))
                edit_file(dest)
                with open(dest, "wb") as f:
                    f.write(source_data)


@opt("Use alt data file")
def alt(file_number):
    global ALT_DATA_FILE
    ALT_DATA_FILE = int(file_number)


def get_input_file(helper, file_type="input"):
    global ALT_DATA_FILE
    if ALT_DATA_FILE is None or ALT_DATA_FILE == 0:
        fn = "day_%02d_%s.txt" % (helper.get_desc()[0], file_type)
    else:
        fn = "day_%02d_%s_alt_%02d.txt" % (helper.get_desc()[0], file_type, ALT_DATA_FILE)
    return os.path.join("Puzzles", fn)


@opt("Launch website")
def launch():
    urls = [
        "https://adventofcode.com/" + YEAR_NUMBER,
        "https://www.reddit.com/r/adventofcode/",
        "https://topaz.github.io/paste/",
        "https://imgur.com/upload",
    ]

    for url in urls:
        if os.name == 'nt':
            cmd = "cmd /c start %s" % (url,)
        else:
            cmd = "open %s" % (url,)
        subprocess.check_call(cmd.split(' '))


@opt("Show other commands for a day")
def show_others(helper_day):
    sys.path.insert(0, 'Helpers')
    for helper in get_helpers_id(helper_day):
        print("## %s" % (helper.get_desc()[1]))
        found = False
        for cur in dir(helper):
            if cur.startswith("other_"):
                print("%s - %s" % (cur[6:], getattr(helper, cur)(True, None)))
                found = True
        if not found:
            print("(No other commands found)")


@opt("Run other command for a day")
def run_other(helper_day, command):
    sys.path.insert(0, 'Helpers')
    for helper in get_helpers_id(helper_day):
        found = False
        for cur in dir(helper):
            if cur == "other_" + command.lower():
                with open(get_input_file(helper)) as f:
                    values = []
                    for sub in f:
                        values.append(sub.strip("\r\n"))
                getattr(helper, cur)(False, values)
                found = True
        if not found:
            print("## %s" % (helper.get_desc()[1]))
            print("ERROR: Unable to find '%s'" % (command,))


@opt("Make new day (Offline)")
def make_day_offline():
    make_day_helper(False)


@opt("Make new day")
def make_day():
    make_day_helper(False)


def make_day_helper(offline):
    if not os.path.isfile("cookie.txt"):
        print("ERROR: Need 'cookie.txt' with the session information!")
        raise Exception("Need cookie file!")

    for cur in os.listdir("Puzzles"):
        if "DO_NOT_CHECK_THIS_FILE_IN" in cur:
            raise Exception("You appear to be trying to rerun make_day before a day is done!")

    helper_day = 1
    while os.path.isfile(os.path.join("Helpers", "day_%02d.py" % (helper_day,))):
        helper_day += 1

    files = [
        os.path.join("Helpers", "day_%02d.py" % (helper_day,)),
        os.path.join("Puzzles", "day_%02d.html" % (helper_day,)),
        os.path.join("Puzzles", "day_%02d.html.DO_NOT_CHECK_THIS_FILE_IN" % (helper_day,)),
        os.path.join("Puzzles", "day_%02d_input.txt" % (helper_day,)),
    ]

    for filename in files:
        if os.path.isfile(filename):
            print("ERROR: '%s' already exists!" % (filename,))
            return

    todo = "TODO"
    for pass_number in range(2):
        if pass_number == 1:
            todo = dl_day(str(helper_day))

        with open(os.path.join("Helpers", "example.txt")) as f_src:
            with open(os.path.join("Helpers", "day_%02d.py" % (helper_day,)), "w") as f_dest:
                data = f_src.read()
                data = data.replace("DAY0_NUM", "%02d" % (helper_day,))
                data = data.replace("DAY_NUM", "%d" % (helper_day,))
                data = data.replace("DAY_TODO", codecs.escape_encode(todo.encode("utf8"))[0])
                f_dest.write(data)

    with open(os.path.join("Puzzles", "day_%02d.html.DO_NOT_CHECK_THIS_FILE_IN" % (helper_day,)), "w") as f:
        f.write("You need to rerun dl_day!")

    if not offline:
        for filename in files:
            add_file(filename)

        for filename in files:
            if "html" not in filename:
                cmd = ["code", filename]
                if os.name == 'nt':
                    cmd = ["cmd", "/c"] + cmd
                subprocess.check_call(cmd)

    print("Created day #%d" % (helper_day,))


@opt("Show days")
def show_days():
    for helper in utils.get_helpers():
        print(helper.get_desc()[1])


def get_helpers_id(helper_day):
    helper_day = helper_day.lower()
    if helper_day == "all":
        for helper in utils.get_helpers():
            yield helper
    elif helper_day in {"last", "latest", "cur", "now"}:
        last = None
        for helper in utils.get_helpers():
            last = helper
        yield last
    else:
        helper_day = int(helper_day)
        for helper in utils.get_helpers():
            if helper_day == helper.get_desc()[0]:
                yield helper


@opt("Test helper")
def test(helper_day):
    good = 0
    bad = 0

    sys.path.insert(0, 'Helpers')

    for helper in get_helpers_id(helper_day):
        print("## %s" % (helper.get_desc()[1]))
        if helper.test(Logger()):
            print("That worked!")
            good += 1
        else:
            print("FAILURE!")
            bad += 1

    if good + bad > 1:
        print("# " + "-" * 60)

    print("Done, %d worked, %d failed" % (good, bad))
    if bad != 0:
        print("THERE WERE PROBLEMS")


_print_catcher = None
class PrintCatcher:
    def __init__(self):
        self.safe = False
        self.old_stdout = sys.stdout
        self.raw_used = False
        sys.stdout = self

    def write(self, value):
        if not self.safe:
            self.raw_used = True
        self.old_stdout.write(value)

    def flush(self):
        self.old_stdout.flush()

    def undo(self):
        sys.stdout = self.old_stdout
        return None


@opt("Run helper")
def run(helper_day):
    global _print_catcher
    _print_catcher = PrintCatcher()
    run_helper(helper_day, False)
    if _print_catcher.raw_used:
        safe_print("WARNING: Raw 'print' used somewhere!")
    _print_catcher = _print_catcher.undo()


@opt("Run helper and save output as correct")
def run_save(helper_day):
    run_helper(helper_day, True)


def safe_print(value):
    global _print_catcher
    if _print_catcher is not None:
        _print_catcher.safe = True
    print(value)
    if _print_catcher is not None:
        _print_catcher.safe = False


def run_helper(helper_day, save):
    sys.path.insert(0, 'Helpers')

    passed = 0
    failed = []

    for helper in get_helpers_id(helper_day):
        safe_print("## %s" % (helper.get_desc()[1]))
        with open(get_input_file(helper)) as f:
            values = []
            for cur in f:
                values.append(cur.strip("\r\n"))
        log = Logger()
        helper.run(log, values)
        filename = get_input_file(helper, file_type="expect")
        if save:
            if os.path.isfile(filename):
                edit_file(filename)
                log.save_to_file(filename)
            else:
                log.save_to_file(filename)
                add_file(filename)
        else:
            if os.path.isfile(filename):
                if log.compare_to_file(filename):
                    safe_print("# Got expected output!")
                    passed += 1
                else:
                    safe_print("# ERROR: Expected output doesn't match!")
                    failed.append("## %s FAILED!" % (helper.get_desc()[1]))
            else:
                safe_print("# No expected output to check")

    if passed + len(failed) > 1:
        safe_print("# " + "-" * 60)
        safe_print("Passed: %d" % (passed,))
        if len(failed) > 0:
            safe_print("ERROR: Failed: %d" % (len(failed),))
            for cur in failed:
                safe_print(cur)


@opt("Make a stand alone version of the day")
def make_demo(helper_day):
    sys.path.insert(0, 'Helpers')

    blanks = 0
    for helper in get_helpers_id(helper_day):
        filename = os.path.join("Helpers", "day_%02d.py" % (helper.get_desc()[0],))
        with open(filename) as f:
            for cur in f:
                cur = cur.strip("\r\n")
                print(cur)
                if cur.strip() == "":
                    blanks += 1
                else:
                    blanks = 0

        while blanks < 2:
            print("")
            blanks += 1

        print('# These are the simple versions of a more complex harness')
        print('')
        print('class Logger:')
        print('    def __init__(self):')
        print('        pass')
        print('')
        print('    def show(self, value):')
        print('        print(value)')
        print('')
        print('')
        print('def main():')
        print('    import os')
        print('    import sys')
        print('    if (sys.version_info.major, sys.version_info.minor) != (2, 7):')
        print('        print("WARNING: I expect to run on Python 2.7, no clue what\'s about to happen!")')
        print('    filename = "day_%02d_input.txt" % (get_desc()[0],)')
        print('    if not os.path.isfile(filename):')
        print('        print("ERROR: Need \'%s\' puzzle input to continue" % (filename,))')
        print('        return')
        print('    with open(filename) as f:')
        print('        values = []')
        print('        for line in f:')
        print('            values.append(line.strip("\\r\\n"))')
        print('    print("## Running \'%s\'..." % (get_desc()[1],))')
        print('    run(Logger(), values)')
        print('    print("All done!")')
        print('')
        print('')
        print('if __name__ == "__main__":')
        print('    main()')
        print('')


def get_header_footer():
    header = textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en-us">
        <head>
        <meta charset="utf-8"/>
        <title>Advent of Code """ + YEAR_NUMBER + """</title>
        <!--[if lt IE 9]><script src="html5.js"></script><![endif]-->
        <link href='SourceCodePro.css' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <link rel="stylesheet alternate" type="text/css" href="highcontrast.css?0" title="High Contrast"/>
        <link rel="shortcut icon" href="favicon.png"/>
        </head><body>
        <main>
    """).strip()

    footer = """</main></body></html>"""

    return header, footer


def get_page(url):
    if not os.path.isfile("cookie.txt"):
        print("ERROR: Need 'cookie.txt' with the session information!")
        raise Exception("Need cookie file!")

    with open("cookie.txt") as f:
        cookie = f.read().strip()

    resp = requests.get(url, headers={'Cookie': cookie})

    return resp.text


@opt("Download Index")
def get_index():
    resp = get_page("https://adventofcode.com/%s" % (YEAR_NUMBER,))

    resp = re.sub("[\x00-\xff]+<main>", "", resp)
    resp = re.sub("</main>[\x00-\xff]+", "", resp)

    for i in range(30, 0, -1):
        resp = resp.replace("/%s/day/%d" % (YEAR_NUMBER, i), "day_%02d.html" % (i,))

    header, footer = get_header_footer()

    edit_file(os.path.join("Puzzles", "index.html"))

    with open(os.path.join("Puzzles", "index.html"), "w") as f:
        f.write(header + resp.encode("utf8") + footer)

    print("Wrote out index")


@opt("Download Day")
def dl_day(helper_day):
    ret = ""
    already_downloaded = False

    for helper in get_helpers_id(helper_day):
        if already_downloaded:
            time.sleep(0.250)
        already_downloaded = True
        helper_day = helper.get_desc()[0]

        bad_file = os.path.join("Puzzles", "day_%02d.html.DO_NOT_CHECK_THIS_FILE_IN" % (helper_day,))
        if os.path.isfile(bad_file):
            os.unlink(bad_file)
            revert_file(bad_file)

        filename = os.path.join("Puzzles", "day_%02d_input.txt" % (helper_day,))
        if not os.path.isfile(filename):
            resp = get_page("https://adventofcode.com/%s/day/%d/input" % (YEAR_NUMBER, helper_day))

            with open(filename, "w") as f:
                f.write(resp)

            print("Wrote out puzzle input for day #%d" % (helper_day,))

        resp = get_page("https://adventofcode.com/%s/day/%d" % (YEAR_NUMBER, helper_day))

        resp = re.sub("[\x00-\xff]+<main>", "", resp)
        resp = re.sub("</main>[\x00-\xff]+", "", resp)
        resp = re.sub('<p>At this point, you should <a href="/[0-9]+">return to your advent calendar</a> and try another puzzle.</p>[\x00-\xff]+', "", resp, flags=re.MULTILINE)

        header, footer = get_header_footer()

        with open(os.path.join("Puzzles", "day_%02d.html" % (helper_day,)), "w") as f:
            f.write(header + resp + footer)

        print("Wrote out puzzle for day #%d" % (helper_day,))

        m = re.search("<h2>--- (.*?) ---</h2>", resp)
        if m:
            ret = m.group(1)
            ret = ret.replace("&gt;", ">")
            ret = ret.replace("&lt;", "<")
            ret = ret.replace("&amp;", "&")

    return ret


if __name__ == "__main__":
    main_entry('func')


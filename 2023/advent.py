#!/usr/bin/env python3

from advent_year import YEAR_NUMBER
from command_opts import opt, main_entry
from datetime import datetime, timedelta
import itertools, json, os, re, subprocess, sys, tempfile, textwrap, time, utils
if sys.version_info >= (3, 11): from datetime import UTC
else: import datetime as datetime_fix; UTC=datetime_fix.timezone.utc

ALT_DATA_FILE = None
SOURCE_CONTROL = "p4"
DESC = """
### The suggested dail routine looks like this:
advent.py launch        # This launches some useful links, and waits to make the next day
advent.py test cur      # This tests the current day, keep going till it works!
advent.py run cur       # This runs on the same day with the clue's data
### And finally, when everything's done, some clean up, and make a comment to post
advent.py finish_day    # This runs the following commands:
                        # run_save cur, dl_day cur, get_index, gen_comment
"""

class TestFailedException(Exception):
    pass

class Logger:
    def __init__(self):
        self.rows = []

    def __call__(self, value):
        self.show(value)

    def show(self, value, log_msg=True):
        global _print_catcher
        if _print_catcher is not None:
            _print_catcher.safe = True

        value = str(value)
        value = value.replace("\r\n", "\n")
        for cur in value.split("\n"):
            cur += "\n"
            if log_msg:
                self.rows.append(cur)
            sys.stdout.write(cur)
        sys.stdout.flush()

        if _print_catcher is not None:
            _print_catcher.safe = False

    def copy_result_to_clipboard(self):
        if len(self.rows) > 0:
            try:
                import clipboard
                clipboard.copy(self.rows[-1].strip())
                self.show("# '" + self.rows[-1].strip() + "' copied to clipboard", log_msg=False)
            except:
                self.show("# Unable to copy text to clipboard!", log_msg=False)

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for cur in self.rows:
                f.write(cur)

    def compare_to_file(self, filename):
        is_good = True
        with open(filename) as f:
            for i, (before, after) in enumerate(itertools.zip_longest(f, self.rows)):
                if before != after:
                    is_good = False
                    before = "(empty line)" if before is None else before.rstrip('\r\n')
                    after = "(empty line)" if after is None else after.rstrip('\r\n')
                    self.show(error_msg("ERROR") + f": Line {i+1}: Got '{after}', expected: '{before}'", log_msg=False)
        return is_good

    def decode_values(self, values):
        ret = values.replace("\t", "    ").split("\n")
        # Only remove empty lines at the start and end
        while len(ret) > 0 and len(ret[0].strip()) == 0:
            ret = ret[1:]
        while len(ret) > 0 and len(ret[-1].strip()) == 0:
            ret = ret[:-1]
        # Remove the common indent so extra spaces on the first line are left
        if len(ret) > 0:
            pad = min(len(x) - len(x.lstrip(' ')) for x in ret if len(x.strip()) > 0)
            if pad > 0:
                ret = [x[pad:] for x in ret]
        return ret

    def test(self, actual, expected):
        if str(actual) != str(expected):
            self.show(f"Test returned {actual}, " + error_msg(f"expected {expected}"))
            raise TestFailedException()
        else:
            self.show(f"Test returned {actual}, expected {expected}")

def error_msg(value):
    return "\x1b[97;101m" + value + "\x1b[m"

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

@opt("Update all advent.py files", group="Utilities")
def update_selfs():
    with open("advent.py", "rb") as f:
        source_data = f.read()

    for year in os.listdir(".."):
        if re.search("^[0-9]{4}$", year) is not None:
            year = os.path.join("..", year)
            if os.path.isdir(year):
                dest = os.path.join(year, "advent.py")
                with open(dest, "rb") as f:
                    dest_data = f.read()
                if dest_data == source_data:
                    print(f"{dest} is already up to date")
                else:
                    print(f"Updating {dest}...")
                    edit_file(dest)
                    with open(dest, "wb") as f:
                        f.write(source_data)

@opt("Finish off all items for a day", group="Advent of Code")
def finish_day():
    print("$ advent.py run_save cur")
    run_save("cur")
    print("$ advent.py dl_day cur")
    dl_day("cur")
    print("$ advent.py get_index")
    get_index()
    print("$ advent.py gen_comment")
    gen_comment()

@opt("Use alt data file", group="Session Management")
def alt(file_number:int):
    global ALT_DATA_FILE
    ALT_DATA_FILE = file_number

def get_input_file(helper, file_type="input"):
    global ALT_DATA_FILE
    if ALT_DATA_FILE is None or ALT_DATA_FILE == 0:
        fn = f"day_{helper.DAY_NUM:02d}_{file_type}.txt"
    else:
        fn = f"day_{helper.DAY_NUM:02d}_{file_type}_alt_{ALT_DATA_FILE:02d}.txt"
    return os.path.join("Puzzles", fn)

@opt("Generate a comment based off scores", group="Advent of Code")
def gen_comment(for_sharing=False):
    max_day = 0
    for helper in utils.get_helpers():
        max_day = max(helper.DAY_NUM, max_day)
    
    scores_url = "https://adventofcode.com/" + YEAR_NUMBER + "/leaderboard/self"
    score_re = re.compile(r"^ *(?P<day>\d+) +\d+:\d+:\d+ +(?P<score1>\d+) +\d+ +\d+:\d+:\d+ +(?P<score2>\d+) +\d+ *$")
    scores = get_page(scores_url)

    found = False
    day, score1, score2 = -1, -1, -1

    for cur in scores.split("\n"):
        m = score_re.search(cur)
        if m is not None:
            day, score1, score2 = int(m.group("day")), int(m.group("score1")), int(m.group("score2"))
            if day == max_day:
                found = True
                break
    
    if not found:
        print("Warning: Couldn't find day!")
        print("")
    
    if for_sharing:
        msg = f"Advent of Code, day {max_day}: {score1} / {score2}\n"
    else:
        msg = f"[LANGUAGE: Python] {score1} / {score2}\n"
        msg += "\n"
        msg += f"[github](https://github.com/seligman/aoc/blob/master/{YEAR_NUMBER}/Helpers/day_{max_day:02}.py)\n"

    print("-" * 70)
    print(msg.rstrip("\n"))
    print("-" * 70)

    try:
        import clipboard
        clipboard.copy(msg)
        print("# Copied to clipboard")
    except:
        print("# Unable to copy to clipboard")

@opt("Launch website", group="Advent of Code")
def launch():
    import webbrowser
    urls = [
        "https://www.reddit.com/r/adventofcode/",
        "https://adventofcode.com/" + YEAR_NUMBER,
    ]

    for url in urls:
        print("Launch: " + url)
        webbrowser.open(url, 2)

    if os.environ.get("TERM_PROGRAM", "") == "vscode":
        print("Already running inside of VS Code")
    else:
        print("Launching VS Code")
        subprocess.check_call("code .", shell=True)

    make_day_wait()

@opt("Show other commands for a day", group="Utilities")
def show_others(helper_day):
    sys.path.insert(0, 'Helpers')
    for helper in get_helpers_id(helper_day):
        print(f"## {helper.DAY_DESC}")
        found = False
        for cur in dir(helper):
            if cur.startswith("other_"):
                print(f"{cur[6:]} - {getattr(helper, cur)(True, None)}")
                found = True
        if not found:
            print("(No other commands found)")

@opt("Run other command for a day", group="Utilities")
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
            print(f"## {helper.DAY_DESC}")
            print(f"ERROR: Unable to find '{command}'")

@opt("Make new day (Offline)", group="Utilities")
def make_day_offline(target_day="cur"):
    make_day_helper(True, force_day=target_day)

@opt("Make new day", group="Utilities")
def make_day(target_day="cur"):
    make_day_helper(False, force_day=target_day)

@opt("Make new day, after sleeping till midnight", group="Utilities")
def make_day_wait(target_day="cur"):
    import sleeper
    import random
    resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}")
    m = re.search(r"var server_eta *= *(?P<eta>\d+);", resp)
    eta = int(m.group("eta")) + random.randint(5, 10)
    if sleeper.sleep(str(eta), exit_at_end=False):
        make_day_helper(False, force_day=target_day)

@opt("Load cookie from browser to cache", group="Session Management")
def save_cookie(browser="Chrome", alt_id=""):
    try:
        import browser_cookie3 # type: ignore
    except:
        raise Exception("Unable to load 'browser_cookie3', please try running in a venv with requirements.txt")

    browser = browser.lower().strip().replace(" ", "")
    if alt_id == "":
        alt_id = -1
    else:
        global ALT_DATA_FILE
        alt_id = int(alt_id)
        ALT_DATA_FILE = alt_id

    browsers = {
        "chrome": browser_cookie3.chrome,
        "chromium": browser_cookie3.chromium,
        "opera": browser_cookie3.opera,
        "edge": browser_cookie3.edge,
        "firefox": browser_cookie3.firefox,
    }
    if browser not in browsers:
        print(f"Unknown choice of browser: {browser}, please use one of:")
        for x in browsers:
            print(f"  {x}")
        exit(1)
    fn = os.path.expanduser(os.path.join("~", ".aoc_cookies.json"))
    if os.path.isfile(fn):
        with open(fn) as f:
            data = json.load(f)
    else:
        data = {}

    cookie = browsers[browser](domain_name='adventofcode.com')
    cookie = ';'.join(f'{x.name}={x.value}' for x in cookie)
    data[str(alt_id)] = cookie
    data["_last_updated"] = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    with open(fn, "w") as f:
        data = json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")

    resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}")
    with open("main_page.html", "wt") as f:
        f.write(resp)

    print("Make sure to validate that main_page.html looks good, look for the")
    print("username in the source code and delete the file after validating it")
    print("")

    print("Done")

def get_cookie():
    fn = os.path.expanduser(os.path.join("~", ".aoc_cookies.json"))
    if os.path.isfile(fn):
        if (datetime.now(UTC).replace(tzinfo=None) - datetime.fromtimestamp(os.path.getmtime(fn))) > timedelta(days=60):
            print("Warning, cookie is very old, removing it")
            os.unlink(fn)

    if not os.path.isfile(fn):
        save_cookie(alt_id="-1" if (ALT_DATA_FILE is None or ALT_DATA_FILE == 0) else ALT_DATA_FILE)

    with open(fn) as f:
        data = json.load(f)
        return data[str(-1 if (ALT_DATA_FILE is None or ALT_DATA_FILE == 0) else ALT_DATA_FILE)]

def make_day_helper(offline, force_day=None):
    if not offline:
        get_cookie()

    for cur in os.listdir("Puzzles"):
        if "DO_NOT_CHECK_THIS_FILE_IN" in cur:
            raise Exception("You appear to be trying to rerun make_day before a day is done!")

    if force_day is None or force_day.lower() == "cur":
        helper_day = 1
        while os.path.isfile(os.path.join("Helpers", f"day_{helper_day:02d}.py")):
            helper_day += 1
    else:
        helper_day = int(force_day)

    files = [
        os.path.join("Puzzles", f"day_{helper_day:02d}_input.txt"),
        os.path.join("Helpers", f"day_{helper_day:02d}.py"),
        os.path.join("Puzzles", f"day_{helper_day:02d}.html"),
        os.path.join("Puzzles", f"day_{helper_day:02d}.html.DO_NOT_CHECK_THIS_FILE_IN"),
    ]

    for filename in files:
        if os.path.isfile(filename):
            print(f"ERROR: '{filename}' already exists!")
            return

    todo = "TODO"
    for pass_number in range(2):
        if pass_number == 1:
            todo = dl_day(str(helper_day))

        with open(os.path.join("Helpers", "example.txt")) as f_src:
            with open(os.path.join("Helpers", f"day_{helper_day:02d}.py"), "w") as f_dest:
                data = f_src.read()
                data = data.replace("NEED_DAY0_NUM", f"{helper_day:02d}")
                data = data.replace("NEED_DAY_NUM", str(helper_day))
                data = data.replace("NEED_DAY_DESC", todo)
                f_dest.write(data)

    with open(os.path.join("Puzzles", f"day_{helper_day:02d}.html.DO_NOT_CHECK_THIS_FILE_IN"), "w") as f:
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

    print(f"Created day #{helper_day}")

@opt("Show days", group="Utilities")
def show_days():
    for helper in utils.get_helpers():
        print(helper.DAY_DESC)

def get_helpers_id(helper_day):
    helper_day = helper_day.lower()
    if helper_day == "all":
        for helper in utils.get_helpers():
            yield helper
    else:
        valid = set()
        def parse_value(value):
            if value.lower() in {"last", "latest", "cur", "now"}:
                last = None
                for helper in utils.get_helpers():
                    last = helper.DAY_NUM
                return last
            else:
                return int(value)

        for part in helper_day.split(","):
            if "-" in part:
                part = part.split("-")
                for x in range(parse_value(part[0]), parse_value(part[1]) + 1):
                    valid.add(x)
            else:
                valid.add(parse_value(part))

        for helper in utils.get_helpers():
            if helper.DAY_NUM in valid:
                yield helper

@opt("Test helper", group="Advent of Code")
def test(helper_day):
    good, bad = 0, 0

    sys.path.insert(0, 'Helpers')

    for helper in get_helpers_id(helper_day):
        print(f"## {helper.DAY_DESC}")

        try:
            helper.test(Logger())
            print("That worked!")
            good += 1
        except TestFailedException:
            bad += 1
            print(error_msg("  FAILURE!  "))
        except SystemExit as e:
            print(error_msg(f"  exit({e}) called!  "))
            raise
        except:
            import traceback
            traceback.print_exc()
            exit(1)

    if good + bad > 1:
        print("# " + "-" * 60)

    print(f"Done, {good} worked, {bad} failed")
    if bad != 0:
        print(error_msg("  THERE WERE PROBLEMS  "))

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

@opt("Run and time duration", group="Advent of Code")
def run_time(helper_day):
    start = datetime.now(UTC).replace(tzinfo=None)
    run(helper_day)
    end = datetime.now(UTC).replace(tzinfo=None)
    secs = (end - start).total_seconds()
    if secs >= 90:
        pretty = f"{secs / 60:0.2f} minutes.  That's a long time!"
    elif secs >= 15:
        pretty = f"{secs:0.2f} seconds.  That's a long time!"
    elif secs >= 10:
        pretty = f"{secs:0.2f} seconds."
    elif secs >= 0.01:
        pretty = f"{int(secs * 1000):d} milliseconds."
    else:
        pretty = f"no time."
    safe_print(f"Done, that took {pretty}")

@opt("Run helper", group="Advent of Code")
def run(helper_day):
    global _print_catcher
    _print_catcher = PrintCatcher()
    run_helper(helper_day, False)
    if _print_catcher.raw_used:
        safe_print("WARNING: Raw 'print' used somewhere!")
    _print_catcher = _print_catcher.undo() # pylint: disable=assignment-from-none

@opt("Run helper and save output as correct", group="Advent of Code")
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

    if helper_day == "cur" and not save:
        copy_result = True
    else:
        copy_result = False

    passed = 0
    failed = []
    summary = []
    cached_runs = {"year": YEAR_NUMBER}
    if os.path.isfile(os.path.join(tempfile.gettempdir(), "aoc_run_cache.json")):
        try:
            with open(os.path.join(tempfile.gettempdir(), "aoc_run_cache.json")) as f:
                cached_runs = json.load(f)
            if cached_runs["year"] != YEAR_NUMBER:
                cached_runs = {"year": YEAR_NUMBER}
        except:
            cached_runs = {"year": YEAR_NUMBER}
    cached_runs['changed'] = False

    max_len = 0
    for helper in get_helpers_id(helper_day):
        max_len = max(max_len, len(helper.DAY_DESC))

    for helper in get_helpers_id(helper_day):
        safe_print(f"## {helper.DAY_DESC}")
        with open(get_input_file(helper)) as f:
            values = []
            for cur in f:
                values.append(cur.strip("\r\n"))
        log = Logger()
        start = datetime.now(UTC).replace(tzinfo=None)
        real_run = True
        if save and cached_runs.get(str(helper.DAY_NUM), {}).get("hash", "--") == helper.hash:
            log.rows = cached_runs[str(helper.DAY_NUM)]["rows"]
            for row in log.rows:
                print(row.rstrip("\r\n"))
            real_run = False
        else:
            helper.run(log, values)
            cached_runs[str(helper.DAY_NUM)] = {"hash": helper.hash, "rows": log.rows}
            cached_runs["changed"] = True
        finish = datetime.now(UTC).replace(tzinfo=None)
        secs = (finish - start).total_seconds()
        if real_run:
            if secs >= 90:
                pretty = f"{secs / 60:0.2f} minutes to complete.  That's a long time!"
            elif secs >= 15:
                pretty = f"{secs:0.2f} seconds to complete.  That's a long time!"
            elif secs >= 10:
                pretty = f"{secs:0.2f} seconds to complete."
            elif secs >= 0.01:
                pretty = f"{int(secs * 1000):d} milliseconds to complete."
            else:
                pretty = f"no time to complete."
            safe_print(f"# That took {pretty}")

        filename = get_input_file(helper, file_type="expect")

        if copy_result:
            log.copy_result_to_clipboard()

        if save:
            info = "Saved output."
            if os.path.isfile(filename):
                edit_file(filename)
                log.save_to_file(filename)
            else:
                log.save_to_file(filename)
                add_file(filename)
        else:
            if os.path.isfile(filename):
                if log.compare_to_file(filename):
                    info = "Good"
                    safe_print("# Got expected output!")
                    passed += 1
                else:
                    info = error_msg("ERROR")
                    safe_print("# " + error_msg("  ERROR: Expected output doesn't match!  "))
                    failed.append(f"## {helper.DAY_DESC} FAILED!")
            else:
                info = "Unknown"
                safe_print("# No expected output to check")
        temp = helper.DAY_DESC + ":" + " " * (max_len - len(helper.DAY_DESC))
        summary.append(f"{temp} {int(secs * 1000):6d}ms {error_msg('!') if secs > 15 else ' '} {info}")

    if cached_runs["changed"]:
        with open(os.path.join(tempfile.gettempdir(), "aoc_run_cache.json"), "wt") as f:
            json.dump(cached_runs, f, indent=2, sort_keys=True)
            f.write("\n")

    if passed + len(failed) > 1:
        safe_print("# " + "-" * 75)
        for cur in summary:
            safe_print(cur)
        safe_print("# " + "-" * 75)
        safe_print(f"Passed: {passed}")
        if len(failed) > 0:
            safe_print(f"# " + error_msg(f"  ERROR: Failed: {len(failed)}  "))
            for cur in failed:
                safe_print(cur)

@opt("Make a stand alone version of the day", group="Utilities")
def make_demo(helper_day):
    sys.path.insert(0, 'Helpers')

    blanks = 0
    for helper in get_helpers_id(helper_day):
        filename = os.path.join("Helpers", f"day_{helper.DAY_NUM:02d}.py")
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
        print('    filename = f"day_{DAY_NUM:02d}_input.txt"')
        print('    if not os.path.isfile(filename):')
        print('        print(f"ERROR: Need \'{filename}\' puzzle input to continue")')
        print('        return')
        print('    with open(filename) as f:')
        print('        values = []')
        print('        for line in f:')
        print('            values.append(line.strip("\\r\\n"))')
        print('    print(f"## Running \'{DAY_DESC}\'...")')
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
    import urllib.request
    cookie = get_cookie()

    req = urllib.request.Request(
        url, 
        headers={
            'Cookie': cookie,
            'User-Agent': 'github.com/seligman/aoc by scott.seligman@gmail.com',
        },
    )
    resp = urllib.request.urlopen(req)
    resp = resp.read().decode("utf-8")
    resp = resp.encode('ascii', 'xmlcharrefreplace')
    resp = resp.decode("utf-8")
    return resp

@opt("Download Index", group="Advent of Code")
def get_index():
    resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}")

    resp = re.sub("^.*<main>", "", resp, flags=re.DOTALL)
    resp = re.sub("</main>.*$", "", resp, flags=re.DOTALL)

    for i in range(30, 0, -1):
        resp = resp.replace(f"/{YEAR_NUMBER}/day/{i}", f"day_{i:02d}.html")

    header, footer = get_header_footer()

    edit_file(os.path.join("Puzzles", "index.html"))

    with open(os.path.join("Puzzles", "index.html"), "wt", encoding="utf-8") as f:
        f.write(header + resp + footer)

    print("Wrote out index")

@opt("Download Day", group="Advent of Code")
def dl_day(helper_day, input_only="no"):
    input_only = input_only.lower() in {"yes", "true", "y"}
    ret = ""
    already_downloaded = False

    for helper in get_helpers_id(helper_day):
        if already_downloaded:
            time.sleep(0.250)
        already_downloaded = True
        helper_day = helper.DAY_NUM

        if not input_only:
            bad_file = os.path.join("Puzzles", f"day_{helper_day:02d}.html.DO_NOT_CHECK_THIS_FILE_IN")
            if os.path.isfile(bad_file):
                os.unlink(bad_file)
                revert_file(bad_file)

        if ALT_DATA_FILE is None or ALT_DATA_FILE == 0:
            filename = os.path.join("Puzzles", f"day_{helper_day:02d}_input.txt")
        else:
            filename = os.path.join("Puzzles", f"day_{helper_day:02d}_input_alt_{ALT_DATA_FILE:02d}.txt")

        if not os.path.isfile(filename):
            resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}/day/{helper_day}/input")

            with open(filename, "wt", encoding="utf-8") as f:
                f.write(resp)

            print(f"Wrote out puzzle input for day #{helper_day}")

        if not input_only:
            resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}/day/{helper_day}")

            resp = re.sub("^.*<main>", "", resp, flags=re.DOTALL)
            resp = re.sub("</main>.*$", "", resp, flags=re.DOTALL)
            resp = re.sub('<p>At this point, you should <a href="/[0-9]+">return to your advent calendar</a> and try another puzzle.</p>.+', "", resp, flags=(re.MULTILINE | re.DOTALL))

            header, footer = get_header_footer()

            with open(os.path.join("Puzzles", f"day_{helper_day:02d}.html"), "wt", encoding="utf-8") as f:
                f.write(header + resp + footer)

            print(f"Wrote out puzzle for day #{helper_day}")

            m = re.search("<h2>--- (.*?) ---</h2>", resp)
            if m:
                ret = m.group(1)
                ret = ret.replace("&gt;", ">")
                ret = ret.replace("&lt;", "<")
                ret = ret.replace("&amp;", "&")

    return ret

@opt("Compare expected results with website", group="Advent of Code")
def compare_results(helper_day):
    already_downloaded = False

    for helper in get_helpers_id(helper_day):
        print(f"## {helper.DAY_DESC}")
        if already_downloaded:
            time.sleep(0.250)

        filename = get_input_file(helper, file_type="expect")
        data = []
        if os.path.isfile(filename):
            with open(filename) as f:
                for row in f:
                    row = row.strip()
                    if " " not in row:
                        data.append(row)

        resp = get_page(f"https://adventofcode.com/{YEAR_NUMBER}/day/{helper.DAY_NUM}")
        expecteds = []
        for m in re.finditer(f'Your puzzle answer was <code>(?P<answer>.*?)</code>', resp):
            expecteds.append(m.group("answer"))

        all_good = True
        for i, (current, expected) in enumerate(itertools.zip_longest(data, expecteds)):
            current = "(nothing)" if current is None else current.rstrip("\r\n")
            expected = "(nothing)" if expected is None else expected.rstrip("\r\n")
            if current != expected:
                print(error_msg("ERROR: ") + f"Have '{current}', but website reports '{expected}' for line {i+1}")
                all_good = False
        if all_good:
            print("(all results are good)")

if __name__ == "__main__":
    main_entry('func', program_desc=DESC)

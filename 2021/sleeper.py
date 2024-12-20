#!/usr/bin/env python3

from datetime import datetime, timedelta
import sys
import time
import re
import threading
import math
if sys.version_info >= (3, 11): from datetime import UTC
else: import datetime as datetime_fix; UTC=datetime_fix.timezone.utc

__version__ = 4

ENABLE_SERVER = False
def _make_server_call(**kargs):
    raise Exception()

def _input_thread(sentinel):
    try:
        input()
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
    sentinel.append(None)

def parse_duration(val):
    sleep_amount = None

    if sleep_amount is None:
        m = re.search("^[xX]:([0-9]{2})$", val)
        if m is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            future = datetime(
                now.year, now.month, now.day, 
                now.hour, int(m.groups()[0]), 0)
            while future <= now:
                future += timedelta(hours=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            future = datetime(
                now.year, now.month, now.day, 
                int(m.groups()[0]), int(m.groups()[1]), 0)
            while future <= now:
                future += timedelta(days=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2}):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            future = datetime(
                now.year, now.month, now.day, 
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]))
            while future <= now:
                future += timedelta(days=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2})$", val)
        if m is not None:
            now = datetime.now()
            future = datetime(
                now.year, now.month, now.day, 
                int(m.groups()[0]), int(m.groups()[1]), 0)
            while future <= now:
                future += timedelta(days=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2}):([0-9]{2})$", val)
        if m is not None:
            now = datetime.now()
            future = datetime(
                now.year, now.month, now.day, 
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]))
            while future <= now:
                future += timedelta(days=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]+):([0-9]{2})$", val)
        if m is not None:
            now = datetime.now()
            future = datetime(
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 
                int(m.groups()[3]), int(m.groups()[4]), 0)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]+):([0-9]{2}):([0-9]{2})$", val)
        if m is not None:
            now = datetime.now()
            future = datetime(
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 
                int(m.groups()[3]), int(m.groups()[4]), int(m.groups()[5]))
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]+):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            future = datetime(
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 
                int(m.groups()[3]), int(m.groups()[4]), 0)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]+):([0-9]{2}):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            future = datetime(
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 
                int(m.groups()[3]), int(m.groups()[4]), int(m.groups()[5]))
            sleep_amount = (future - now).total_seconds()

    for word, mul in (("sec", 1.0), ("min", 60.0), ("hour", 3600.0), ("day", 86400.0)):
        if sleep_amount is None:
            m = re.search("^([0-9]+(\\.[0-9]+|)) *" + word, val, re.IGNORECASE)
            if m is not None:
                sleep_amount = float(m.groups()[0]) * mul

    for word, mul in (("s", 1.0), ("m", 60.0), ("h", 3600.0), ("d", 86400.0)):
        if sleep_amount is None:
            m = re.search("^([0-9]+(\\.[0-9]+|)) *" + word, val, re.IGNORECASE)
            if m is not None:
                sleep_amount = float(m.groups()[0]) * mul

    if sleep_amount is None:
        m = re.search("^([0-9]+(\\.[0-9]+|))$", val, re.IGNORECASE)
        if m is not None:
            sleep_amount = float(m.groups()[0])

    return sleep_amount

def time_command(cmd):
    import subprocess
    start = datetime.now(UTC).replace(tzinfo=None)
    print(f" Started: {start.strftime('%Y-%m-%d %H:%M:%S')}.{start.microsecond // 1000:03d}")
    temp = " ".join(f'"{x}"' if ' ' in x else x for x in cmd)
    print(f" Running: '{temp}'")
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        print(f"  Command returned {ret}")
    stop = datetime.now(UTC).replace(tzinfo=None)
    print(f" Started: {start.strftime('%Y-%m-%d %H:%M:%S')}.{start.microsecond // 1000:03d}")
    _show_total(start, stop, "")
    return ret

def _show_total(start, stop, extra):
    print(f"{extra} Stopped: {stop.strftime('%Y-%m-%d %H:%M:%S')}.{stop.microsecond // 1000:03d}")
    dur = int((stop - start).total_seconds() * 1000)
    days = dur // 86400000
    hours = (dur // 3600000) % 24
    minutes = (dur // 60000) % 60
    seconds = (dur // 1000) % 60
    milliseconds = dur % 1000
    if days > 0:
        print(f"{extra}   Total: {days}day{'' if days == 1 else 's'}, {hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
    else:
        print(f"{extra}   Total: {hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
    print(f"{extra}          {dur // 1000}.{milliseconds:03d} seconds")

def run_timer():
    global _enter_waiter, _sentinel

    start = datetime.now(UTC).replace(tzinfo=None)
    last = start
    print(f"{start.strftime('%d %H:%M:%S')}:  Started: {start.strftime('%Y-%m-%d %H:%M:%S')}.{start.microsecond // 1000:03d}")

    if _enter_waiter is None:
        _enter_waiter = threading.Thread(target=_input_thread, args=(_sentinel,))
        _enter_waiter.daemon = True
        _enter_waiter.start()

    last_len = 0
    while True:
        if len(_sentinel) != 0:
            break

        dur = datetime.now(UTC).replace(tzinfo=None) - start

        if dur.total_seconds() > 90000:
            last_len = _temp_msg(f"Timer at {float(dur.total_seconds()) / 86400.0:.1f} days...", last_len)
            to_sleep = 8640
        elif dur.total_seconds() > 3900:
            last_len = _temp_msg(f"Timer at {float(dur.total_seconds()) / 3600.0:.1f} hours...", last_len)
            to_sleep = 360
        elif dur.total_seconds() > 90:
            last_len = _temp_msg(f"Timer at {float(dur.total_seconds()) / 60.0:.1f} minutes...", last_len)
            to_sleep = 6
        else:
            val = int(math.floor(dur.total_seconds()))
            to_sleep = 1
            if val == 1:
                last_len = _temp_msg(f"Timer at {val:d} second...", last_len)
            else:
                last_len = _temp_msg(f"Timer at {val:d} seconds...", last_len)

        last += timedelta(seconds=to_sleep)
        to_sleep = (last - datetime.now(UTC).replace(tzinfo=None)).total_seconds()
        stop_at = time.time() + to_sleep
        while time.time() <= stop_at and len(_sentinel) == 0:
            to_sleep = max(0.01, stop_at - time.time())
            time.sleep(min(to_sleep, 0.25))

    if len(_sentinel) > 0:
        _temp_msg("Enter detected", 0)
        temp_nl()
    else:
        _temp_msg(None, last_len)

    stop = datetime.now(UTC).replace(tzinfo=None)
    _show_total(start, stop, f"{stop.strftime('%d %H:%M:%S')}: ")
    _sentinel.clear()
    return 0

def main():
    sleep_amount = None
    keep_going = False
    val = sys.argv[1:]

    if ENABLE_SERVER and len(val) > 2 and (val[0], val[1]) in {("server", "run"), ("run", "server")}:
        _launch_server()
        time_command(val[2:])
        val = [str(_get_time(_server_id)[1])]
    elif ENABLE_SERVER and len(val) >= 2 and (val[0], val[1]) in {("server", "timer"), ("timer", "server")}:
        _launch_server()
        run_timer()
        val = [str(_get_time(_server_id)[1])]
    elif len(val) > 1 and val[0] == "run":
        exit(time_command(val[1:]))
    elif len(val) > 2 and val[0] in {"run_loop", "run-loop"}:
        cmd = val[2:]
        sleep_amount = parse_duration(val[1])
        while True:
            ret = time_command(cmd)
            if ret != 0:
                exit(ret)
            if not sleep(sleep_amount, exit_at_end=False):
                exit(1)
    elif len(val) >= 1 and val[0] == "timer":
        exit(run_timer())
    elif ENABLE_SERVER and len(val) > 1 and val[0] == "server":
        _launch_server()
        val = val[1:]
    elif ENABLE_SERVER and len(val) > 1 and val[0] == "client":
        keep_going, sleep_amount = _get_time(" ".join(val[1:]))
        val = []

    if sleep_amount is None:
        if len(val) > 0:
            sleep_amount = parse_duration(" ".join(val))

    if sleep_amount is None:
        import textwrap
        msg = textwrap.dedent("""
            Specify a sleep amount, can be one of the following options:
                #        - A specific number of seconds.
                #:##     - Till the next 24 hour clock value is hit, using local time
                #:##:##  - Till the next 24 hour clock value is hit, using local time
                x:##     - Till the next minute value is hit
                ####-##-## ##:##     - Till the next specific date and time, using local time
                ####-##-## ##:##:##  - Till the next specific date and time, using local time
                      All times can end with "u" to specify UTC time
                # (sec,min,hour,day) - A specific number of seconds, minutes, hours, or days.
                # (s,m,h,d) - A specific number of seconds, minutes, hours, or days.
            
            Other options:
                run <command>    - Run a command and time how long it takes to run
                run_loop <amount> <command>
                                 - Run a command over and over again, sleeping between runs
                timer            - Start a timer till enter is pressed
        """).strip()
        if ENABLE_SERVER:
            msg += "\n" + textwrap.dedent("""
                Server options:
                    server <amount>  - Run a timer, and accept clients that also stop at the same time
                                       Server also supports "run" and "timer"
                    client <name>    - Connect to a running server for the timer
            """)
        print(msg)
        exit(1)
    else:
        if sleep_amount > 0:
            while True:
                sleep(sleep_amount, exit_at_end=not keep_going)
                keep_going, sleep_amount = _get_time()
        else:
            now = datetime.now(UTC).replace(tzinfo=None)
            print(now.strftime("%d %H:%M:%S") + ": Nothing to do!")

def _temp_msg(value, old_len):
    now = datetime.now(UTC).replace(tzinfo=None)
    if value is None:
        value = ""
    else:
        value = f"{now.strftime('%d %H:%M:%S')}: {value}"
    
    if sys.stdout.isatty():
        sys.stdout.write("\r" + " " * old_len + "\r" + value)
        sys.stdout.flush()
        
        return len(value)
    else:
        return 0

def temp_nl():
    sys.stdout.write("\n")
    sys.stdout.flush()

_local_server = None
_local_running = None
def _server_thread():
    global _end_at, _server_id
    
    data = _make_server_call(set=30, alive=1)
    word = data['id']

    print("Server running, use:")
    print(f"  sleeper client {word}")
    _server_id = word
    _local_running.set()

    last_end = None
    update_tick = datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=25)

    while True:
        time.sleep(1)
        if datetime.now(UTC).replace(tzinfo=None) >= update_tick or last_end != _end_at:
            last_end = _end_at
            if last_end is None:
                _make_server_call(update=word, secs=30, alive=1)
            else:
                now = datetime.now(UTC).replace(tzinfo=None)
                secs = (last_end - now).total_seconds()
                _make_server_call(update=word, secs=secs, alive=0)
            update_tick = datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=25)
            if last_end is not None:
                break

_server_id = None
def _get_time(server_id=None):
    global _server_id
    if server_id is None:
        server_id = _server_id
    else:
        _server_id = server_id

    data = _make_server_call(get=server_id)
    if not data.get("valid", True):
        raise Exception(f"Unable to load server with key '{server_id}'")
    return data["alive"], data["secs"]

def _launch_server():
    global _local_server, _local_running

    _local_running = threading.Event()
    _local_server = threading.Thread(target=_server_thread)
    _local_server.daemon = True
    _local_server.start()
    _local_running.wait()

_enter_waiter = None
_sentinel = []
_end_at = None
def sleep(to_sleep, exit_at_end=True, extra_msg="", note_time=None):
    global _enter_waiter, _sentinel, _end_at

    if note_time is not None:
        note_time = note_time.replace(tzinfo=None)

    if isinstance(to_sleep, str):
        temp = to_sleep
        to_sleep = parse_duration(temp)
        if to_sleep is None:
            raise Exception(f"Unable to parse '{temp}'")

    now = datetime.now(UTC).replace(tzinfo=None)
    sleep = timedelta(seconds=to_sleep)
    target = now + sleep
    _end_at = target
    last_len = 0

    if _enter_waiter is None:
        _enter_waiter = threading.Thread(target=_input_thread, args=(_sentinel,))
        _enter_waiter.daemon = True
        _enter_waiter.start()

    def pretty_seconds(seconds):
        if seconds > 90000:
            msg = f"{float(seconds) / 86400.0:.1f} days"
            max_sleep = seconds - ((math.floor(seconds) // 8640) * 8640)
        elif seconds > 3900:
            msg = f"{float(seconds) / 3600.0:.1f} hours"
            max_sleep = seconds - ((math.floor(seconds) // 360) * 360)
        elif seconds > 180:
            msg = f"{float(seconds) / 60.0:.1f} minutes"
            max_sleep = seconds - ((math.floor(seconds) // 6) * 6)
        else:
            val = int(math.ceil(seconds))
            max_sleep = seconds - math.floor(seconds)
            if val == 1:
                msg = f"{val:d} second"
            else:
                msg = f"{val:d} seconds"
        return msg, max_sleep

    while True:
        if len(_sentinel) != 0:
            break

        now = datetime.now(UTC).replace(tzinfo=None)
        if now >= target:
            break

        sleep = target - now
        max_sleep = 5.0

        dur, max_sleep = pretty_seconds(sleep.total_seconds())
        noted = ""
        if note_time is not None:
            if now < note_time:
                noted, _ = pretty_seconds((note_time - now).total_seconds())
                noted = f", {noted} till event"
        last_len = _temp_msg(f"{extra_msg}Sleeping for {dur}{noted}...", last_len)

        if sleep.total_seconds() < max_sleep:
            max_sleep = sleep.total_seconds()
        max_sleep = max(max_sleep, 0.01)

        stop_at = time.time() + max_sleep
        while time.time() <= stop_at and len(_sentinel) == 0:
            max_sleep = max(0.01, stop_at - time.time())
            time.sleep(min(max_sleep, 0.25))

    if len(_sentinel) > 0:
        _temp_msg("Enter detected, aborting!", 0)
        temp_nl()
        if exit_at_end:
            exit(1)
        else:
            return False
    else:
        _temp_msg(None, last_len)
        if exit_at_end:
            exit(0)
        else:
            return True

if __name__ == "__main__":
    main()

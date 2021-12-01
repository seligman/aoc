#!/usr/bin/env python3

from datetime import datetime, timedelta
import sys
import time
import re
import threading
import math


def _make_server_call(**kargs):
    from urllib.request import urlopen
    from urllib.parse import urlencode
    import json
    kargs["cookie"] = "nbfxxfrdbnujyhcbtcotifyqy"
    url = "https://gex5mj1v01.execute-api.us-west-2.amazonaws.com/default/sleeper?" + urlencode(kargs)
    return json.loads(urlopen(url).read())


def _input_thread(sentinel):
    input()
    sentinel.append(None)


def parse_duration(val):
    sleep_amount = None

    if sleep_amount is None:
        m = re.search("^[xX]:([0-9]{2})$", val)
        if m is not None:
            now = datetime.utcnow()
            future = datetime(
                now.year, now.month, now.day, 
                now.hour, int(m.groups()[0]), 0)
            while future <= now:
                future += timedelta(hours=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.utcnow()
            future = datetime(
                now.year, now.month, now.day, 
                int(m.groups()[0]), int(m.groups()[1]), 0)
            while future <= now:
                future += timedelta(days=1)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]+):([0-9]{2}):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.utcnow()
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
            now = datetime.utcnow()
            future = datetime(
                int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 
                int(m.groups()[3]), int(m.groups()[4]), 0)
            sleep_amount = (future - now).total_seconds()

    if sleep_amount is None:
        m = re.search("^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]+):([0-9]{2}):([0-9]{2})[Uu]$", val)
        if m is not None:
            now = datetime.utcnow()
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
    start = datetime.utcnow()
    print(f" Started: {start.strftime('%Y-%m-%d %H:%M:%S')}.{start.microsecond // 1000:03d}")
    print(f" Running: '{cmd}'")
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        print(f"  Command returned {ret}")
    stop = datetime.utcnow()
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

    start = datetime.utcnow()
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

        dur = datetime.utcnow() - start

        if dur.total_seconds() > 90000:
            last_len = _temp_msg("Timer at %.1f days..." % (float(dur.total_seconds()) / 86400.0,), last_len)
            to_sleep = 8640
        elif dur.total_seconds() > 3900:
            last_len = _temp_msg("Timer at %.1f hours..." % (float(dur.total_seconds()) / 3600.0,), last_len)
            to_sleep = 360
        elif dur.total_seconds() > 180:
            last_len = _temp_msg("Timer at %.1f minutes..." % (float(dur.total_seconds()) / 60.0,), last_len)
            to_sleep = 6
        else:
            val = int(math.floor(dur.total_seconds()))
            to_sleep = 1
            if val == 1:
                last_len = _temp_msg("Timer at %d second..." % (val,), last_len)
            else:
                last_len = _temp_msg("Timer at %d seconds..." % (val,), last_len)

        last += timedelta(seconds=to_sleep)
        to_sleep = (last - datetime.utcnow()).total_seconds()
        stop_at = time.time() + to_sleep
        while time.time() <= stop_at and len(_sentinel) == 0:
            to_sleep = max(0.01, stop_at - time.time())
            time.sleep(min(to_sleep, 0.25))

    if len(_sentinel) > 0:
        _temp_msg("Enter detected", 0)
        temp_nl()
    else:
        _temp_msg(None, last_len)

    stop = datetime.utcnow()
    _show_total(start, stop, f"{stop.strftime('%d %H:%M:%S')}: ")
    _sentinel.clear()
    return 0


def main():
    sleep_amount = None
    keep_going = False
    val = " ".join(sys.argv[1:])

    if val.startswith("server run ") or val.startswith("run server "):
        _launch_server()
        time_command(val[11:])
        val = str(_get_time(_server_id)[1])
    elif val == "server timer" or val == "timer server":
        _launch_server()
        run_timer()
        val = str(_get_time(_server_id)[1])
    elif val.startswith("run "):
        exit(time_command(val[4:]))
    elif val == "timer":
        exit(run_timer())
    elif val.startswith("server "):
        _launch_server()
        val = val[7:]
    elif val.startswith("client "):
        keep_going, sleep_amount = _get_time(val[7:])
        val = ""

    if sleep_amount is None:
        if len(val) > 0:
            sleep_amount = parse_duration(val)

    if sleep_amount is None:
        import textwrap
        print(textwrap.dedent("""
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
                timer            - Start a timer till enter is pressed
                server <amount>  - Run a timer, and accept clients that also stop at the same time
                client <name>    - Connect to a running server for the timer
        """).strip())
        exit(1)
    else:
        if sleep_amount > 0:
            while True:
                sleep(sleep_amount, exit_at_end=not keep_going)
                keep_going, sleep_amount = _get_time()
        else:
            now = datetime.utcnow()
            print(now.strftime("%d %H:%M:%S") + ": Nothing to do!")


def _temp_msg(value, old_len):
    now = datetime.utcnow()
    if value is None:
        value = ""
    else:
        value = "%s: %s" % (now.strftime("%d %H:%M:%S"), value)
    
    sys.stdout.write("\r" + " " * old_len + "\r" + value)
    sys.stdout.flush()
    
    return len(value)


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
    update_tick = datetime.utcnow() + timedelta(seconds=25)

    while True:
        time.sleep(1)
        if datetime.utcnow() >= update_tick or last_end != _end_at:
            last_end = _end_at
            if last_end is None:
                _make_server_call(update=word, secs=30, alive=1)
            else:
                now = datetime.utcnow()
                secs = (last_end - now).total_seconds()
                _make_server_call(update=word, secs=secs, alive=0)
            update_tick = datetime.utcnow() + timedelta(seconds=25)
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
def sleep(to_sleep, exit_at_end=True):
    global _enter_waiter, _sentinel, _end_at

    if isinstance(to_sleep, str):
        temp = to_sleep
        to_sleep = parse_duration(temp)
        if to_sleep is None:
            raise Exception(f"Unable to parse '{temp}'")

    now = datetime.utcnow()
    sleep = timedelta(seconds=to_sleep)
    target = now + sleep
    _end_at = target
    last_len = 0

    if _enter_waiter is None:
        _enter_waiter = threading.Thread(target=_input_thread, args=(_sentinel,))
        _enter_waiter.daemon = True
        _enter_waiter.start()

    while True:
        if len(_sentinel) != 0:
            break

        now = datetime.utcnow()
        if now >= target:
            break

        sleep = target - now
        max_sleep = 5.0

        if sleep.total_seconds() > 90000:
            last_len = _temp_msg("Sleeping for %.1f days..." % (float(sleep.total_seconds()) / 86400.0,), last_len)
            max_sleep = sleep.total_seconds() - ((math.floor(sleep.total_seconds()) // 8640) * 8640)
        elif sleep.total_seconds() > 3900:
            last_len = _temp_msg("Sleeping for %.1f hours..." % (float(sleep.total_seconds()) / 3600.0,), last_len)
            max_sleep = sleep.total_seconds() - ((math.floor(sleep.total_seconds()) // 360) * 360)
        elif sleep.total_seconds() > 180:
            last_len = _temp_msg("Sleeping for %.1f minutes..." % (float(sleep.total_seconds()) / 60.0,), last_len)
            max_sleep = sleep.total_seconds() - ((math.floor(sleep.total_seconds()) // 6) * 6)
        else:
            val = int(math.ceil(sleep.total_seconds()))
            max_sleep = sleep.total_seconds() - math.floor(sleep.total_seconds())
            if val == 1:
                last_len = _temp_msg("Sleeping for %d second..." % (val,), last_len)
            else:
                last_len = _temp_msg("Sleeping for %d seconds..." % (val,), last_len)

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
        _temp_msg(None, last_len)
        if exit_at_end:
            exit(0)


if __name__ == "__main__":
    main()

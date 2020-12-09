#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta
import os

def main(lines):
    sys.path.insert(0, os.path.join('..', '..', 'Helpers'))

    from program import Program
    from dummylog import DummyLog

    #Program.debug(lines)
    p = Program([int(x) for x in lines.split(",")], DummyLog())
    while p.flag_running:
        p.tick()
        while len(p.output) > 0:
            sys.stdout.write(chr(p.get_output()))
            sys.stdout.flush()

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        main(f.read())

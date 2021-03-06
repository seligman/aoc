#!/usr/bin/env python3

import os
import imp

def get_helpers(include_disabled=False):
    required_methods = [
        "run",
        "test",
        "get_desc",
    ]

    for cur in sorted(os.listdir("Helpers")):
        cur = os.path.join("Helpers", cur)
        if cur.endswith(".py"):
            name = cur.split(os.path.sep)[-1]
            name = ".".join(name.split(".")[:-1])
            helper = imp.load_source(name, cur)
            for method in required_methods:
                if not hasattr(helper, method):
                    raise Exception("ERROR: %s doesn't implement '%s'!" % (cur, method))
            helper.filename = cur
            yield helper

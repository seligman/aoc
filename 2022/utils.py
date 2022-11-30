#!/usr/bin/env python3

import os
import imp
import hashlib

def get_helpers():
    required_methods = [
        "run",
        "test",
        "DAY_NUM",
        "DAY_DESC",
    ]

    for cur in sorted(os.listdir("Helpers")):
        if cur.startswith("day_") and cur.endswith(".py"):
            name = ".".join(cur.split(".")[:-1])
            cur = os.path.join("Helpers", cur)
            with open(cur, "rb") as f:
                hash = hashlib.sha256(f.read()).hexdigest()
            helper = imp.load_source(name, cur)
            for method in required_methods:
                if not hasattr(helper, method):
                    raise Exception(f"ERROR: {cur} doesn't implement '{method}'!")
            helper.filename = cur
            helper.hash = hash
            yield helper

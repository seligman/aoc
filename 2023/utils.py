#!/usr/bin/env python3

import os
import sys
if sys.version_info >= (3, 10): 
    import importlib.util
    import importlib.machinery
else: 
    import imp
import hashlib

def load_source(modname, filename):
    if sys.version_info >= (3, 11): 
        loader = importlib.machinery.SourceFileLoader(modname, filename)
        spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        sys.modules[module.__name__] = module
        return module
    else:
        return imp.load_source(modname, filename)

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
            helper = load_source(name, cur)
            for method in required_methods:
                if not hasattr(helper, method):
                    raise Exception(f"ERROR: {cur} doesn't implement '{method}'!")
            helper.filename = cur
            helper.hash = hash
            yield helper

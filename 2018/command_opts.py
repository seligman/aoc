#!/usr/bin/env python3

import os
import sys
import inspect
import textwrap

VERSION = 19
SAMPLE_CODE = """
# --------------------------------------------------------------------------
# This module is not meant to be run directly.  To use it, add code like
# this to a script to have this module parse the command line directly
# and call the function the user wants to invoke:
# --------------------------------------------------------------------------

#!/usr/bin/env python""" + str(sys.version_info.major) + """

from command_opts import opt, main_entry

@opt("Example function!")
def example():
    print("You passed 'example' on the command line!")

if __name__ == "__main__":
    main_entry('func')

# --------------------------------------------------------------------------
"""
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
        self.group_name = ""
        self.default = False

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
            ret.group_name = self.group_name
            ret.default = self.default
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

    if 'group' in kargs:
        method.group_name = kargs['group']

    if 'default' in kargs:
        method.default = kargs['default']

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


def main_entry(order_by='none', include_other=False, program_desc=None, default_action=None, picker=None):
    # order_by = A string representing the order conditions
    #              'none' = No order to the options
    #              'func' = Order by the function name
    #              'desc' = Order by the help text
    #              'special' = Order by the 'special' flag to @opt
    # include_other = Include @opt methods in modules outside of the main module
    # program_desc = Text to show before the main options help display
    # default_action = Default action to run if no options are present.  Can be a 
    #                  string or function
    # picker = Function to call to pick an option to run with a list of 
    #          ("desc", "object") tuples to pick an option if no options are 
    #          selected.  Expected to return "object" for the user's choice.

    global _g_options
    temp = sys.argv[1:]
    good = False

    if not include_other:
        _g_options = [x for x in _g_options if x.module_name == "__main__"]

    if default_action is None:
        for cur in _g_options:
            if cur.default:
                default_action = cur.func
                break

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
        # Look for an explicit help request
        help_found = False
        for cur in sys.argv[1:]:
            if cur.lower() in {"-h", "/h", "--help", "-?", "/?"}:
                help_found = True
                break

        # If there wasn't an explicit ask for help, and there's a 
        # default action to call, go ahead and use it
        if default_action is not None and not help_found:
            # Allow either passing in a string, or function to call
            if isinstance(default_action, str):
                for arg in _g_options:
                    for func_name in arg.func_names:
                        if default_action.replace("-", "_") == func_name:
                            default_action = arg.func
            default_action(*sys.argv[1:])
            return

        # Ok, if we get here, we're going to show help, but first
        # see if there's a picker to call instead, only if there
        # isn't an explicit ask for help
        if picker is not None and not help_found:
            # We've been told to use a picker as a backup method of 
            # selecting an action, so call it and see if it runs
            options = []
            for cur in _g_options:
                if not cur.hidden:
                    options.append((cur.help, cur))
            picked = picker(options)
            if picked is not None:
                picked.func()
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

        groups = set([x.group_name for x in options])
        groups = sorted(groups)

        for group in groups:
            if len(groups) > 1:
                group_pretty = "(Misc)" if len(group) == 0 else group
                print("  %s %s %s" % (
                    "-" * 10,
                    group_pretty,
                    "-" * (50 - len(group_pretty)),
                ))
            for arg in options:
                if not arg.hidden and arg.group_name == group:
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


def main():
    import_name = "command_opts"
    if __name__ != "__main__":
        import_name = __name__
    else:
        # Only check for the package version on Python 3
        if sys.version_info.major >= 3:
            from pathlib import Path
            temp = Path(__file__).parent.joinpath(Path("__init__.py"))
            if os.path.isfile(temp):
                import_name = str(temp.parent.name) + "." + import_name

    print(SAMPLE_CODE.replace("command_opts", import_name))
    sys.exit(1)


if __name__ == "__main__":
    main()

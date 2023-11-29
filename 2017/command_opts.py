#!/usr/bin/env python3

import inspect
import os
import sys
import textwrap

VERSION = 24
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

def opt_to_bool(value):
    # Helper to turn an opt into a bool, can return None if the value is empty
    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        value = str(value)

    if len(value) == 0:
        return None
    
    return value.lower() in {"true", "yes", "y"}

def opt_to_int(value):
    # Helper to turn an opt into an int, can return None if the value is empty
    # Also returns None if the value isn't parsable as a number
    if isinstance(value, int):
        return value
    
    if not isinstance(value, str):
        value = str(value)
    
    if len(value) == 0:
        return None
    
    try:
        return int(value)
    except:
        return None

def opt_to_float(value):
    # Helper to turn an opt into a float, can return None if the value is empty
    # Also returns None if the value isn't parsable as a number
    if isinstance(value, float):
        return value
    
    if not isinstance(value, str):
        value = str(value)
    
    if len(value) == 0:
        return None
    
    try:
        return float(value)
    except:
        return None

class OptMethod:
    # Internal data structure to keep track a single option

    def __init__(self, help):
        self.func = None            # The function to call when the option is picked
        self.func_names = []        # List of all strings that this option can can be called by
        self.hidden_args = []       # List of all args to hide in the help display
        self.help = help            # The help description for this option
        self.args = []              # List of arguments for this option
        self.parsers = []           # Optional parser to use to convert the type of each arg
        self.hidden = False         # Is this option hidden on the help screen?
        self.other = None           # The default name for this option (synthesized from .func_names)
        self.aka = None             # List of all other names for this option (synthesized from .func_names)
        self.special = None         # Optional key to control the sort order for 'sort' sort order
        self.module_name = ""       # The module name the option came from
        self.group_name = ""        # Optional group name for this option
        self.default = False        # Is option selected automatically when no option picked?

    def create_clones(self):
        # Helper to create a clone of a valid option
        if len(self.func_names) >= 1:
            ret = OptMethod(self.help)
            ret.func = self.func
            ret.args = self.args[:]
            ret.hidden = self.hidden
            ret.other = self.func_names[0]
            ret.aka = self.func_names[1:]
            ret.special = self.special
            ret.module_name = self.module_name
            ret.group_name = self.group_name
            ret.default = self.default
            ret.parsers = self.parsers[:]
            ret.hidden_args = self.hidden_args[:]
            yield ret

def opt(help_string, hidden=False, func_name:str=None, func_names:list=None, sort:str=None, group="", default=False, hidden_args:list=None):
    # This method acts as the decorator for the function
    # It's primary job is to crack out the various options passed in, create
    # a OptMethod object and add it to the global list of options.  It returns
    # a function that can be called, making the decorator work

    global _g_options
    method = OptMethod(help_string)
    _g_options.append(method)

    # Store the various options
    method.hidden = hidden
    if func_name is not None:
        method.func_names.append(func_name)
    if func_names is not None:
        method.func_names.extend(func_names)
    if hidden_args is not None:
        method.hidden_args.extend(hidden_args)
    if sort is not None:
        method.special = sort
    method.group_name = group
    method.default = default

    # Create a bounce function that's actually called by scripts
    # This exists to let us get a pointer to the real function
    def real_opts(func):
        if len(method.func_names) == 0:
            method.func_names.append(func.__name__)

        method.module_name = func.__module__
        method.func = func
        arg_spec = inspect.getfullargspec(func)
        method.args += arg_spec.args

        for i, arg in enumerate(arg_spec.args):
            target_type = None
            if arg_spec.defaults is not None and i < len(arg_spec.defaults) and arg_spec.defaults[i] is not None:
                target_type = type(arg_spec.defaults[i])
            if arg in arg_spec.annotations:
                target_type = arg_spec.annotations[arg]

            if target_type is bool:
                method.parsers.append(opt_to_bool)
            elif target_type is int:
                method.parsers.append(opt_to_int)
            elif target_type is float:
                method.parsers.append(opt_to_float)
            else:
                method.parsers.append(None)

        for i in range(len(method.args)):
            if method.args[i] in method.hidden_args:
                method.args[i] = None

        if inspect.getfullargspec(func)[3] is not None:
            for i in range(len(inspect.getfullargspec(func)[3])):
                i = -(i + 1)
                if method.args[i] is not None:
                    method.args[i] = "(" + method.args[i] + ")"
        
        method.args = [x for x in method.args if x]

        def wrapper(*args2, **kwargs):
            return func(*args2, **kwargs)
        return wrapper

    return real_opts

def main_entry(order_by='none', include_other=False, program_desc=None, default_action=None, picker=None):
    # order_by = A string representing the order conditions
    #              'none' = No order to the options
    #              'func' = Order by the function name
    #              'desc' = Order by the help text
    #              'special' = Order by the 'sort' flag to @opt
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
                            temp_args = temp[1:params + 1]
                            for i in range(len(temp_args)):
                                if callable(arg.parsers[i]):
                                    temp_args[i] = arg.parsers[i](temp_args[i])
                            arg.func(*temp_args)
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

def get_sample_code():
    # See what this script should be called, basically
    # if this is in a package, add the package name, 
    # otherwise the name is just "command_opts", but only
    # support for Python3, since the python2 "version" of
    # this script rarely gets new features
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

    return SAMPLE_CODE.replace("command_opts", import_name)

def main():
    # If called as a script, just dump a little help screen
    # showing how to embed this script in another script
    print(get_sample_code())
    sys.exit(1)

if __name__ == "__main__":
    main()

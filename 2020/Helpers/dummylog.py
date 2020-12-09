#!/usr/bin/env python3

class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)

    def __call__(self, value):
        print(value)

    def decode_values(self, values):
        ret = values.replace("\t", "    ").split("\n")
        # Only remove empty lines at the start and end
        while len(ret) > 0 and len(ret[0].strip()) == 0:
            ret = ret[1:]
        while len(ret) > 0 and len(ret[-1].strip()) == 0:
            ret = ret[:-1]
        # Remove the indenting based off the first line
        if len(ret) > 0:
            pad = len(ret[0]) - len(ret[0].lstrip(' '))
            pad -= pad % 4
        if pad > 0 and len(ret) > 0:
            for i in range(len(ret)):
                if ret[i].startswith(" " * pad):
                    ret[i] = ret[i][pad:]
        return ret

    def test(self, actual, expected):
        self.show("Test returned %s, expected %s" % (str(actual), str(expected)))
        if actual != expected:
            raise ValueError("Test failure")

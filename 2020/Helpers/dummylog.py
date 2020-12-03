#!/usr/bin/env python

class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)

    def __call__(self, value):
        print(value)

    def decode_values(self, values):
        ret = []
        for cur in values.split("\n"):
            cur = cur.strip()
            if len(cur) > 0:
                ret.append(cur)
        return ret

    def test(self, actual, expected):
        self.show("Test returned %s, expected %s" % (str(actual), str(expected)))
        if actual != expected:
            raise ValueError("Test failure")

#!/usr/bin/env python3

class DummyLog:
    def __init__(self):
        pass

    def show(self, value):
        print(value)

    def __call__(self, value):
        print(value)

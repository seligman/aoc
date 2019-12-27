#!/usr/bin/env python

class GridN:
    def __init__(self, dims, default=0):
        self.dims = dims
        self.grid = {}
        self.default = default
        self.mins = [0] * dims
        self.maxs = [0] * dims

    def get(self, *coords):
        return self.grid.get(coords, self.default)

    def size(self, dim):
        return self.maxs[dim] - self.mins[dim] + 1

    def range(self, dim):
        return range(self.mins[dim], self.maxs[dim] + 1)

    def set(self, value, *coords):
        for i in range(self.dims):
            self.mins[i] = min(self.mins[i], coords[i])
            self.maxs[i] = max(self.maxs[i], coords[i])
        self.grid[coords] = value

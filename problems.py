from math import pi

import numpy as np


class Problem:
    def __init__(self):
        print(repr(self))

    def __repr__(self):
        return "{} - f(x)={} x={}".format(self.name, self.optimal, self.optimal_coord)

    def get_best(self, obj):
        return np.min(obj)


class Sphere(Problem):
    name = "sphere"
    optimal_coord = (0, 0)
    optimal = 0

    def __init__(self, dims=2, lim=2):
        super().__init__()
        self.dims = dims
        self.lims = (-lim, lim)

    def __call__(self, *vals):
        vals = np.array(vals).reshape(self.dims)
        return np.sum(np.power(vals, 2))


class Schwefel(Problem):
    name = "schwefel"
    optimal_coord = (420.96874636, 420.96874636)
    optimal = 0

    def __init__(self, dims=2, lim=500):
        super().__init__()
        self.dims = dims
        self.lims = (-lim, lim)

    def __call__(self, *vals):
        c = 418.9828872724339
        vals = np.array(vals).reshape(self.dims)
        return c * self.dims - np.sum(np.sin(np.sqrt(np.abs(vals))) * vals)


class H1(Problem):
    name = "h1"
    optimal_coord = (8.6998, 6.7665)
    optimal = 2
    dims = 2

    def __init__(self, lim=20):
        super().__init__()
        self.lims = (-lim, lim)

    def __call__(self, vals):
        x, y = vals
        top = np.power(np.sin(x - y / 8), 2) + np.power(np.sin(y + x / 8), 2)
        bot = np.sqrt(np.power(x - 8.6998, 2) + np.power(y - 6.7665, 2)) + 1
        return -1 * top / bot


class Rastrigin(Problem):
    name = "rastrigin"
    optimal_coord = (0, 0)
    optimal = 0

    def __init__(self, dims=2, lim=5.12):
        super().__init__()
        self.dims = dims
        self.lims = (-lim, lim)

    def __call__(self, *vals):
        vals = np.array(vals).reshape(self.dims)
        return np.sum(np.power(vals, 2) - 10 * np.cos(2 * pi * vals)) + 10 * self.dims

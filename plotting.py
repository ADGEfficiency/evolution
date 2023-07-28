import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from problems import *


def create_surface(prob, num=1000):
    X, Y = np.meshgrid(
        np.linspace(start=prob.lims[0], stop=prob.lims[1], num=num, endpoint=True),
        np.linspace(start=prob.lims[0], stop=prob.lims[1], num=num, endpoint=True),
        indexing="ij",
    )

    #  can handle N-dimensional spaces
    obj = np.zeros(num**prob.dims).reshape(*(num for _ in range(prob.dims)))

    for x in range(X.shape[0]):
        for y in range(X.shape[1]):
            obj[x, y] = prob((X[x, y], Y[x, y]))

    return X, Y, obj


def plot_surface(prob, X, Y, obj, cmap=cm.plasma_r, savefig=None):
    fig = plt.figure(figsize=(20, 10))
    axe = fig.add_subplot(1, 2, 1, projection="3d")
    axe.plot_surface(X, Y, obj, cmap=cmap)
    plt.title(repr(prob), pad=100)

    axe = fig.add_subplot(1, 2, 2)
    im = axe.contourf(X, Y, obj, cmap=cmap)
    plt.tight_layout()

    fig.colorbar(im)
    if savefig:
        fig.savefig("./figs/{}.png".format(prob.name))


def plot_surface_with_points(
    prob,
    X,
    Y,
    obj,
    samples=None,
    mean=None,
    best=None,
    cmap=cm.plasma_r,
    savefig=None,
    title=None,
):
    fig = plt.figure(figsize=(10, 10))

    if title:
        fig.suptitle(title)

    axe = fig.add_subplot(1, 1, 1)
    im = axe.contourf(X, Y, obj, cmap=cmap, zorder=0)

    axe.scatter(
        x=samples[:, 0],
        y=samples[:, 1],
        marker="o",
        s=10,
        c="black",
        alpha=0.2,
        zorder=1,
    )

    axe.scatter(
        x=best[:, 0], y=best[:, 1], marker="o", s=10, c="#90EE90", alpha=1.0, zorder=2
    )

    axe.scatter(
        x=mean[:, 0], y=mean[:, 1], marker="o", s=10, c="red", alpha=1.0, zorder=3
    )

    axe.set_xlim(prob.lims)
    axe.set_ylim(prob.lims)

    if savefig:
        fig.savefig("./figs/{}.png".format(prob.name))

    return fig


def process_image_for_gif(fig):
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    return image.reshape(fig.canvas.get_width_height()[::-1] + (3,))


if __name__ == "__main__":
    probs = [Schwefel(), H1(), Rastrigin(), Sphere()]
    for prob in probs:
        X, Y, obj = create_surface(prob, num=1000)
        plot_surface(prob, X, Y, obj, savefig=True)

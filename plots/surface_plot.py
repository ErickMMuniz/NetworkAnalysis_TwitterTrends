import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from logging import warning

abd = pd.__version__
# Define a function to plot a surface.


def f(x, y):
    return np.sin(np.sqrt(x**2 + y**2))


def g(x, y):
    return np.square(np.sqrt(x**2 + y**2))


x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

warning("[RUNNING] Generating surface plot - BEFORE autoregulación")
fig = plt.figure()
ax = plt.axes(projection="3d")

ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.savefig(".\\..\\data\\images\\before_autoregulacion.png")
warning("[RUNNING] Saving figure")


warning("[RUNNING] Generating surface plot - AFTER autoregulación")
fig = plt.figure()
ax = plt.axes(projection="3d")

ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.savefig(".\\..\\data\\images\\after_autoregulacion.png")
warning("[RUNNING] Saving figure")

warning("[RUNNING] Generating surface plot - BEFORE auto-organizacion")
fig = plt.figure()
ax = plt.axes(projection="3d")

ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.savefig(".\\..\\data\\images\\before_auto-organizacion.png")
warning("[RUNNING] Saving figure")

warning("[RUNNING] Generating surface plot - AFTER auto-organizacion")
fig = plt.figure()
ax = plt.axes(projection="3d")

ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.savefig(".\\..\\data\\images\\after_auto-organizacion.png")
warning("[RUNNING] Saving figure")


warning("[RUNNING] Generating surface plot - BEFORE auto-organizacion")
fig = plt.figure()
ax = plt.axes(projection="3d")

ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.get_figure().savefig(".\\..\\data\\images\\before_emergencia.png")
warning("[RUNNING] Saving figure")

warning("[RUNNING] Generating surface plot - AFTER auto-organizacion")
fig = plt.figure()
ax = plt.axes(projection="3d")

Z = g(X, Y)
ax.contour3D(X, Y, Z, 50, cmap="binary")
ax.set_xlabel("x")
ax.view_init(60, 35)
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.savefig(".\\..\\data\\images\\after_emergencia.png")
warning("[RUNNING] Saving figure")


input("Press Enter to continue...")

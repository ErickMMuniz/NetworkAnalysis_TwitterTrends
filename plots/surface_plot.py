import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


abd = pd.__version__
# Define a function to plot a surface.


def f(x, y):
    return np.sin(np.sqrt(x**2 + y**2))


x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.view_init(60, 35)
ax.set_ylabel('y')
ax.set_zlabel('z')

fig.show()
input("Press Enter to continue...")
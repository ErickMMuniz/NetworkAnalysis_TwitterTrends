from matplotlib import font_manager

import matplotlib.pyplot as plt

from os import path

ALEGREYA = "Alegreya"


FONT_DIRS = [path.join("assets", "fonts", ALEGREYA)]
FONT_FILES = font_manager.findSystemFonts(fontpaths=FONT_DIRS)

for font_file in FONT_FILES:
    font_manager.fontManager.addfont(font_file)

plt.rcParams["font.family"] = ALEGREYA

plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.rcParams["font.size"] = 18
plt.rcParams["figure.figsize"] = [7, 7]
plt.style.use("seaborn-v0_8-pastel")

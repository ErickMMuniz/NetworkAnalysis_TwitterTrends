import os
import pprint

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from burstkit.util.read_files import get_list_trend_first_case_graphs
from networkx import read_gexf

from logging import warning

plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.size"] = 15
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.usetex"] = False
plt.style.use("bmh")

COLOR_BURST: dict[int, str] = {1: "purple", 0: "orange"}

PATH_GRAPHS_FIRST_CASE = os.path.join("data/data_new_vecindad/", "data_new_vecindad")


def read_graph_attribute_from_gefx(trend: str, attribute: str = "core") -> pd.DataFrame:
    try:
        g: nx.Graph = read_gexf(os.path.join(PATH_GRAPHS_FIRST_CASE, trend))
    except FileNotFoundError:
        g = None
    assert g is not None, "The graph is not found"
    nodes_with_data: dict[str, dict[str, str]] = dict(g.nodes(data=True))

    validated_keys : list[str] = list(nodes_with_data.values())[0].keys()
    warning(f"[NOTE] You have this keys: {validated_keys}")
    assert attribute in validated_keys, "The attribute is not found"
    keys = nodes_with_data.keys()
    values = map(
        lambda dict_attributes: dict_attributes[attribute], nodes_with_data.values()
    )
    return pd.DataFrame({"uid": keys, attribute: values})


def main() -> None:
    list_graphs_files: list[str] = get_list_trend_first_case_graphs()
    # trends_name: list[str] = list(map(lambda x: x.split(".")[0], list_graphs_files))
    TRENDS = list_graphs_files[0]

    g: nx.Graph = read_gexf(os.path.join(PATH_GRAPHS_FIRST_CASE, list_graphs_files[0]))
    foo = read_graph_attribute_from_gefx(TRENDS, attribute="core")

    pprint.pprint(dict(zip(foo.uid, foo.core)))

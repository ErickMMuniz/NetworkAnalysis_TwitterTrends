import networkx as nx
import networkit as nk
import numpy as np
from collections import Counter
from pandas import DataFrame
from typing import Optional

from src.db import read_extended_simple_graph, save_calculated_extended_graph


def metrics_for_first_neighbor(df: DataFrame) -> DataFrame:
    df["entropy"] = df["graph"].apply(calculate_network_entropy)
    df["clustering"] = df["graph"].apply(calculate_network_clustering)
    return df


def metrics_for_extended_graph(G: nx.Graph) -> nx.Graph:
    nkG = nk.nxadapter.nx2nk(G)
    # idmap : node => index
    idmap = dict((u, id) for (id, u) in zip(G.nodes(), range(G.number_of_nodes())))

    # Metrics
    core_number: dict = nx.core_number(G)
    ditc_node_community: dict = {}

    # Index hack for restore networkit for networkx
    community = nk.community.detectCommunities(
        nkG, algo=nk.community.PLM(nkG, gamma=1.0)
    )
    for cluster_users in community.getSubsetIds():
        for node in community.getMembers(cluster_users):
            ditc_node_community[idmap[node]] = cluster_users

    nx.set_node_attributes(G, core_number, "core_number")
    nx.set_node_attributes(G, core_number, "community_index")

    return G


def calculate_network_entropy(G: Optional[nx.Graph]) -> Optional[float]:
    """
    Calculate
    :param G: A non-directed network
    :return:
    """
    if G is None:
        return None
    assert not nx.is_directed(G)

    degree_sequence = sorted((degree for node, degree in G.degree()), reverse=True)

    counter = dict(Counter(degree_sequence))
    n = len(degree_sequence)
    nodes = counter.keys()
    degree = map(lambda d: d / n, counter.values())
    degree_probability = dict(zip(nodes, degree))

    X, y = degree_probability.keys(), degree_probability.values()

    entropy = np.sum(np.array(list(y)) * -np.log2(list(y)))

    return entropy


def calculate_network_clustering(G: Optional[nx.Graph]) -> Optional[float]:
    """
    Calculate
    :param G: A non-directed network
    :return:
    """
    if G is None:
        return None
    assert not nx.is_directed(G)
    return nx.average_clustering(G)


def calculate_all_metrics(trend):
    """
    General funtion to read all trends and make all calculates

    :return:
    """

    def run(trend):
        G = read_extended_simple_graph(trend)
        g_calculated = metrics_for_extended_graph(G)
        save_calculated_extended_graph(g_calculated, trend)

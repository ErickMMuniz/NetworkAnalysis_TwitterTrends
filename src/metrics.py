import networkx as nx
import numpy as np
from collections import Counter
from pandas import DataFrame
from typing import Optional


def metrics_for_first_neighbor(df: DataFrame) -> DataFrame:
    df["entropy"] = df["graph"].apply(calculate_network_entropy)
    df["clustering"] = df["graph"].apply(calculate_network_clustering)
    return df


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

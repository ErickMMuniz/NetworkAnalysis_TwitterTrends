import networkx as nx
import numpy as np
from collections import Counter


def calculate_network_entropy(G: nx.Graph) -> float:
    """
    Calculate
    :param G: A non-directed network
    :return:
    """

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

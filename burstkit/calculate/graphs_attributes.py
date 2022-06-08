from burstkit.util.generate_graphs import generate_mutual_follow_graph
from networkx import Graph
from networkx.algorithms import core_number
from networkx import set_node_attributes


def calculate_some_metrics_and_return_graph_follower() -> "Graph":
    """
    Metrics:
        - ![core number](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.core.core_number.html)
    """
    G = generate_mutual_follow_graph()

    # TODO: GET THE SAME NUMBERS IN PARALLEL COMPUTE
    core_number_attributes: "dict[int,int]" = core_number(G)

    set_node_attributes(G, core_number_attributes, name="core_number")

    return G






import pandas as pd

from burstkit.util.generate_graphs import generate_mutual_follow_graph
from networkx import Graph
from networkx.algorithms import core_number
from networkx import set_node_attributes
from networkit.centrality import (
    LocalClusteringCoefficient,
    ApproxBetweenness,
    ApproxCloseness,
    KatzCentrality,
    CoreDecomposition,
    DegreeCentrality,
    EigenvectorCentrality,
)
from networkit.community import PLM
from networkit.community import detectCommunities
from networkit import Graph as networkit_Graph
from logging import warning

from burstkit.util.read_files import write_attributes_by_trend


def calculate_some_metrics_and_return_graph_follower() -> "Graph":
    """
    Metrics:
        - ![core number](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.core.core_number.html)
        - ![degree]
        - ![communitie](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.modularity_max.greedy_modularity_communities.html)
    """
    G = generate_mutual_follow_graph()

    # TODO: GET THE SAME NUMBERS IN PARALLEL COMPUTE
    core_number_attributes: "dict[int,int]" = core_number(G)

    set_node_attributes(G, core_number_attributes, name="core_number")

    return G


### ATTRIBUTES BY NETWORKIT


def calculate_some_metrics(
    trend: "str", g: "networkit_Graph", save_to_file=False, from_colab=False
) -> "Graph":
    """
    Metrics:
        - ![Local clustering](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.LocalClusteringCoefficient
        - ![ApproxBetweenness](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.ApproxBetweenness)
        - ![ApproxCloseness](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.ApproxCloseness)
        - ![KatzCentrality](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.KatzCentrality)
        - ![CoreDecomposition](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.CoreDecomposition)
        - ![DegreeCentrality](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.DegreeCentrality)
        - ![EigenvectorCentrality](https://networkit.github.io/dev-docs/python_api/centrality.html?highlight=approx#networkit.centrality.EigenvectorCentrality)
        - ![PLM](https://networkit.github.io/dev-docs/python_api/community.html?highlight=approx#networkit.community.PLM)
    """
    percent_of_sample = 0.8
    nSamples = int(g.numberOfNodes() * percent_of_sample)

    list_of_nodes = list(map(lambda x: x, g.iterNodes()))

    local_clustering_coefficient = LocalClusteringCoefficient(g)
    # betweenness = ApproxBetweenness(g)
    closeness = ApproxCloseness(g, normalized=True, nSamples=nSamples)
    katz = KatzCentrality(g)
    core_decomposition = CoreDecomposition(g)
    degree_centrality = DegreeCentrality(g)
    eigenvector_centrality = EigenvectorCentrality(g)
    plm = PLM(g, refine=True)

    # run section
    warning(f"[{trend}][METRIC] Calculating local clustering coefficient")
    local_clustering_coefficient.run()
    warning(f"[{trend}][METRIC] Calculating betweenness")
    # betweenness.run()
    warning(f"[{trend}][METRIC] Calculating closeness")
    closeness.run()
    warning(f"[{trend}][METRIC] Calculating Katz centrality")
    katz.run()
    warning(f"[{trend}][METRIC] Calculating core decomposition")
    core_decomposition.run()
    warning(f"[{trend}][METRIC] Calculating degree centrality")
    degree_centrality.run()
    warning(f"[{trend}][METRIC] Calculating eigenvector centrality")
    eigenvector_centrality.run()
    warning(f"[{trend}][COMMUNITY] Calculating PLM")
    plm.run()

    # get results
    local_clustering_coefficient_results = local_clustering_coefficient.scores()
    # betweenness_results = betweenness.scores()
    closeness_results = closeness.scores()
    katz_results = katz.scores()
    core_decomposition_results = core_decomposition.scores()
    degree_centrality_results = degree_centrality.scores()
    eigenvector_centrality_results = eigenvector_centrality.scores()
    community_results = list(plm.getPartition().getVector())

    # save results
    if save_to_file:
        try:
            warning("Saving local clustering coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": local_clustering_coefficient_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="local_clustering",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local clustering coefficient for TREND: {trend}. File already opened"
            )

        # try:
        #     warning("Saving local betweenness coefficient")
        #     scores = pd.DataFrame(
        #         data={
        #             "uid_part": list_of_nodes,
        #             "value": betweenness_results,
        #         }
        #     )
        #     write_attributes_by_trend(
        #         trend=trend,
        #         attribute_name="betweenness",
        #         scores=scores,
        #         from_colab=from_colab,
        #     )
        # except PermissionError:
        #     warning(
        #         f"PermissionError: cannot save local betweenness coefficient for TREND: {trend}. File already opened"
        #     )

        try:
            warning("Saving local closeness coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": closeness_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="closeness",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local closeness coefficient for TREND: {trend}. File already opened"
            )

        try:
            warning("Saving local katz coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": katz_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="katz",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local katz coefficient for TREND: {trend}. File already opened"
            )

        try:
            warning("Saving local core decomposition coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": core_decomposition_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="core_decomposition",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local core decomposition coefficient for TREND: {trend}. File already opened"
            )

        try:
            warning("Saving local degree centrality coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": degree_centrality_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="degree_centrality",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local degree centrality coefficient for TREND: {trend}. File already opened"
            )

        try:
            warning("Saving local eigenvector centrality coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": eigenvector_centrality_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="eigenvector_centrality",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local eigenvector centrality coefficient for TREND: {trend}. File already opened"
            )

        try:
            warning("Saving local communitie coefficient")
            scores = pd.DataFrame(
                data={
                    "uid_part": list_of_nodes,
                    "value": community_results,
                }
            )
            write_attributes_by_trend(
                trend=trend,
                attribute_name="communitie",
                scores=scores,
                from_colab=from_colab,
            )
        except PermissionError:
            warning(
                f"PermissionError: cannot save local community coefficient for TREND: {trend}. File already opened"
            )

    warning(f"[DEBUG] All metrics calculated and saved for trend: {trend}")

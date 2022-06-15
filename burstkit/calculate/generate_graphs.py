import os.path

from pandas import DataFrame
from pandas import read_csv
from os import mkdir

from networkit.nxadapter import nx2nk, nk2nx
from networkit import Graph as networkit_Graph
from networkit import overview
from networkit.distance import BidirectionalDijkstra
from networkit import graphtools

from networkx import Graph
from networkx import write_gml

from itertools import combinations
from functools import reduce
from tqdm import tqdm
from logging import warning

from burstkit.util.manioulation import generate_pair_until_last_from_array
from burstkit.util.read_files import get_timeline_tweets_by_trend, get_path_folder_trend

unique_uid_git = []


# Necesitamos una función que dado el trend, me des la red generada de los camnios más cortos.


def get_index_node_nk_to_nx(G: "nx.Graph") -> "DataFrame":
    idmap = dict((id, u) for (id, u) in zip(G.nodes(), range(G.number_of_nodes())))
    uid = idmap.keys()
    uid_part = idmap.values()
    return DataFrame(data={"uid_part": uid_part, "uid": uid})


def save_attribute_by_partition(partition, name):
    values = partition.scores()
    DataFrame(
        data={"uid_part": index_uid_Git_trend["uid_part"], "value": values}
    ).to_csv(f"{path_trend_folder}/attributes/{name}.csv", index=False)


def calculate_shortest_path_from_uid_to_partition_id(
    source_uid: "str", target_uid: "str"
):
    source_uid_git = idmap_G_to_Git[source_uid]
    target_uid_git = idmap_G_to_Git[target_uid]
    shortest_path_source_target = BidirectionalDijkstra(
        Git, source_uid_git, target_uid_git
    )

    shortest_path_source_target.run()

    unique_uid_git.append(source_uid_git)
    unique_uid_git.append(target_uid_git)

    for inter_node in shortest_path_source_target.getPath():
        unique_uid_git.append(inter_node)


def calculate_metrics_by_networkit(G_networkit):
    # Betweennes
    betweenees = ApproxBetweenness(G_networkit)

    # run
    betweenees.run()

    # partiton and save to Drive
    save_attribute_by_partition(betweenees, "betweenees")


# PATH_INDEX_TRENDS = "/content/drive/MyDrive/tesis/data/networks_by_trend"
# PATH_FOLDERS_TREND = "/content/drive/MyDrive/tesis/data/networks_by_trend"
#
# index_trend = read_csv(f"{PATH_INDEX_TRENDS}/index_trends.csv")
# index_id_trend: "dict[str, int]" = dict(zip(index_trend["trend"], index_trend["id_trend"]))
#
# trend = "gop"
# folder_name_trend = f"TREND_ID_{index_id_trend[trend]}"
# path_trend_folder = f"{PATH_FOLDERS_TREND}/{folder_name_trend}"
#
# try:
#     mkdir(path_trend_folder)
# except FileExistsError:
#     pass
#
# try:
#     mkdir(f"{path_trend_folder}/attributes")
# except FileExistsError:
#     pass

# timeline_tweets_trend: "DataFrame" = TREND_TIMELINE_TWEETS[trend]
# user_trend_tweets = timeline_tweets_trend["uid"].unique()
# G_trend = G.subgraph(user_trend_tweets)
# uid_uid_G = list(combinations(G_trend.nodes(), 2))
#
# # unique_uid_git = []
#
# idmap_G_to_Git = dict((id, u) for (id, u) in zip(G.nodes(), range(G.number_of_nodes())))
#
# for s, t in tqdm(uid_uid_G[:5]):
#     calculate_shortest_path_from_uid_to_partition_id(s, t)
#
# unique_uid_git_trend = set(unique_uid_git)
#
# G_foo = nk2nx(graphtools.subgraphFromNodes(Git, unique_uid_git_trend))

# map( lambda source_target: calculate_shortest_path_from_uid_to_partition_id(source_target[0],source_target[1]), uid_uid_G)

# Get network from mutual follow
# G_trend = G.subgraph(user_trend_tweets)


def get_path_nodes(G: "networkit_Graph", s: "int", t: "int") -> "set[int]":
    inter_nodes = get_inter_nodes_git_trend(G, s, t)
    inter_nodes.add(s)
    inter_nodes.add(t)
    return inter_nodes


def get_inter_nodes_git_trend(G: "networkit_Graph", s: "int", t: "int") -> "set[int]":
    """
    Note: Source and target are not in the path
    """
    shortest_path = BidirectionalDijkstra(G, s, t)
    shortest_path.run()
    return set(shortest_path.getPath())


def transform_networkx_to_networkit(g: "Graph") -> "Graph":
    return nx2nk(g)


def get_combinators_from_nodes_list(nodes_list: "list[str]") -> "list[tuple[str, str]]":
    return list(combinations(nodes_list, 2))


def map_node_to_uid_g(node: "int", id_map: "dict[int, str]") -> "str":
    return id_map[node]


def map_node_to_uid_git(node: "str", id_map: "dict[str, int]") -> "str":
    return id_map[node]


def get_really_nodes_from_networkx_graph(g: "Graph") -> "list[str]":
    return list(g.nodes())


def get_networkx_graph_from_raw_nodes(g: "Graph", raw_nodes: "list[str]") -> "nx.Graph":
    return g.subgraph(raw_nodes)


def get_unique_users_raw(timeline: "DataFrame") -> "list[str]":
    return timeline["uid"].unique()


def get_timeline(timelines: "dict[str, DataFrame]", trend: "str") -> "DataFrame":
    return timelines[trend]


def get_unique_users_from_timeline_to_networkit(
    trend: "str",
    timelines: "dict[str,DataFrame]",
    g: "Graph",
    git: "networkit_Graph",
    idmap_g_to_git: "dict[str, int]",
) -> "list[int]":
    timeline = get_timeline(timelines, trend)
    uid_raw = get_unique_users_raw(timeline)
    g_networkx: "Graph" = get_networkx_graph_from_raw_nodes(g, uid_raw)
    clean_uid_raw: "list[str]" = get_really_nodes_from_networkx_graph(g_networkx)
    source_target: "list[tuple[str, str]]" = get_combinators_from_nodes_list(
        clean_uid_raw
    )

    warning("[RUNNING] Calculating shortest path from source to target")

    set_nodes: "list[set[int]]" = list(
        map(
            lambda source_target: get_path_nodes(
                git,
                map_node_to_uid_git(source_target[0], idmap_g_to_git),
                map_node_to_uid_git(source_target[1], idmap_g_to_git),
            ),
            tqdm(source_target),
        )
    )
    union_sets: "list[int]" = list(reduce(lambda x, y: x.union(y), set_nodes))
    return union_sets


def get_unique_users_from_timeline_to_networkit_in_susseive_way(
    trend: "str",
    g: "Graph",
    git: "networkit_Graph",
    idmap_g_to_git: "dict[str, int]",
    save_path: "bool" = False,
    path_to_save: "str" = None,
) -> "Graph":
    """Esta función es más eficiente que la anterior, pero solo considera que un tiempo. Un nodo sigue a otro si en el timeline está seguidos."""
    timeline: "DataFrame" = get_timeline_tweets_by_trend(trend)
    source_target_raw: "list[(str,str)]" = generate_pair_until_last_from_array(
        timeline["uid"]
    )
    nodes_clean = list(g.nodes())
    source_target = list(
        filter(lambda x: x[0] in nodes_clean and x[1] in nodes_clean, source_target_raw)
    )

    warning("[RUNNING] Calculating shortest path from source to target")

    set_nodes: "list[set[int]]" = list(
        map(
            lambda source_target: get_path_nodes(
                git,
                map_node_to_uid_git(source_target[0], idmap_g_to_git),
                map_node_to_uid_git(source_target[1], idmap_g_to_git),
            ),
            tqdm(source_target),
        )
    )
    union_sets: "list[int]" = list(reduce(lambda x, y: x.union(y), set_nodes))

    neighbour: "networkit_Graph" = graphtools.subgraphFromNodes(git, union_sets)

    neighbour_nx: "Graph" = nk2nx(neighbour)

    if save_path:
        if path_to_save is None:
            path = get_path_folder_trend(trend)
        else:
            path = path_to_save
        write_gml(neighbour_nx, os.path.join(path, "network_neighbour.gml"))

    return neighbour_nx


if __name__ == "__main__":
    pass

# Git_trend = nx2nk(G_trend)

# #Guardamos el índice de los usuarios.

# index_uid_Git_trend : "DataFrame" = get_index_node_nk_to_nx(G_trend)

# index_uid_Git_trend.to_csv(f"{path_trend_folder}/index_nodes.csv", index = False)

# # betweenees = ApproxBetweenness(Git_trend)
# # #run
# # betweenees.run()

# calculate_metrics_by_networkit(Git_trend)


# #overview(Git_trend)

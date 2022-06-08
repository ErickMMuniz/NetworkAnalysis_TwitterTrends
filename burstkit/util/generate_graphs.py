from burstkit.util.read_files import *
import networkx as nx


def generate_mutual_follow_graph(limit_rows: "int" = None) -> "nx.Graph":
    edge_df = get_mutual_followers(limit_rows=limit_rows)
    return nx.from_pandas_edgelist(df=edge_df, source="source", target="target")

from burstkit.util.read_files import get_mutual_followers
import networkx as nx

#FIXME: HOT FIX
SOURCE = "source"
TARGET = "target"

def generate_mutual_follow_graph(limit_rows: "int" = None) -> "nx.Graph":
    edge_df = get_mutual_followers(limit_rows=limit_rows)
    return nx.from_pandas_edgelist(df=edge_df, source="source", target="target")

def generate_graph_from_dataframe(dataframe: "pd.DataFrame", is_directed = False) -> "nx.Graph | nx.Digraph":
    return nx.from_pandas_edgelist(df=dataframe, source=SOURCE, target=TARGET)
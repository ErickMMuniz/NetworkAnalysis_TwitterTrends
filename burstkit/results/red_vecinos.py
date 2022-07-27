from pandas import DataFrame
from logging import warning
from pandas import Grouper


# FIXME: HOT FIX #############################################################
import matplotlib.pyplot as plt

plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.size"] = 15
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.usetex"] = False

# mpl.rcParams['axes.prop_cycle'] = cycler(color=['r', 'g', 'b', 'y'])
# print(plt.style.available)
plt.style.use("bmh")

from burstkit.util.read_files import (
    get_timeline_tweets_by_trend,
    get_dataframe_trend_to_id,
    get_nx_graph_from_file,
    get_uid_list_from_networkx,
    get_attribute_uidpart_dataframe_by_trend,
)


def group_timeline_by_interval(interval: "str" = "15min"):
    pass


def main():
    TREND: "str" = "gop"

    idmap: "dict[str,str]" = get_dataframe_trend_to_id()
    ID: "int" = idmap[TREND]
    warning(f"ID: {ID}")
    warning(f"TREND: {TREND}")
    warning("#############################################################")
    warning("Reading timeline tweets...")
    timeline: "DataFrame" = get_timeline_tweets_by_trend(TREND)
    warning("#############################################################")
    warning("Reading active users...")
    g_neig = get_nx_graph_from_file(ID)
    warning("#############################################################")
    warning("Reading network...")
    attributes = get_attribute_uidpart_dataframe_by_trend(
        id_trend=ID, attribute="core_decomposition"
    )
    idmap_g_to_git = dict(zip(g_neig.nodes(), range(len(g_neig.nodes))))
    idmap_core = dict(zip(g_neig.nodes(), attributes["value"]))

    print(idmap_core)
    foo = timeline
    foo["attribute"] = foo["uid"].replace(idmap_core)
    foo["count"] = 1
    foo["attribute"] = foo["attribute"].astype(float)
    # Index(['timestamp', 'uid', 'attribute', 'count'], dtype='object')
    # foo.index = foo['timestamp']
    # No se pone index aquí con el timestamp porque puede haber tweets en el mismo segundo

    freq = "60min"
    rng = Grouper(freq=freq)

    foo.index = foo["timestamp"]

    count = foo["count"].groupby(rng).sum()
    attribute = foo["attribute"].groupby(rng).mean()
    print(count)
    print(attribute)
    X = count.index

    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax = axes.flatten()
    ax[0].plot(X, count, label="count", color="red")
    ax[1].plot(X, attribute, label="attribute", color="blue")
    fig.legend()
    fig.show()

    # list_nodes = get_uid_list_from_networkx(g_neig)

    print(":D ")

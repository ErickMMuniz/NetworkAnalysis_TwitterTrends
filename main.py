import pandas as pd
import matplotlib as plt
import numpy as np
import burstkit.util.read_files as rf
import burstkit.util.generate_graphs as gg
import networkx as nx

from burstkit.calculate.generate_graphs import (
    get_unique_users_from_timeline_to_networkit,
)
from burstkit.util.User import User
from pprint import pprint
from burstkit.util.generate_graphs import generate_mutual_follow_graph
from networkit.nxadapter import nx2nk
from networkit import overview

# G: "nx.Graph" = gg.generate_mutual_follow_graph(100)

# pprint(G.number_of_nodes())


G = generate_mutual_follow_graph()
Git = nx2nk(G)

TREND_TIMELINE_TWEETS: "dict[str, pd.DataFrame]" = (
    rf.get_relation_trend_timeline_tweets(min_number_tweets=4000)
)

id_map_g_to_git = dict(zip(G.nodes(), range(G.number_of_nodes())))
id_map_git_to_g = dict(zip(id_map_g_to_git.values(), id_map_g_to_git.keys()))


# TREND_TIMELINE_RETWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_retweets(1000)
# TREND_TIMELINE_MENTIONS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_mentions(1000)
#
# print(TREND_TIMELINE_TWEETS)
# print(TREND_TIMELINE_RETWEETS)
# print(TREND_TIMELINE_MENTIONS)
# test = filter(lambda trend_name: TREND_TIMELINE_TWEETS[trend_name].shape[0] > 1, TREND_TIMELINE_TWEETS)
# print(next(test))
# trend = list(TREND_TIMELINE_TWEETS.keys())[2]
# df = TREND_TIMELINE_TWEETS[trend]
# print(df.dtypes)
# calculate_some_metrics_and_return_graph_follower()

def save_timeline_line_dataframe(trend: "str"):
    timeline: "pd.DataFrame" = TREND_TIMELINE_TWEETS[trend]
    id = map_id_trend[trend]

    FOLDER_NAME = f"TREND_ID_{id}"

    try:
        mkdir(f"{PATH_ROOT_NETWORKS_BY_TREND}\\{FOLDER_NAME}")
    except FileExistsError:
        pass

    timeline.to_csv(f"{PATH_ROOT_NETWORKS_BY_TREND}\\{FOLDER_NAME}\\tweets_timeline.csv", index=False)


if __name__ == "__main__":
    trend = "gop"
    # list_set_int = get_unique_users_from_timeline_to_networkit(
    #     trend = trend, timelines=TREND_TIMELINE_TWEETS, g=G, git=Git, idmap_g_to_git=id_map_g_to_git
    # )
    # print(list_set_int)

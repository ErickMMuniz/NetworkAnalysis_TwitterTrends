import pandas as pd
import matplotlib as plt
import numpy as np
import burstkit.util.read_files as rf
import burstkit.util.generate_graphs as gg
import networkx as nx
from burstkit.util.User import User
from pprint import pprint
from burstkit.calculate.graphs_attributes import calculate_some_metrics_and_return_graph_follower

#G: "nx.Graph" = gg.generate_mutual_follow_graph(100)

#pprint(G.number_of_nodes())







TREND_TIMELINE_TWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_tweets(1000)
TREND_TIMELINE_RETWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_retweets(1000)
TREND_TIMELINE_MENTIONS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_mentions(1000)

print(TREND_TIMELINE_TWEETS)
print(TREND_TIMELINE_RETWEETS)
print(TREND_TIMELINE_MENTIONS)
test = filter(lambda trend_name: TREND_TIMELINE_TWEETS[trend_name].shape[0] > 1, TREND_TIMELINE_TWEETS)
print(next(test))
trend = list(TREND_TIMELINE_TWEETS.keys())[2]
df = TREND_TIMELINE_TWEETS[trend]
print(df.dtypes)
calculate_some_metrics_and_return_graph_follower()
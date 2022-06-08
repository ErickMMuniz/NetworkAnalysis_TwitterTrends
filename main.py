import pandas as pd
import matplotlib as plt
import numpy as np
import burstkit.util.read_files as rf
import burstkit.util.generate_graphs as gg
import networkx as nx
from burstkit.util.User import User
from pprint import pprint

#G: "nx.Graph" = gg.generate_mutual_follow_graph(100)

#pprint(G.number_of_nodes())
from burstkit.util import SEED
np.random.seed(SEED)
some_array = [1,2,3,4,5,6,7,8,9]
print(np.random.choice(some_array))
some_dict = {"a": [1,2,3,4],
             "b": [123,45]}
print(some_dict.values())
print(some_dict.keys())
print(rf.get_relation_trend_timeline_retweets(100)['007april'])

TREND_TIMELINE_TWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_tweets()
TREND_TIMELINE_RETWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_retweets()
TREND_TIMELINE_MENTIONS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_mentions()

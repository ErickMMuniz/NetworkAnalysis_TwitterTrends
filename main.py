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


TREND_TIMELINE_TWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_tweets(1000)
#TREND_TIMELINE_RETWEETS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_retweets()
#TREND_TIMELINE_MENTIONS : "dict[str, pd.DataFrame]" = rf.get_relation_trend_timeline_mentions()

"""
A package to save the principal function to analysis the networks of burst trends.
"""
import tarfile
import pandas as pd
import numpy as np
import networkx as nx
#import networkit as nk
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import collections
import itertools
import random
import seaborn as sn
import threading
import os
import logging
import pytz
from datetime import datetime

from readata import *

main_seed = 123456789
np.random.seed(main_seed)

path_main_drive = "/content/drive/My Drive/NetworkAnalysis_TwitterTrends/virality2013.tar.gz"
path_friends_followers = "/content/follower_gcc.anony.dat"
path_tweets_users = "/content/timeline_tag.anony.dat"
path_retweets_users = "/content/timeline_tag_rt.anony.dat"
path_mentions_users = "/content/timeline_tag_men.anony.dat"

# FINALS_DATAFRAME
path_final_dataframe = '/content/drive/MyDrive/FC_Materias/FC_Proyecto_1/finaldf.csv'


if __name__ == '__main__':
    extract_file_from_drive(path_main_drive)

    # Toda la info
    dic_tweets_user = get_dic_tweets()
    dic_retweets_user = get_dic_retweets()
    dic_mentions_user = get_dic_mentions()

    # Vamos a tomar las tendencias que coincidan.
    set_trend_tweets = set(dic_tweets_user.keys())
    set_trend_retweets = set(dic_retweets_user.keys())
    set_trend_menntions = set(dic_mentions_user.keys())

    # Variables generales
    list_trends = list(set_trend_menntions & set_trend_retweets & set_trend_tweets)
    df_mutual_follow = get_data_followers_and_friends()

    array_true_trends = pd.read_csv(path_final_dataframe)[['trend', 'burst']]
    print("This is a test")

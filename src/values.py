import os
from typing import Text
from pandas import read_csv
from numpy import array_split

SEED = 11245

MINIMUN_TWEETS = 4000
WINDOW_STUDY = 30

MAX_RECURSIVE_EXTENDED_GRAPH = 20000

HASHTAG_RE: Text = "\w+(?=\s)"
TWEET_LOG_RE: Text = "\d+,\d+"
RETWEET_LOG_RE: Text = "\d+,\d+,\d+"

FOLLOWER_GCC: Text = "follower_gcc.anony.dat"
TIMELINE_TWEETS: Text = "timeline_tag.anony.dat"
TIMELINE_RETWEETS: Text = "timeline_tag_rt.anony.dat"
FINAL_DF: Text = "finaldf.csv"

DATA_PATH: Text = os.path.join(os.getcwd(), "data")
DB_PATH: Text = os.path.join(os.getcwd(), "db")

MUTUAL_FOLLOWERS_PATH: Text = os.path.join(DATA_PATH, FOLLOWER_GCC)
TIMELINE_TWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_TWEETS)
TIMELINE_RETWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_RETWEETS)
FINAL_DF_PATH: Text = os.path.join(DB_PATH, FINAL_DF)

EXTENDED_GRAPH_PATH: Text = os.path.join(DB_PATH, "extended_graph")
ACITVE_USERS_IN_15MINUTES_WINDOWS_FOLDER: Text = os.path.join(
    EXTENDED_GRAPH_PATH, "active_users_in_25minutes_windows"
)
VALID_USER: Text = os.path.join(EXTENDED_GRAPH_PATH, "valid_users")
EXTENDED_GRAPHS: Text = os.path.join(EXTENDED_GRAPH_PATH, "graphs")

FIRST_NEIGHBOR_PATH: Text = os.path.join(DB_PATH, "first_neighbor")
TRENDS_DB: Text = os.path.join(DB_PATH, "timelines_trends.csv")


MUTUAL_FOLLOWING = read_csv(
    MUTUAL_FOLLOWERS_PATH, sep=" ", names=["source", "target"], dtype=str
)
SPLIITED_MUTUAL_FOLLOWING = array_split(MUTUAL_FOLLOWING, 28)

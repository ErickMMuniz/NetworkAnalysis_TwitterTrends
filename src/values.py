import os
from typing import Text


MINIMUN_TWEETS = 4000

HASHTAG_RE: Text = "\w+(?=\s)"
TWEET_LOG_RE: Text = "\d+,\d+"
RETWEET_LOG_RE: Text = "\d+,\d+,\d+"

FOLLOWER_GCC: Text = "follower_gcc.anony.dat"
TIMELINE_TWEETS: Text = "timeline_tag.anony.dat"
TIMELINE_RETWEETS: Text = "timeline_tag_rt.anony.dat"

DATA_PATH: Text = os.path.join(os.getcwd(), "data")
MUTUAL_FOLLOWERS_PATH: Text = os.path.join(DATA_PATH, FOLLOWER_GCC)
TIMELINE_TWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_TWEETS)
TIMELINE_RETWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_RETWEETS)

DB_PATH: Text = os.path.join(os.getcwd(), "db")
TRENDS_DB: Text = os.path.join(DB_PATH,"timelines_trends.csv")

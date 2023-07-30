import os
from typing import Text


MINIMUN_TWEETS = 4000

HASHTAG_RE: Text = "\w+(?=\s)"
TWEET_LOG_RE: Text = "\d+,\d+"

FOLLOWER_GCC: Text = "follower_gcc.anony.dat"
TIMELINE_TWEETS: Text = "timeline_tag.anony.dat"

DATA_PATH: Text = os.path.join(os.getcwd(), "data")
MUTUAL_FOLLOWERS_PATH: Text = os.path.join(DATA_PATH, FOLLOWER_GCC)
TIMELINE_TWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_TWEETS)

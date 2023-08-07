from src.values import *
from src.io import read_tweets, read_retweets, read_all_trends_names
from src.objects import *
from src.util import *


import pandas as pd
import logging
import os

from datetime import datetime
from typing import Optional


def get_trend_str(trend):
    logging.warning("[READING TWEET/RETWEET USERS] BEGIN {}".format(trend))
    trend_with_tweets = read_tweets(trend)
    trend_with_retweets = read_retweets(trend)

    t = Trend(trend=trend, tweets=trend_with_tweets.tweets,
              retweets=trend_with_retweets.retweets)
    assert t.tweets
    assert t.retweets
    created_at = datetime.now()
    logging.warning("[READING TWEET/RETWEET USERS] END {}".format(trend))
    return t.json(), created_at

def generate_timelines_in_csv():
    assert os.path.isdir(DB_PATH)
    assert os.path.isdir(DATA_PATH)
    assert os.path.isfile(MUTUAL_FOLLOWERS_PATH)
    assert os.path.isfile(TIMELINE_TWEETS_PATH)
    assert os.path.isfile(TIMELINE_RETWEETS_PATH)


    TRENDS = read_all_trends_names()[:]
    logging.warning("TRENDS IMPORTED")

    trends_format = parallel_map(get_trend_str, TRENDS)

    trend_json, created_at_column = list(map(list, zip(*trends_format)))

    df = pd.DataFrame(
        data={"id": range(len(TRENDS)), "name": TRENDS, "dump_trend": trend_json, "created_at": created_at_column})
    df.to_csv(TRENDS_DB, index=False)


def read_trend_dump(trend : Optional[Text] = None):
    df = pd.read_csv(TRENDS_DB)
    result = df if trend is None else df[df['name'] == trend]
    return result


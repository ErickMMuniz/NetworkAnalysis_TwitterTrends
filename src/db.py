import networkx as nx

from src.values import *
from src.io import read_tweets, read_retweets, read_all_trends_names, get_edge_list_by_users
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


def generate_first_neighbor_by_trend(TREND: Text):
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)

    df = read_trend_dump(TREND)
    t = df['dump_trend'].apply(Trend.parse_raw).iloc[0]

    splited_time = split_by_time(t)

    key_list = []
    edge_list_primera_vecindad = []
    tweets_c = []
    retweets_c = []

    foo = list(splited_time.keys())[:]
    for i,key in enumerate(foo):
        logging.warning("[{} / {} ----  {}] importing user friends ".format(i, len(foo), TREND))
        tweets: List[Tweet] = splited_time[key]["tweets"]
        retweets: List[ReTweet] = splited_time[key]["retweets"]

        users = list(map(lambda tweet: tweet.user, tweets))
        edge_list: Optional[Text] = get_edge_list_by_users(users)

        key_list.append(key)
        edge_list_primera_vecindad.append(edge_list)
        tweets_c.append(Trend(trend=TREND, tweets=tweets).json())
        retweets_c.append(Trend(trend=TREND, retweets=retweets).json())

    df = pd.DataFrame(data={"first_hour": key_list, "edge_list": edge_list_primera_vecindad, "tweets": tweets_c,
                            "retweets": retweets_c})

    first_neighbor_trend_path = os.path.join(FIRST_NEIGHBOR_PATH, "{}.csv".format(TREND))
    df.to_csv(first_neighbor_trend_path, index=False)


def generate_first_neighbor(only_labeled_trends = True):
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)
    assert os.path.isfile(MUTUAL_FOLLOWERS_PATH)
    assert os.path.isfile(TIMELINE_TWEETS_PATH)
    assert os.path.isfile(TIMELINE_RETWEETS_PATH)

    TRENDS = read_all_trends_names()[:]

    labeled_trends = pd.read_csv(FINAL_DF_PATH)['trend'].to_list()
    # print(trends_label["trend"].to_list())
    logging.warning("TRENDS IMPORTED")
    trends = list(set(TRENDS) & set(labeled_trends))

    trends_format = parallel_map(generate_first_neighbor_by_trend, trends)


def read_maybe_graph(result) -> Optional[nx.Graph]:
    empty_graph = """Columns: [source, target]
Index: []"""
    if empty_graph in result:
        return None
    else:
        return nx.parse_edgelist(result.split("\n"), nodetype=str)
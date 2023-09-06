import networkx as nx

from src.values import *
from src.io import (
    read_tweets,
    read_retweets,
    read_all_trends_names,
    get_edge_list_by_users,
    get_first_neigh,
    get_many_user, read_mutual_follow_graph,
)
from src.objects import *
from src.util import *

import pandas as pd
import logging
import os

from datetime import datetime
from typing import Optional, Dict, Any
from itertools import chain


def get_trend_str(trend):
    logging.warning("[READING TWEET/RETWEET USERS] BEGIN {}".format(trend))
    trend_with_tweets = read_tweets(trend)
    trend_with_retweets = read_retweets(trend)

    t = Trend(
        trend=trend,
        tweets=trend_with_tweets.tweets,
        retweets=trend_with_retweets.retweets,
    )
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
        data={
            "id": range(len(TRENDS)),
            "name": TRENDS,
            "dump_trend": trend_json,
            "created_at": created_at_column,
        }
    )
    df.to_csv(TRENDS_DB, index=False)


def read_trend_dump(trend: Optional[Text] = None):
    df = pd.read_csv(TRENDS_DB)
    result = df if trend is None else df[df["name"] == trend]
    return result


def generate_first_neighbor_by_trend(TREND: Text):
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)

    df = read_trend_dump(TREND)
    t = df["dump_trend"].apply(Trend.parse_raw).iloc[0]

    splited_time = split_by_time(t)

    key_list = []
    edge_list_primera_vecindad = []
    tweets_c = []
    retweets_c = []

    foo = list(splited_time.keys())[:]
    for i, key in enumerate(foo):
        logging.warning(
            "[{} / {} ----  {}] importing user friends ".format(i, len(foo), TREND)
        )
        tweets: List[Tweet] = splited_time[key]["tweets"]
        retweets: List[ReTweet] = splited_time[key]["retweets"]

        users = list(map(lambda tweet: tweet.user, tweets))
        edge_list: Optional[Text] = get_edge_list_by_users(users)

        key_list.append(key)
        edge_list_primera_vecindad.append(edge_list)
        tweets_c.append(Trend(trend=TREND, tweets=tweets).json())
        retweets_c.append(Trend(trend=TREND, retweets=retweets).json())

    df = pd.DataFrame(
        data={
            "first_hour": key_list,
            "edge_list": edge_list_primera_vecindad,
            "tweets": tweets_c,
            "retweets": retweets_c,
        }
    )

    first_neighbor_trend_path = os.path.join(
        FIRST_NEIGHBOR_PATH, "{}.csv".format(TREND)
    )
    df.to_csv(first_neighbor_trend_path, index=False)


def generate_first_neighbor(only_labeled_trends=True):
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)
    assert os.path.isfile(MUTUAL_FOLLOWERS_PATH)
    assert os.path.isfile(TIMELINE_TWEETS_PATH)
    assert os.path.isfile(TIMELINE_RETWEETS_PATH)

    TRENDS = read_all_trends_names()[:]

    labeled_trends = pd.read_csv(FINAL_DF_PATH)["trend"].to_list()
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


def read_trend_first_neighbor(trend: Optional[Text] = None):
    assert os.path.isdir(DB_PATH)
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)
    path = os.path.join(FIRST_NEIGHBOR_PATH, "{}.csv".format(trend))
    assert os.path.isfile(path)

    df = pd.read_csv(path)
    df["graph"] = df["edge_list"].apply(read_maybe_graph)

    return df


def generate_extended_only_true_users(trend: Optional[Text] = None):
    assert os.path.isdir(FIRST_NEIGHBOR_PATH)
    STUDY = 50

    df = read_trend_dump(trend)
    t = df["dump_trend"].apply(Trend.parse_raw).iloc[0]

    print("spliting times")
    splited_time: Dict[str, Dict] = split_by_time(
        t, windows_study=STUDY
    )

    # Get all users == Get user for all tweets
    user_by_window: List[List[Text]] = list(
        map(
            lambda listTweets: list(map(lambda t: t.user, listTweets)),
            map(lambda dictValues: dictValues["tweets"], splited_time.values()),
        )
    )

    unique_users = set(list(chain.from_iterable(user_by_window)))
    return unique_users


def _generate_active_users_in25minutes(trend):
    logging.warning(
        "[BEGIN] Calculating active users in 25 minutes for {} ".format(trend)
    )
    path = os.path.join(
        ACITVE_USERS_IN_15MINUTES_WINDOWS_FOLDER, "{}.txt".format(trend)
    )

    active_users = generate_extended_only_true_users(trend)
    active_users = map(lambda user: User(id=user), active_users)
    users_to_save = Users(value=list(active_users))
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(users_to_save.json())
            f.close()

    logging.warning("[END] trend => {} ".format(trend))


def generate_active_users_inOneHour_windows():
    assert os.path.isdir(ACITVE_USERS_IN_15MINUTES_WINDOWS_FOLDER)

    TRENDS = read_all_trends_names()[:]

    labeled_trends = pd.read_csv(FINAL_DF_PATH)["trend"].to_list()
    # print(trends_label["trend"].to_list())
    logging.warning("TRENDS IMPORTED")
    trends = list(set(TRENDS) & set(labeled_trends))

    trends_format = parallel_map(_generate_active_users_in25minutes, trends)


def generate_valid_users_for_extended_graph():
    assert os.path.isdir(ACITVE_USERS_IN_15MINUTES_WINDOWS_FOLDER)
    TRENDS = read_all_trends_names()[:]

    labeled_trends = pd.read_csv(FINAL_DF_PATH)["trend"].to_list()
    # print(trends_label["trend"].to_list())
    logging.warning("TRENDS IMPORTED")
    trends = list(set(TRENDS) & set(labeled_trends))

    def run(trend):
        logging.warning("[BEGIN] Calculating valid for \t {} ".format(trend))
        path = os.path.join(
            ACITVE_USERS_IN_15MINUTES_WINDOWS_FOLDER, "{}.txt".format(trend)
        )
        assert os.path.exists(path)
        with open(path, "r") as f:
            lines = "\n".join(f.readlines())
            f.close()
            users = Users.parse_raw(lines)
            users = list(map(lambda user: user.id, users.value))
            users = get_many_user(users)
            users = map(lambda user: User(id=user), users)
            users_to_save = Users(value=list(users))
            path_to_save = os.path.join(VALID_USER, "{}.txt".format(trend))
        if not os.path.exists(path_to_save):
            with open(path_to_save, "w") as s:
                s.write(users_to_save.json())
                s.close()
        logging.warning("[END] valid users for => \t {} ".format(trend))

    # parallel_map(run, trends)
    for i,trend in enumerate(trends):
        print("trend => {} \t  {} / {}".format(trend, i, len(trends)))
        path_to_save = os.path.join(VALID_USER, "{}.txt".format(trend))
        if not os.path.exists(path_to_save):
            run(trend)

def read_extended_valid_users(trend) -> List[Text]:
    path = os.path.join(VALID_USER, "{}.txt".format(trend))

    assert os.path.exists(path)
    users_to_find = []
    with open(path, "r") as f:
        lines = "\n".join(f.readlines())
        users: List[User] = Users.parse_raw(lines).value
        users_to_find = map(lambda u: u.id, users)
        f.close()
    return users_to_find


def generate_extended_graph(number_chunks = -1):
    assert os.path.exists(EXTENDED_GRAPHS)

    G_mutual = read_mutual_follow_graph(number_chunks)

    TRENDS = read_all_trends_names()[:]

    labeled_trends = pd.read_csv(FINAL_DF_PATH)["trend"].to_list()
    logging.warning("TRENDS IMPORTED")
    trends = list(set(TRENDS) & set(labeled_trends))

    def run(trend):
        users_to_find = read_extended_valid_users(trend)
        subgraph = G_mutual.subgraph(users_to_find)

        path_graph = os.path.join(EXTENDED_GRAPHS, "{}.gefx".format(trend))
        if not os.path.exists(path_graph):
            nx.write_gexf(subgraph,path_graph)

    for trend in trends:
        run(trend)
import logging
import re
import networkx as nx
import pandas as pd
from tqdm import tqdm
from numpy import any as np_any
from numpy import concatenate, unique
from logging import warning

from src.values import *
from src.objects import *
from src.random import choice


def read_and_parse_mutual_followers_dat(path: Text, limit_lines=100) -> nx.Graph:
    USER_RE = "\d+"
    with open(path) as file:
        for i, line in enumerate(file):
            assert i < limit_lines
            maybe_users = re.findall(USER_RE, line.strip())
            print(maybe_users)


def read_mutual_follow_graph(number_parts = -1):
    logging.warning("[MUTUAL FOLLOW GRAPH] Reading")
    path = os.path.exists(MUTUAL_FOLLOWERS_PATH)
    assert path

    compose_graph = nx.Graph() # Empty graph

    for part in enumerate(SPLIITED_MUTUAL_FOLLOWING[:number_parts]):
        logging.warning("[compuse] G actual state {}".format(compose_graph.__str__()))
        df = (
            part[1].astype(str)
        )
        G = nx.from_pandas_edgelist(df)

        compose_graph = nx.compose(compose_graph, G)
    logging.warning("[COMPOSE] G actual state {}".format(compose_graph.__str__()))
    logging.warning("[MUTUAL FOLLOW GRAPH] SAVING IN G")
    return compose_graph


def read_all_trends_names(path=TIMELINE_TWEETS_PATH):
    trends = []
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_trend = (
                maybe_hashtag.group()
                if maybe_hashtag is not None
                else line.strip().split()[0]
            )
            maybe_tweets = re.findall(TWEET_LOG_RE, line.strip())
            if len(maybe_tweets) > MINIMUN_TWEETS:
                trends.append(maybe_trend)
        file.close()

    return trends


def read_and_parse_timeline_tweets_path(path: Text):
    trends = []
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_tweets = re.findall(TWEET_LOG_RE, line.strip())
            if len(maybe_tweets) > MINIMUN_TWEETS:
                trend = maybe_hashtag.group()
                tweets = list(
                    map(
                        lambda tweet_log: to_tweet(tweet_log, trend),
                        maybe_tweets,
                    )
                )
                trends.append(Trend(trend=trend, tweets=tweets))

        file.close()

    return trends


def read_users_by_trend(trend: Text, path=TIMELINE_TWEETS_PATH):
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_trend = (
                maybe_hashtag.group()
                if maybe_hashtag is not None
                else line.strip().split()[0]
            )

            if maybe_trend == trend:
                maybe_tweets = re.findall(TWEET_LOG_RE, line.strip())
                tweets = list(
                    map(
                        lambda tweet_log: to_tweet(tweet_log, trend),
                        maybe_tweets,
                    )
                )
                file.close()
                return Trend(trend=trend, tweets=tweets)


def get_first_neigh(users: List[Text], path=SPLIITED_MUTUAL_FOLLOWING):
    many_littel_df = []
    for part in SPLIITED_MUTUAL_FOLLOWING:
        is_valid_edge = np_any(part.isin(users), axis=1)
        many_littel_df.append(part[is_valid_edge])
    ignoring_header = pd.concat(many_littel_df)

    source = ignoring_header["source"].unique()
    target = ignoring_header["target"].unique()

    uniques_users = unique(concatenate([source, target]))
    return uniques_users


def get_many_user(users: List[Text]):
    warning("[calculating networks with ] \t n = {} ".format(len(users)))
    if len(users) < MAX_RECURSIVE_EXTENDED_GRAPH:
        users_and_neigh = get_first_neigh(users)
        users_to_add = list(set(users_and_neigh) - set(users))
        ## Validator:
        if (
            int(len(users_to_add) * 0.10) > 500
        ):  # This is in order to iterate many steps
            users_to_add = choice(users_to_add, 500)
            users_and_neigh = unique(concatenate([users, users_to_add]))
            return get_many_user(users_and_neigh)
        else:
            n = int(len(users_to_add) * 0.10)
            users_to_add = choice(users_to_add, n)
            users_and_neigh = unique(concatenate([users, users_to_add]))
            return get_many_user(users_and_neigh)
    else:
        return users


def get_edge_list_by_users(users, path=SPLIITED_MUTUAL_FOLLOWING) -> Text:
    many_littel_df = []
    for part in SPLIITED_MUTUAL_FOLLOWING:
        is_valid_edge = np_any(part.isin(users), axis=1)
        many_littel_df.append(part[is_valid_edge])

    ignoring_header = (
        pd.concat(many_littel_df).to_string(index=False).split("\n")[1:]
    )  # Ignoring column names

    striped_lines = list(map(lambda line: line.strip(), ignoring_header))
    result = "\n".join(striped_lines)

    return result


def read_tweets(trend: Text, path=TIMELINE_TWEETS_PATH):
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_trend = (
                maybe_hashtag.group()
                if maybe_hashtag is not None
                else line.strip().split()[0]
            )

            if maybe_trend == trend:
                maybe_tweets = re.findall(TWEET_LOG_RE, line.strip())
                tweets = list(
                    map(
                        lambda tweet_log: to_tweet(tweet_log, trend),
                        maybe_tweets,
                    )
                )
                file.close()
                return Trend(trend=trend, tweets=tweets)


def read_retweets(trend: Text, path=TIMELINE_RETWEETS_PATH):
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_trend = (
                maybe_hashtag.group()
                if maybe_hashtag is not None
                else line.strip().split()[0]
            )

            if maybe_trend == trend:
                maybe_retweets = re.findall(RETWEET_LOG_RE, line.strip())
                retweets = list(
                    map(
                        lambda tweet_log: to_retweet(tweet_log, trend),
                        maybe_retweets,
                    )
                )
                file.close()
                return Trend(trend=trend, retweets=retweets)

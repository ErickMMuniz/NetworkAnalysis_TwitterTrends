import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
from typing import Text, List
import networkx as nx
import re
from datetime import datetime
from pydantic import BaseModel
from tqdm import tqdm

MINIMUN_TWEETS = 4000

HASHTAG_RE: Text = "\w+(?=\s)"
TWEET_LOG_RE: Text = "\d+,\d+"

FOLLOWER_GCC: Text = "follower_gcc.anony.dat"
TIMELINE_TWEETS: Text = "timeline_tag.anony.dat"

DATA_PATH: Text = os.path.join(os.getcwd(), "data")
MUTUAL_FOLLOWERS_PATH: Text = os.path.join(DATA_PATH, FOLLOWER_GCC)
TIMELINE_TWEETS_PATH: Text = os.path.join(DATA_PATH, TIMELINE_TWEETS)


class Tweet(BaseModel):
    trend: Text
    user: Text
    created_at: datetime


class Trend(BaseModel):
    trend: Text
    tweets: List[Tweet]


def to_tweet(tweet_log_text: Text, trend: Text) -> Tweet:
    """
    Parse text like
            TIMESTAMP_UNIX_EPCH,USER
    :param tweet_log_text:
    :param trend:
    :return: Tweet
    """
    timestamp, user = tweet_log_text.split(",")
    created_at = datetime.fromtimestamp(float(timestamp))
    user = str(user)

    return Tweet(trend=trend, user=user, created_at=created_at)


# Reading files


def read_and_parse_mutual_followers_dat(path: Text, limit_lines=100) -> nx.Graph:
    USER_RE = "\d+"
    with open(path) as file:
        for i, line in enumerate(file):
            assert i < limit_lines
            maybe_users = re.findall(USER_RE, line.strip())
            print(maybe_users)


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

def read_users_by_trend(trend:Text, path = TIMELINE_TWEETS_PATH):
    with open(path, encoding="utf8") as file:
        for i, line in enumerate(file):
            maybe_hashtag = re.search(HASHTAG_RE, line.strip())
            maybe_trend = maybe_hashtag.group() if maybe_hashtag is not None else line.strip().split()[0]

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

def get_edge_list_by_users(users, path = MUTUAL_FOLLOWERS_PATH) -> Text:
    USER_RE = "\d+"
    result = ""
    with open(path) as file:
        for line in tqdm(file):
            maybe_users = re.findall(USER_RE, line.strip())
            is_valid_edge = any(map(lambda user: user in users, maybe_users))
            if is_valid_edge:
                result += line.strip() + "\n"
        file.close()
    return result



if __name__ == "__main__":
    assert os.path.isdir(DATA_PATH)
    assert os.path.isfile(MUTUAL_FOLLOWERS_PATH)
    assert os.path.isfile(TIMELINE_TWEETS_PATH)

    TREND = "music"
    trend = read_users_by_trend(TREND)
    users = set(map(lambda tweet: tweet.user, trend.tweets)) #There user that tweet more than once
    edge_list = get_edge_list_by_users(users)
    print(edge_list)




    # read_and_parse_mutual_followers_dat(MUTUAL_FOLLOWERS_PATH)
    # trends = read_and_parse_timeline_tweets_path(TIMELINE_TWEETS_PATH)

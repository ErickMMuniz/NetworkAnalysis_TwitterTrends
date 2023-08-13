import re
import networkx as nx
from tqdm import tqdm
from numpy import any as np_any

from src.values import *
from src.objects import *


def read_and_parse_mutual_followers_dat(path: Text, limit_lines=100) -> nx.Graph:
    USER_RE = "\d+"
    with open(path) as file:
        for i, line in enumerate(file):
            assert i < limit_lines
            maybe_users = re.findall(USER_RE, line.strip())
            print(maybe_users)


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

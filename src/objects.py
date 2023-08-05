from pydantic import BaseModel
from typing import Text, List
from datetime import datetime, timedelta
import pandas as pd


class Tweet(BaseModel):
    trend: Text
    user: Text
    created_at: datetime

class ReTweet(BaseModel):
    trend: Text
    source_user: Text
    target_user: Text
    created_at: datetime

class Trend(BaseModel):
    trend: Text
    tweets: List[Tweet] = []
    retweets: List[ReTweet] = []


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


def to_retweet(retweet_log_text: Text, trend: Text) -> ReTweet:
    """
        Parse text like
                TIMESTAMP_UNIX_EPCH,USER
        :param tweet_log_text:
        :param trend:
        :return: Tweet
        """
    timestamp, source_user, target_user = retweet_log_text.split(",")
    created_at = datetime.fromtimestamp(float(timestamp))
    source = str(source_user)
    target = str(target_user)

    return ReTweet(trend=trend, source_user=source, target_user=target, created_at=created_at)


def split_by_time(tweets: List[Tweet], window="'1H'") -> List[List[Tweet]]:
    tweets = sorted(tweets, key=lambda t: t.created_at)

    first_tweet = tweets[0].created_at
    last_tweet = tweets[-1].created_at

    first_date = datetime(first_tweet.year, first_tweet.month, first_tweet.day, hour=first_tweet.hour)
    last_date = datetime(last_tweet.year, last_tweet.month, last_tweet.day, hour=last_tweet.hour) + timedelta(hours=1)

    range = pd.date_range(first_date, last_date, freq='1H')
    windows = zip(range[:-2], range[1:])

    nested_elements = []

    for window in windows:
        elements = []
        for tweet in tweets:
            lower_bound = window[0]
            upper_bound = window[1]
            is_in_window = lower_bound <= tweet.created_at <= upper_bound

            if is_in_window:
                elements.append(tweet)
        nested_elements.append(elements)

    return nested_elements

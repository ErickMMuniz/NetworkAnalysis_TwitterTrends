from pydantic import BaseModel
from typing import Text, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from src.values import WINDOW_STUDY

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


def split_by_time(trend: Trend, window_freq="1H"):

    tweets = sorted(trend.tweets, key=lambda t: t.created_at)
    retweets = sorted(trend.retweets, key=lambda t: t.created_at)

    first_tweet = tweets[0].created_at
    last_tweet = tweets[-1].created_at

    first_retweet = retweets[0].created_at
    last_retweet = retweets[-1].created_at

    first_event = sorted([first_tweet, first_retweet])[0]
    last_event = sorted([last_tweet, last_retweet])[-1]

    first_date = datetime(first_event.year, first_event.month, first_event.day, hour=first_event.hour)
    last_date = datetime(last_event.year, last_event.month, last_event.day, hour=last_event.hour) + timedelta(hours=1)

    range = pd.date_range(first_date, last_date, freq=window_freq)
    windows : zip[Tuple[datetime]] = zip(range[:-2], range[1:])

    nested_elements = {}

    for window in windows:
        inner_tweets = []
        inner_retweets = []
        lower_bound = window[0]
        upper_bound = window[1]
        key = str(lower_bound)
        nested_elements[key] = {}

        for tweet in tweets:
            is_in_window = lower_bound <= tweet.created_at <= upper_bound

            if is_in_window:
                inner_tweets.append(tweet)

        for retweet in retweets:
            is_in_window = lower_bound <= retweet.created_at <= upper_bound

            if is_in_window:
                inner_retweets.append(retweet)

        nested_elements[key]["tweets"] = inner_tweets
        nested_elements[key]["retweets"] = inner_retweets

    # Only works for WINDOWS_STUDY neighbor +- burst hour
    times = sorted(list(zip(nested_elements.keys(), nested_elements.values())), key= lambda x: datetime.fromisoformat(x[0]))
    burst_ancla = max(times, key= lambda x: len(x[1]["tweets"]))


    n = len(times)
    index_ancla = times.index(burst_ancla)

    time_min_index = max([0, index_ancla - WINDOW_STUDY])
    time_max_index = min([n,index_ancla + WINDOW_STUDY])

    return dict(times[time_min_index:time_max_index+1])

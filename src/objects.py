from pydantic import BaseModel
from typing import Text, List
from datetime import datetime


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

import os
from typing import Dict, Union

from src.db import read_trend_dump
from src.objects import *
from src.values import *
from src.util import parse_date_time
from logging import warning

# Create a datetime object from the string
from src.plot import plt


def make_time_series_tweets(TREND: Text, windos_study=None) -> None:
    warning("[BEGIN] PLOTTING TREND \t => {}".format(TREND))
    df = read_trend_dump(TREND)
    t = df["dump_trend"].apply(Trend.parse_raw).iloc[0]

    # Split by time 2 days before and after peak.
    # Check windows_study of thw following function
    splited_time: Dict[str, Dict[str, List[Union[Tweet, ReTweet]]]] = split_by_time(
        t, windows_study=windos_study
    )

    x = map(parse_date_time, splited_time.keys())
    # activity_dict = Dict[str, list[Tweet | ReTweet]
    y = map(lambda activity_dict: len(activity_dict["tweets"]), splited_time.values())
    y = list(y)
    path_fig = os.path.join(TIME_SERIES_COMPLETE, "{}.pdf".format(TREND))
    fig, ax = plt.subplots()
    ax.plot(range(len(y)), y)
    ax.set_ylabel("Cantidad de tweets por hora")
    ax.set_xlabel("Número de horas desde el primer tweet")
    # ax.set_title("Línea de tiempo de {}".format(TREND))
    fig.savefig(path_fig)
    warning("[END] PLOTTING TREND \t => {}".format(TREND))

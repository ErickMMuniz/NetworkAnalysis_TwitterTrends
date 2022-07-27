import pprint

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Index

from burstkit.util.read_files import (
    get_dataframe_trend_to_id,
    get_timeline_tweets_by_trend,
    get_dict_trend_burst,
)

plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.size"] = 15
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.usetex"] = False
plt.style.use("bmh")

COLOR_BURST: dict[str, str] = {1: "purple", 0: "orange"}


def generate_windows_time_timeline_count(
    timeline: pd.DataFrame, size_window: str = "60min"
) -> pd.DataFrame:
    """
    Generate a dataframe with the windows of the timeline
    :param timeline: pd.DataFrame
    :param window_size: int
    :return: pd.DataFrame
    """
    assert timeline.columns.to_list() == [
        "timestamp",
        "uid",
    ], "The columns of the timeline are not correct"
    updated_timeline: pd.DataFrame = timeline.copy()
    updated_timeline["count"] = 1
    updated_timeline.set_index("timestamp", inplace=True)
    assert (
        timeline.shape[0] == updated_timeline.shape[0]
    ), "The number of rows of the timeline is not correct"
    timeline_count_by_windows: pd.DataFrame = updated_timeline.resample(
        size_window
    ).sum()
    assert timeline_count_by_windows.columns.to_list() == [
        "count"
    ], "The columns of the timeline are not correct"

    return timeline_count_by_windows


def centrered_timeline_count_in_maximun_activiy(
    timeline_count_by_windows: pd.DataFrame, delta: int = 10
) -> pd.DataFrame:
    assert timeline_count_by_windows.columns.to_list() == [
        "count"
    ], "The columns of the timeline are not correct"
    timeline_count_by_windows_centered: pd.DataFrame = timeline_count_by_windows.copy()
    index_max: int = timeline_count_by_windows_centered["count"].idxmax()

    index: Index = timeline_count_by_windows_centered.index
    n = len(index.to_list())
    id_index_max = index.to_list().index(index_max)
    lim_inf: int = max(0, id_index_max - delta)
    lim_sup: int = min(n, id_index_max + delta) - 1

    lim_inf_index = index[lim_inf]
    lim_sup_index = index[lim_sup]
    spplited_timeline = timeline_count_by_windows_centered.loc[
        lim_inf_index:lim_sup_index
    ]
    assert spplited_timeline.columns.to_list() == [
        "count"
    ], "The columns of the timeline are not correct"
    return spplited_timeline


def main() -> None:
    trends_by_burst: dict[str, str] = get_dict_trend_burst()
    for trend in trends_by_burst:
        TREND: str = trend
        b = trends_by_burst[TREND]
        timeline: pd.DataFrame = get_timeline_tweets_by_trend(TREND)

        timeline_count: pd.DataFrame = generate_windows_time_timeline_count(timeline)
        timeline_count_centered_in_maximun_activity: pd.DataFrame = (
            centrered_timeline_count_in_maximun_activiy(timeline_count)
        )

        fig, ax = plt.subplots()
        ax.plot(
            timeline_count_centered_in_maximun_activity["count"], color=COLOR_BURST[b]
        )
        ax.set_xlabel("Time")
        ax.set_xticklabels(
            list(
                map(
                    lambda x: str(x).split(" ")[1][0:5],
                    timeline_count_centered_in_maximun_activity.index,
                )
            ),
            rotation=45,
            size=12,
        )
        ax.set_ylabel("Number of tweets")
        ax.set_title(f"Timeline of {TREND}")
        plt.show()

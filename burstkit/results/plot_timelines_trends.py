import pprint

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Index
from tqdm import tqdm
from networkx import Graph
import logging

from burstkit.results.comparative_timeline_attribute import (
    read_graph_attribute_from_gefx,
    read_graph_attribute_from_gml,
)
from burstkit.util.read_files import (
    get_dataframe_trend_to_id,
    get_timeline_tweets_by_trend,
    get_dict_trend_burst,
    get_list_trend_gml_graphs,
    read_gml_red_by_trend,
)

plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.size"] = 15
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.usetex"] = False
plt.style.use("bmh")

COLOR_BURST: dict[str, str] = {1: "#67568c", 0: "#fbdd74"}

LEGEND_ATTRIBUTE: dict[str, str] = {"core": "Core", "idcom": "Comunidades"}


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


def generate_windows_attribute_timeline_count(
    timeline: pd.DataFrame, size_window: str = "60min", attribute: str = "core"
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
        attribute,
    ], "The columns of the timeline are not correct"
    updated_timeline: pd.DataFrame = timeline.copy()
    updated_timeline.set_index("timestamp", inplace=True)
    assert (
        timeline.shape[0] == updated_timeline.shape[0]
    ), "The number of rows of the timeline is not correct"
    timeline_count_by_windows: pd.DataFrame = updated_timeline.resample(
        size_window
    ).mean()
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


# Some specific trends to plot


def generate_plot_timeline_count_and_core_attribute(
    trends_by_burst: dict[str, str]
) -> None:
    for trend in tqdm(trends_by_burst):
        TREND: str = trend
        try:
            ATTRIBUTE: str = "core"
            WINDOW_DELTA: str = "60min"
            b = trends_by_burst[TREND]
            timeline: pd.DataFrame = get_timeline_tweets_by_trend(TREND)

            timeline_count: pd.DataFrame = generate_windows_time_timeline_count(
                timeline, size_window=WINDOW_DELTA
            )
            timeline_count_centered_in_maximun_activity: pd.DataFrame = (
                centrered_timeline_count_in_maximun_activiy(timeline_count)
            )
            user_attribute: pd.DataFrame = read_graph_attribute_from_gefx(
                trend=TREND, attribute=ATTRIBUTE
            )
            timeline_mapped_attribute: pd.DataFrame = timeline.copy()

            dict_to_replace = dict(
                zip(user_attribute["uid"], user_attribute[ATTRIBUTE])
            )

            timeline_mapped_attribute[ATTRIBUTE] = timeline_mapped_attribute["uid"].map(
                dict_to_replace
            )

            number_of_null_values = (
                timeline_mapped_attribute[ATTRIBUTE].isnull().sum()
                / timeline_mapped_attribute.shape[0]
            )
            logging.warning(
                f"Number of null values in {ATTRIBUTE} is {number_of_null_values}"
            )
            logging.warning("[engine] Input null values with the mean of the attribute")
            timeline_mapped_attribute[ATTRIBUTE].fillna(
                timeline_mapped_attribute[ATTRIBUTE].mean(), inplace=True
            )
            assert (
                timeline_mapped_attribute[ATTRIBUTE].isnull().sum() == 0
            ), "There are null values in the attribute"

            timeline_mapped_attribute.set_index("timestamp", inplace=True)
            timeline_mapped_attribute = timeline_mapped_attribute.resample(
                WINDOW_DELTA
            ).mean()

            X: Index = timeline_count_centered_in_maximun_activity.index

            Y_count = timeline_count_centered_in_maximun_activity["count"]
            id_max = Y_count.idxmax()
            Y_attribute = timeline_mapped_attribute[
                timeline_mapped_attribute.index.isin(X)
            ]

            # Codes for the plot
            logging.warning("Generating timelines")
            fig, ax = plt.subplots()
            ax.plot(Y_count, color=COLOR_BURST[b])
            ax.patch.set_facecolor("#FFFFFF")

            ax.vlines(id_max, 0, Y_count.max(), colors=COLOR_BURST[b], alpha=0.2)

            ax2 = ax.twinx()
            ax2.plot(Y_attribute[ATTRIBUTE], color="#ff6e6c", alpha=0.8, linestyle="--")

            ax2.set_ylabel("Valor de núcleo promedio")

            ax.set_xlabel("Tiempo")
            ax.set_xticklabels(
                list(
                    map(
                        lambda x: str(x).split(" ")[1][0:5],
                        X,
                    )
                ),
                rotation=45,
                size=12,
            )
            ax.set_ylabel("Cantidad de Tweets")
            ax.set_title(f"#{TREND}")

            ax.grid(True)
            # TODO: EN CUÁNTAS COMUNIDADES DE MANERA SIMULTÁNEA SE ENCUENTRA EL TREND EN EL MOMENTO DE LA MAYOR ACTIVADAD.
            plt.savefig(f"data\\images\\timeline_tweets\\TREND_{TREND}_B_{b}.png")
            # plt.show()
            input("qwer")
        except Exception as e:
            logging.error(f"Error in {TREND}")
            logging.error(e)
            continue


def generate_plot_len_unique_comminities_by_burst(
    trends_by_burst: dict[str, str]
) -> None:
    trends_with_community_and_gml_extension: list[str] = get_list_trend_gml_graphs()
    for trend in tqdm(trends_by_burst):
        try:
            TREND: str = trend
            TREND_GML: str = f"{TREND}.gml"
            ATTRIBUTE = "idcom"
            WINDOW_DELTA: str = "60min"
            b = trends_by_burst[TREND]
            is_possible_to_plot: bool = (
                TREND_GML in trends_with_community_and_gml_extension
            )

            assert is_possible_to_plot, f"{TREND} is not possible to plot"

            timeline: pd.DataFrame = get_timeline_tweets_by_trend(TREND)

            timeline_count: pd.DataFrame = generate_windows_time_timeline_count(
                timeline, size_window=WINDOW_DELTA
            )
            timeline_count_centered_in_maximun_activity: pd.DataFrame = (
                centrered_timeline_count_in_maximun_activiy(timeline_count)
            )
            logging.warning(f"[engine] {TREND} Reading graph attribute")
            user_attribute: pd.DataFrame = read_graph_attribute_from_gml(
                TREND, ATTRIBUTE
            )
            logging.warning("[engine] FINISH Reading graph attribute")

            timeline_mapped_attribute: pd.DataFrame = timeline.copy()

            dict_to_replace = dict(
                zip(user_attribute["uid"], user_attribute[ATTRIBUTE])
            )

            timeline_mapped_attribute[ATTRIBUTE] = timeline_mapped_attribute["uid"].map(
                dict_to_replace
            )

            number_of_null_values = (
                timeline_mapped_attribute[ATTRIBUTE].isnull().sum()
                / timeline_mapped_attribute.shape[0]
            )
            logging.warning(
                f"Number of null values in {ATTRIBUTE} is {number_of_null_values}"
            )
            logging.warning("[engine] Input null values with the mean of the attribute")
            timeline_mapped_attribute[ATTRIBUTE].fillna(method="pad", inplace=True)
            assert (
                timeline_mapped_attribute[ATTRIBUTE].isnull().sum() == 0
            ), "There are null values in the attribute"

            timeline_mapped_attribute.set_index("timestamp", inplace=True)
            timeline_mapped_attribute = timeline_mapped_attribute.resample(
                WINDOW_DELTA
            ).apply(lambda x: x.nunique())

            X: Index = timeline_count_centered_in_maximun_activity.index

            Y_count = timeline_count_centered_in_maximun_activity["count"]
            Y_attribute = timeline_mapped_attribute[
                timeline_mapped_attribute.index.isin(X)
            ]

            id_max = Y_count.idxmax()

            # Codes for the plot
            logging.warning("Generating timelines")
            fig, ax = plt.subplots()
            ax.patch.set_facecolor("#FFFFFF")
            ax.plot(Y_count, color=COLOR_BURST[b])

            ax.vlines(id_max, 0, Y_count.max(), colors=COLOR_BURST[b], alpha=0.2)

            ax2 = ax.twinx()
            ax2.plot(Y_attribute[ATTRIBUTE], color="#ff6e6c", alpha=0.8, linestyle="--")

            ax2.set_ylabel("Número de comunidades")

            ax.set_xlabel("Tiempo")
            ax.set_xticklabels(
                list(
                    map(
                        lambda x: str(x).split(" ")[1][0:5],
                        X,
                    )
                ),
                rotation=45,
                size=12,
            )
            ax.set_ylabel("Cantidad de Tweets")
            ax.set_title(f"#{TREND}")

            ax.grid(True)

            # plt.show()
            plt.savefig(
                f"data\\images\\timeline_tweets_count_com\\TREND_{TREND}_B_{b}.png"
            )
        except Exception as e:
            logging.error(f"Error in {TREND}")
            logging.error(e)
            continue


def comparative_core_comunities_by_burst(trends_by_burst: dict[str, str]) -> None:
    fig, ax = plt.subplots()
    ax.set_title("test")
    ax.set_xlabel("Core")
    ax.set_ylabel("Comunidad")

    for trend in tqdm(trends_by_burst.keys()):
        TREND: str = trend
        try:
            ATTRIBUTE_CORE: str = "core"
            ATTRIBUTE_IDCOM: str = "idcom"
            WINDOW_DELTA: str = "60min"
            b = trends_by_burst[TREND]
            timeline: pd.DataFrame = get_timeline_tweets_by_trend(TREND)

            timeline_count: pd.DataFrame = generate_windows_time_timeline_count(
                timeline, size_window=WINDOW_DELTA
            )
            timeline_count_centered_in_maximun_activity: pd.DataFrame = (
                centrered_timeline_count_in_maximun_activiy(timeline_count)
            )

            #
            timeline_mapped_attribute: pd.DataFrame = timeline.copy()
            user_core: pd.DataFrame = read_graph_attribute_from_gefx(
                trend=TREND, attribute=ATTRIBUTE_CORE
            )
            user_idcom: pd.DataFrame = read_graph_attribute_from_gml(
                trend=TREND, attribute=ATTRIBUTE_IDCOM
            )
            dict_to_replace_core = dict(
                zip(user_core["uid"], user_core[ATTRIBUTE_CORE])
            )

            dict_to_replace_idcom = dict(
                zip(user_idcom["uid"], user_idcom[ATTRIBUTE_IDCOM])
            )

            timeline_mapped_attribute[ATTRIBUTE_CORE] = timeline_mapped_attribute[
                "uid"
            ].map(dict_to_replace_core)

            timeline_mapped_attribute[ATTRIBUTE_IDCOM] = timeline_mapped_attribute[
                "uid"
            ].map(dict_to_replace_idcom)

            number_of_null_values = timeline_mapped_attribute.isnull().sum().sum()
            logging.warning(f"Number of null values is {number_of_null_values}")
            logging.warning("Input null values with the mean of the attribute")
            timeline_mapped_attribute[ATTRIBUTE_CORE].fillna(
                timeline_mapped_attribute[ATTRIBUTE_CORE].mean(), inplace=True
            )
            timeline_mapped_attribute[ATTRIBUTE_IDCOM].fillna(
                method="pad", inplace=True
            )

            assert (
                timeline_mapped_attribute.isnull().sum().sum() == 0
            ), "There are null values in the attribute"
            timeline_mapped_attribute.set_index("timestamp", inplace=True)

            timeline_mapped_attribute_mean = timeline_mapped_attribute.resample(
                WINDOW_DELTA
            ).mean()

            timeline_mapped_attribute_unique = timeline_mapped_attribute.resample(
                WINDOW_DELTA
            ).apply(lambda x: x.nunique())

            Y = timeline_count_centered_in_maximun_activity.copy()["count"]

            # FIXME this is a bug in the code
            idmax: Index = Y.idxmax()

            Y_attribute_mean = timeline_mapped_attribute_mean[
                timeline_mapped_attribute_mean.index.isin([idmax])
            ]
            Y_attribute_unique = timeline_mapped_attribute_unique[
                timeline_mapped_attribute_unique.index.isin([idmax])
            ]

            pprint.pprint(Y_attribute_mean[ATTRIBUTE_CORE])
            pprint.pprint(Y_attribute_unique[ATTRIBUTE_IDCOM])

            ax.scatter(
                Y_attribute_mean[ATTRIBUTE_CORE],
                Y_attribute_unique[ATTRIBUTE_IDCOM],
                color=COLOR_BURST[b]
            )

        except Exception as e:
            logging.error(f"Error in {TREND}")
            logging.error(e)

    fig.savefig(f"data\\images\\comparative_core_comunities_by_burst.png")
    input("Press any key to continue...")


def main() -> None:
    trends_by_burst: dict[str, str] = get_dict_trend_burst()

    # generate_plot_timeline_count_and_core_attribute(trends_by_burst)

    # generate_plot_len_unique_comminities_by_burst(trends_by_burst)

    comparative_core_comunities_by_burst(trends_by_burst)

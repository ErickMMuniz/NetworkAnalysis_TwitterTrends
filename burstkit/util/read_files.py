import pprint

import numpy as np

import pandas as pd
import os
from builtins import open
from networkx import Graph, DiGraph
from networkx import write_gexf, read_gml
from networkit.nxadapter import nx2nk
from burstkit.util.User import User
from tqdm import tqdm
from logging import warning

DATA_PATH = os.path.join("data", "virality2013.tar")

# qwe
DATA_PATH_DRIVE_FROM_COLAB = os.path.join("content", "drive")

PATH_MUTUAL_FOLLOWER_DAT = os.path.join(DATA_PATH, "follower_gcc.anony.dat")
PATH_WEIGHT_MENTION_DAT = os.path.join(DATA_PATH, "mention_gcc.anony.dat")
PATH_WEIGHT_RETWEET_DAT = os.path.join(DATA_PATH, "retweet_gcc.anony.dat")

PATH_TIMELINE_TWEETS = os.path.join(DATA_PATH, "timeline_tag.anony.dat")
PATH_TIMELINE_RETWEETS = os.path.join(DATA_PATH, "timeline_tag_rt.anony.dat")
PATH_TIMELINE_MENTIONS = os.path.join(DATA_PATH, "timeline_tag_men.anony.dat")

PATH_COLAB_MUTUAL_FOLLOW_NETWORK_FROM_DRIVE = (
    "/content/drive/MyDrive/tesis/data/mutual_followers_network_with_attributes.gml"
)

PATH_DATA_NETWORKS_BY_TREND = os.path.join("data", "networks_by_trend")
PATH_FINAL_DF = os.path.join("data", "finaldf.csv")
PATH_INDEX_TREND = os.path.join(PATH_DATA_NETWORKS_BY_TREND, "index_trends.csv")

PATH_GRAPHS_FIRST_CASE = os.path.join("data/data_new_vecindad/", "data_new_vecindad")
PATH_GRAPHS_GML_WITH_COMMUNITIES = os.path.join(
    "data/data_new_vecindad_community", "data_cm_network"
)

FOLDER_TREND_ID = "TREND_ID_{}"
UID = "uid"
SOURCE = "source"
TARGET = "target"
TIMESTAMP = "timestamp"


def get_path_folder_trend(trend: "str") -> "os.path":
    idmap = pd.read_csv(PATH_INDEX_TREND).to_dict("list")
    idmap = dict(zip(idmap["trend"], idmap["id_trend"]))
    # assert idmap in list(idmap.keys()), "Trend not found"
    id = idmap[trend]
    return os.path.join(PATH_DATA_NETWORKS_BY_TREND, FOLDER_TREND_ID.format(id))


def is_path_file_in_data_path(path_file: "str") -> "bool":
    return path_file.find(DATA_PATH) != -1


def read_file_space_separated(
    path_file: "str", limit_rows: "int" = None, is_edge_list: "bool" = False
) -> "pd.DataFrame":
    # assert is_path_file_in_data_path(
    #     path_file
    # ), f"All the file must be allocated on {DATA_PATH}."
    data = pd.read_csv(
        path_file,
        sep=" ",
        nrows=limit_rows,
        names=[SOURCE, TARGET] if is_edge_list else None,
        dtype={SOURCE: np.str, TARGET: np.str} if is_edge_list else None,
    )
    if is_edge_list:
        assert (
            data[SOURCE].dtypes == "object"
        ), "[ERROR][DFDataTypes] There are some users with uid like string"
        assert (
            data[TARGET].dtypes == "object"
        ), "[ERROR][DFDataTypes] There are some users with uid like string"
    return data


def parse_string_to_trend_and_timestamp_and_uid(
    detailed_string: "str",
) -> "(str, list[str])":
    spliited_string = detailed_string.split()
    return spliited_string[0], spliited_string[1:]


def parse_string_to_trend_and_timestamp_and_uid_edge(
    detailed_string: "str",
) -> "(str, list[str])":
    spliited_string = detailed_string.split()
    return spliited_string[0], spliited_string[1:]


def single_split_string_to_timestamp_uid(
    timestamp_user: "str",
) -> "tuple[Timestamp,np.str]":
    split_by_comma: "list[str]" = timestamp_user.split(",")
    timestamp = pd.to_datetime(split_by_comma[0], unit="s")
    uid = np.str(split_by_comma[1])
    assert isinstance(uid, str) or isinstance(
        uid, np.str
    ), "[ERROR][DFDataTypes] There are some users with uid like string"
    return timestamp, uid


def split_timestamp_user(timestamp_uid: "list[str]") -> "list[tuple[Timestamp,np.str]]":
    return list(map(single_split_string_to_timestamp_uid, timestamp_uid))


def transform_tuple_trend_and_timestamp_uid(
    trend_ts_uid: "tuple[str, list[str]]",
) -> "tuple[str, list[tuple[Timestamp,np.str]]]":
    trend_name = trend_ts_uid[0]
    timeline_users: "list[str]" = trend_ts_uid[1]
    transformed_timeline = split_timestamp_user(timeline_users)
    return trend_name, transformed_timeline


def read_file_each_line_different_length(
    path_file: "str", limit_rows: "int" = None, min_number_tweets: "int" = 0
) -> "dict[str, list[tuple[Timestamp, str]]]":
    file = dict(
        map(
            transform_tuple_trend_and_timestamp_uid,
            tqdm(
                filter(
                    lambda trend_list_uid_ts: len(trend_list_uid_ts[1])
                    >= min_number_tweets,
                    tqdm(
                        list(
                            map(
                                parse_string_to_trend_and_timestamp_and_uid,
                                tqdm(
                                    open(path_file, "r", encoding="utf8").readlines(
                                        limit_rows
                                    )
                                ),
                            )
                        )
                    ),
                ),
            ),
        )
    )
    return file


def single_split_string_to_timestamp_uid_fromuid(
    timestamp_user: "str",
) -> "tuple[Timestamp,np.str,np.str]":
    split_by_comma: "list[str]" = timestamp_user.split(",")
    timestamp = pd.to_datetime(split_by_comma[0], unit="s")
    uid_target = np.str(split_by_comma[1])
    uid_source = np.str(split_by_comma[2])

    assert isinstance(uid_source, str) or isinstance(
        uid_source, np.str
    ), "[ERROR][DFDataTypes] There are some users with uid like string"
    assert isinstance(uid_target, str) or isinstance(
        uid_target, np.str
    ), "[ERROR][DFDataTypes] There are some users with uid like string"

    return timestamp, uid_source, uid_target


def single_split_string_to_timestamp_fromuid_uid(
    timestamp_user: "str",
) -> "tuple[Timestamp,np.str,np.str]":
    split_by_comma: "list[str]" = timestamp_user.split(",")
    timestamp = pd.to_datetime(split_by_comma[0], unit="s")
    uid_source = np.str(split_by_comma[1])
    uid_target = np.str(split_by_comma[2])

    assert isinstance(uid_source, str) or isinstance(
        uid_source, np.str
    ), "[ERROR][DFDataTypes] There are some users with uid like string"
    assert isinstance(uid_target, str) or isinstance(
        uid_target, np.str
    ), "[ERROR][DFDataTypes] There are some users with uid like string"

    return timestamp, uid_source, uid_target


def split_timestamp_user_edge(
    timestamp_uid: "list[str]",
) -> "list[tuple[Timestamp,np.str, np.str]]":
    return list(map(single_split_string_to_timestamp_uid_fromuid, timestamp_uid))


def split_timestamp_user_edge_mentions(
    timestamp_uid: "list[str]",
) -> "list[tuple[Timestamp,np.str, np.str]]":
    return list(map(single_split_string_to_timestamp_fromuid_uid, timestamp_uid))


def transform_tuple_trend_and_timestamp_egde_uid(
    trend_ts_uid: "tuple[str, list[str]]",
) -> "tuple[str, list[tuple[Timestamp,np.str, np.str]]]":
    """
    For convention
                        Source     Target
    (uid, from_uid) -> (from_uid -> uid)
    """
    trend_name = trend_ts_uid[0]
    timeline_users: "list[str]" = trend_ts_uid[1]
    transformed_timeline = split_timestamp_user_edge(timeline_users)
    return trend_name, transformed_timeline


def transform_tuple_trend_and_timestamp_egde_uid_mentions(
    trend_ts_uid: "tuple[str, list[str]]",
) -> "tuple[str, list[tuple[Timestamp,np.str, np.str]]]":
    """
    For convention
                        Source     Target
    (from_uid, uid) -> (from_uid -> uid)
    """
    trend_name = trend_ts_uid[0]
    timeline_users: "list[str]" = trend_ts_uid[1]
    transformed_timeline = split_timestamp_user_edge_mentions(timeline_users)
    return trend_name, transformed_timeline


def read_file_each_line_different_length_and_double_user(
    path_file: "str", limit_rows: "int" = None
) -> "dict[str, list[tuple[Timestamp, str , str ]]]":
    file = dict(
        map(
            transform_tuple_trend_and_timestamp_egde_uid,
            list(
                map(
                    parse_string_to_trend_and_timestamp_and_uid_edge,
                    open(path_file, "r", encoding="utf8").readlines(limit_rows),
                )
            ),
        )
    )
    return file


def read_file_each_line_different_length_and_double_user_mention(
    path_file: "str", limit_rows: "int" = None
) -> "dict[str, list[tuple[Timestamp, str , str ]]]":
    """
    Disclaimer: This is the same function, but inverse the order of nodes.


    """
    file = dict(
        map(
            transform_tuple_trend_and_timestamp_egde_uid_mentions,
            list(
                map(
                    parse_string_to_trend_and_timestamp_and_uid_edge,
                    open(path_file, "r", encoding="utf8").readlines(limit_rows),
                )
            ),
        )
    )
    return file


def get_mutual_followers(limit_rows=None) -> "pd.DataFrame":
    return read_file_space_separated(
        PATH_MUTUAL_FOLLOWER_DAT,
        limit_rows=limit_rows if limit_rows is not None else None,
        is_edge_list=True,
    )


def get_timeline_tweets(limit_rows=None, min_number_tweets=0):
    return read_file_each_line_different_length(
        PATH_TIMELINE_TWEETS,
        limit_rows=limit_rows if limit_rows is not None else None,
        min_number_tweets=min_number_tweets,
    )


def get_timeline_retweets(limit_rows=None):
    return read_file_each_line_different_length_and_double_user(
        PATH_TIMELINE_RETWEETS,
        limit_rows=limit_rows if limit_rows is not None else None,
    )


def get_timeline_mentions(limit_rows=None):
    return read_file_each_line_different_length_and_double_user_mention(
        PATH_TIMELINE_MENTIONS,
        limit_rows=limit_rows if limit_rows is not None else None,
    )


def get_relation_trend_timeline_tweets(
    limit_rows=None, min_number_tweets=0
) -> "dict[str,pd.DataFrame]":
    trend_timeline: "dict[str, list[tuple[Timestamp, str]]]" = get_timeline_tweets(
        limit_rows=limit_rows, min_number_tweets=min_number_tweets
    )
    trends = trend_timeline.keys()
    timeline = map(
        lambda tl: pd.DataFrame(data=tl, columns=[TIMESTAMP, UID]),
        trend_timeline.values(),
    )
    return dict(zip(trends, timeline))


def get_relation_trend_timeline_retweets(limit_rows=None) -> "dict[str,pd.DataFrame]":
    trend_timeline: "dict[str, list[tuple[Timestamp, str, str]]]" = (
        get_timeline_retweets(limit_rows=limit_rows)
    )
    trends = trend_timeline.keys()
    timeline = map(
        lambda tl_stamp: pd.DataFrame(
            data=tl_stamp, columns=[TIMESTAMP, SOURCE, TARGET]
        ),
        trend_timeline.values(),
    )
    return dict(zip(trends, timeline))


def get_relation_trend_timeline_mentions(limit_rows=None) -> "dict[str,pd.DataFrame]":
    trend_timeline: "dict[str, list[tuple[Timestamp, str, str]]]" = (
        get_timeline_mentions(limit_rows=limit_rows)
    )
    trends = trend_timeline.keys()
    timeline = map(
        lambda tl_stamp: pd.DataFrame(
            data=tl_stamp, columns=[TIMESTAMP, SOURCE, TARGET]
        ),
        trend_timeline.values(),
    )
    return dict(zip(trends, timeline))


def write_network_to_file(G: "Graph | DiGrpah", path_with_file_type: "str") -> None:
    write_gexf(G=G, path=path_with_file_type)


def get_timeline_tweets_by_trend(trend: "str") -> "pd.DataFrame":
    """
    Get the timeline of a trend.

    """
    idmap = pd.read_csv(PATH_INDEX_TREND).to_dict("list")
    idmap = dict(zip(idmap["trend"], idmap["id_trend"]))
    # assert idmap in list(idmap.keys()), "Trend not found"
    id = idmap[trend]

    path_folder = os.path.join(PATH_DATA_NETWORKS_BY_TREND, FOLDER_TREND_ID.format(id))
    timeline = pd.read_csv(os.path.join(path_folder, "tweets_timeline.csv"))
    timeline["timestamp"] = pd.to_datetime(timeline["timestamp"])
    timeline["uid"] = timeline["uid"].astype(str)
    return timeline


def get_attribute_uidpart_dataframe_by_trend(
    id_trend: "str", attribute: "str"
) -> "pd.DataFrame":
    """
    Get the timeline of a trend.

    """
    path_folder = os.path.join(
        PATH_DATA_NETWORKS_BY_TREND, FOLDER_TREND_ID.format(id_trend)
    )
    assert attribute in [
        "betweenness",
        "closeness",
        "degree",
        "eigenvector",
        "pagerank",
        "core_decomposition",
    ], "Attribute not found"
    attribute_data_frame = pd.read_csv(
        os.path.join(path_folder, "attributes", attribute + ".csv")
    )
    attribute_data_frame["uid_part"] = attribute_data_frame["uid_part"].astype(str)
    return attribute_data_frame


def get_id_trend_colab(trend: "str", from_colab=False) -> "os.path":
    if from_colab:
        idmap = pd.read_csv("/content/data/index_trends.csv").to_dict("list")
    else:
        idmap = pd.read_csv(PATH_INDEX_TREND).to_dict("list")
    idmap = dict(zip(idmap["trend"], idmap["id_trend"]))
    # assert idmap in list(idmap.keys()), "Trend not found"
    id_trend = idmap[trend]
    return id_trend


def get_uid_list_from_networkx(G: "Graph | DiGrpah") -> "list[str]":
    return list(G.nodes())


def get_nk_graph_from_file(trend: "str", from_colab=False) -> "Graph":
    id = get_id_trend_colab(trend, from_colab=from_colab)
    warning("[DEBUG] Writing trend: {} with id -> {}".format(trend, id))
    if from_colab:
        path_root_folders = os.path.abspath(
            "/content/drive/MyDrive/tesis/data/networks_by_trend"
        )
    else:
        path_root_folders = PATH_DATA_NETWORKS_BY_TREND
    path_network = os.path.join(
        path_root_folders, f"TREND_ID_{id}", "network_neighbour.gml"
    )
    g_nx = read_gml(path_network)
    g_nk = nx2nk(g_nx)
    return g_nk


def get_nx_graph_from_file(id_trend: "int", from_colab=False) -> "Graph":
    if from_colab:
        path_root_folders = os.path.abspath(
            "/content/drive/MyDrive/tesis/data/networks_by_trend"
        )
    else:
        path_root_folders = PATH_DATA_NETWORKS_BY_TREND
    path_network = os.path.join(
        path_root_folders, f"TREND_ID_{id_trend}", "network_neighbour.gml"
    )
    g_nx = read_gml(path_network)
    return g_nx


def write_attributes_by_trend(
    trend: "str", attribute_name: "str", scores: "pd.DataFrame", from_colab=False
) -> None:
    id = get_id_trend_colab(trend, from_colab=from_colab)
    warning("[DEBUG] Writing trend: {} with id -> {}".format(trend, id))
    if from_colab:
        path_root_folders = os.path.abspath(
            "/content/drive/MyDrive/tesis/data/networks_by_trend"
        )
    else:
        path_root_folders = PATH_DATA_NETWORKS_BY_TREND
    path_folder_trend = os.path.join(path_root_folders, f"TREND_ID_{id}")
    path_folder_attributes = os.path.join(path_folder_trend, "attributes")
    try:
        os.mkdir(path_folder_attributes)
    except FileExistsError:
        pass

    path_dataframe = os.path.join(path_folder_attributes, f"{attribute_name}.csv")

    scores.to_csv(path_dataframe, index=False)
    warning("[DEBUG] Wrote attribute: {}".format(attribute_name))


def get_dataframe_trend_to_id(from_colab=False) -> "dict[str, str]":
    if from_colab:
        idmap = pd.read_csv("/content/data/index_trends.csv").to_dict("list")
    else:
        idmap = pd.read_csv(PATH_INDEX_TREND).to_dict("list")
    idmap = dict(zip(idmap["trend"], idmap["id_trend"]))
    return idmap


def get_dict_trend_burst(from_colab=False) -> "dict[str, str]":
    if from_colab:
        idmap = pd.read_csv("/content/data/finaldf.csv").to_dict("list")
    else:
        idmap = pd.read_csv(PATH_FINAL_DF).to_dict("list")
    idmap = dict(zip(idmap["trend"], idmap["burst"]))
    return idmap


def get_list_trend_first_case_graphs(from_colab=False) -> "list[str]":
    if from_colab:
        # FIXME: This is a hack to get the list of trends
        path = PATH_GRAPHS_FIRST_CASE
    else:
        path = PATH_GRAPHS_FIRST_CASE
    raw_dir = os.listdir(path)
    is_all_files_gexf: bool = all(map(lambda x: x.split(".")[-1] == "gexf", raw_dir))
    assert is_all_files_gexf, "Not all files are gexf"
    return raw_dir


def get_list_trend_gml_graphs(from_colab=False) -> list[str]:
    if from_colab:
        path = PATH_GRAPHS_GML_WITH_COMMUNITIES
    else:
        path = PATH_GRAPHS_GML_WITH_COMMUNITIES
    raw_dir = os.listdir(path)
    filtered_dir_gml_extension = list(
        filter(lambda x: x.split(".")[-1] == "gml", raw_dir)
    )
    return filtered_dir_gml_extension


def read_gml_red_by_trend(trend_with_gml_extension: str, from_colab=False) -> "Graph":
    assert trend_with_gml_extension.split(".")[-1] == "gml", "Trend is not gml"
    if from_colab:
        path = PATH_GRAPHS_GML_WITH_COMMUNITIES
    else:
        path = PATH_GRAPHS_GML_WITH_COMMUNITIES
    path_gml = os.path.join(path, trend_with_gml_extension)
    assert os.path.exists(path_gml), "File not found"
    g_nx = read_gml(path_gml)
    return g_nx


if __name__ == "__main__":
    pass

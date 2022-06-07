import numpy as np

import pandas as pd
import os
from builtins import open

DATA_PATH = os.path.join("data", "virality2013.tar")

PATH_MUTUAL_FOLLOWER_DAT = os.path.join(DATA_PATH, "follower_gcc.anony.dat")
PATH_WEIGHT_MENTION_DAT = os.path.join(DATA_PATH, "mention_gcc.anony.dat")
PATH_WEIGHT_RETWEET_DAT = os.path.join(DATA_PATH, "retweet_gcc.anony.dat")

PATH_TIMELINE_TWEETS = os.path.join(DATA_PATH, "timeline_tag.anony.dat")
PATH_TIMELINE_RETWEETS = os.path.join(DATA_PATH, "timeline_tag_rt.anony.dat")
PATH_TIMELINE_MENTIONS = os.path.join(DATA_PATH, "timeline_tag_men.anony.dat")


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
        names=["source", "target"] if is_edge_list else None,
        dtype= {"source": np.int16, "target": np.int16} if is_edge_list else None
    )
    return data


def parse_string_to_trend_and_timestamp_and_uid(
    detailed_string: "str",
) -> "(str, list[str])":
    #TODO: INCORPORATE INT AND TIME STAMP VALUES
    spliited_string = detailed_string.split()
    return spliited_string[0], spliited_string[1:]


def read_file_each_line_different_length(path_file: "str", limit_rows: "int" = None):
    file = dict(
        map(
            parse_string_to_trend_and_timestamp_and_uid,
            open(path_file, "r", encoding="utf8").readlines(limit_rows),
        )
    )
    return file


def get_mutual_followers() -> "pd.DataFrame":
    return read_file_space_separated(PATH_MUTUAL_FOLLOWER_DAT)


def get_timeline_tweets():
    return read_file_each_line_different_length(PATH_TIMELINE_TWEETS)


def get_timeline_retweets():
    return read_file_each_line_different_length(PATH_TIMELINE_RETWEETS)


def get_timeline_mentions():
    return read_file_each_line_different_length(PATH_TIMELINE_MENTIONS)


if __name__ == "__main__":
    print(PATH_MUTUAL_FOLLOWER_DAT)
    read_file_space_separated(
        PATH_MUTUAL_FOLLOWER_DAT, is_edge_list=True, limit_rows=10
    )

import pandas as pd
import os

DATA_PATH = "data/"


def is_path_file_in_data_path(path_file: "str") -> "bool":
    return path_file.find(DATA_PATH) != -1


def read_file_space_separated(
    path_file: "str", limit_rows: "int" = None, is_edge_list: "bool" = False
) -> "pd.DataFrame":
    assert is_path_file_in_data_path(
        path_file
    ), f"All the file must be allocated on {DATA_PATH}."
    data = pd.read_csv(
        path_file,
        sep=" ",
        nrows=limit_rows,
        names=["source", "target"] if is_edge_list else None,
    )
    return data


if __name__ == "__main__":
    read_file_space_separated()

from pandas import DataFrame


def generate_pair_until_last_from_array(array: "list[A]") -> "list[(A,A)]":
    return [(array[i], array[i + 1]) for i in range(len(array) - 1)]


if __name__ == "__main__":
    pass

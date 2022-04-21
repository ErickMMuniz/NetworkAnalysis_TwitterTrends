import pandas as pd
import matplotlib as plt
import numpy as np
import burstkit.util.read_files as rf

from pprint import pprint

pprint(rf.is_path_file_in_data_path("data/another.csv"))
pprint(rf.read_file_space_separated("data/another.csv", is_edge_list= True))


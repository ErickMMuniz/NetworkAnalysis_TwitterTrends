import pandas as pd
import matplotlib as plt
import numpy as np
import burstkit.util.read_files as rf
from burstkit.util.User import User

from pprint import pprint

# pprint(rf.is_path_file_in_data_path("data/another.csv"))
# pprint(rf.read_file_space_separated("data/another.csv", is_edge_list= True))
# print(rf.read_file_space_separated(rf.PATH_MUTUAL_FOLLOWER_DAT))

#
#print(rf.get_mutual_followers(10).dtypes)
#print(type(np.int16("1")))
#foo: "Timestamp" = pd.to_datetime("1332769782", unit="s")
uno = User(123)
dos = User(np.int16(16))
print(123)
print(uno)

print(isinstance(uno.uid,np.int16))
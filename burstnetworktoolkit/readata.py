"""
@ErickMM98
A package module to read and manipulate the .dat files.
"""

import tarfile
import pandas as pd
import numpy as np
import networkx as nx

# import networkit as nk
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import collections
import itertools
import random
import seaborn as sn
import threading
import os
import logging
import pytz
from datetime import datetime


plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.size"] = 15
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.usetex"] = False

# mpl.rcParams['axes.prop_cycle'] = cycler(color=['r', 'g', 'b', 'y'])
# print(plt.style.available)
plt.style.use("bmh")
# plt.style.use('classic')

# plt.rcParams.keys()
B = pd.read_csv("/content/drive/MyDrive/FC_Materias/FC_Proyecto_1/finaldf.csv")
dfBeforeBurst = pd.read_csv(
    "/content/drive/MyDrive/NetworkAnalysis_TwitterTrends/data_before_burst.csv"
)
dfBeforeBurst = dfBeforeBurst.dropna()
# b = B[ B['trend'] == trend]['burst'].to_list()[0]

# @title Some variables and extract the data.
# GENERAL VALUES (secret values to public)

main_seed = 123456789
np.random.seed(main_seed)

path_main_drive = (
    "/content/drive/My Drive/NetworkAnalysis_TwitterTrends/virality2013.tar.gz"
)
path_friends_followers = "/content/follower_gcc.anony.dat"
path_tweets_users = "/content/timeline_tag.anony.dat"
path_retweets_users = "/content/timeline_tag_rt.anony.dat"
path_mentions_users = "/content/timeline_tag_men.anony.dat"

# FINALS_DATAFRAME
path_final_dataframe = "/content/drive/MyDrive/FC_Materias/FC_Proyecto_1/finaldf.csv"


def extract_file_from_drive(fooStr="string"):
    """
    Function to extract all the data files.
    Just for the first time.
    """
    my_tar = tarfile.open(fooStr)
    my_tar.extractall("//content")
    my_tar.close()


def get_data_followers_and_friends():
    """
    Function to get a dataframe for the file with
    the basic relation of mutual follow.

    return @Dataframe
    """
    data = pd.read_csv(
        path_friends_followers,
        sep=" ",
        # nrows = 10000000,
        names=["source", "target"],
    )
    return data


def get_data_tweets_time():
    """
    Function to get a dataframe for the file with
    the basic relation of mutual follow.

    return @Dataframe
    """
    data = pd.read_csv(path_tweets_users, sep=" ", nrows=100)
    # names=['source', 'target'])
    return data


def get_data_retweets_time():
    """
    Function to get a dataframe for the file with
    the basic relation of mutual follow.

    return @Dataframe
    """
    pass


def get_data_mentions_time():
    """
    Function to get a dataframe for the file with
    the basic relation of mutual follow.

    return @Dataframe
    """
    pass


def givehour(timestamp):
    day_string = timestamp.hour
    return day_string


def giveday(timestamp):
    day_string = timestamp.dayofyear
    return day_string


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
------------------------ Plot beauty networks ---------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def plot_social_network():
    """
    Function to plot fancy social network
    """


"""
FUNCIONES PARA LEER LA INFORMACIÓN
"""
K_number_tweets = 4000
# K_number_tweets = 0
"""
OBTENER LA INFOR COMO DICCIONARIOS.
"""


def get_dic_tweets():
    """
    TWEETS
    Función para leer la info en un diccionario
    """
    name_all_hastag = {}
    with open(path_tweets_users, "r") as reader:
        for line in reader:
            list_tweets = line.split()
            namehashatag = list_tweets.pop(0)
            count_tw = len(list_tweets)
            if count_tw > K_number_tweets:
                name_all_hastag[namehashatag] = list_tweets
    return name_all_hastag


def get_dic_retweets():
    """
    RETWEETS
    Función para leer la info en un diccionario
    """
    name_all_hastag = {}
    with open(path_retweets_users, "r") as reader:
        for line in reader:
            list_tweets = line.split()
            namehashatag = list_tweets.pop(0)
            name_all_hastag[namehashatag] = list_tweets
    return name_all_hastag


def get_dic_mentions():
    """
    MENCIONES
    Función para leer la info en un diccionario
    """
    name_all_hastag = {}
    with open(path_mentions_users, "r") as reader:
        for line in reader:
            list_tweets = line.split()
            namehashatag = list_tweets.pop(0)
            name_all_hastag[namehashatag] = list_tweets
    return name_all_hastag

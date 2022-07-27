"""
@author: Erick
"""
from burstkit.util import SEED

import numpy as np

from burstkit.util.read_files import (
    get_dataframe_trend_to_id,
    get_timeline_tweets_by_trend,
)

np.random.seed(SEED)

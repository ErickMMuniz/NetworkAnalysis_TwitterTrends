import numpy as np
from builtins import isinstance


class User(object):
    def __init__(self, uid: "int"):
        assert isinstance(uid, np.int16) or isinstance(
            uid, int
        ), "[WARNING] The value {uid} is not a int."
        self.uid = uid

    def __eq__(self, other: "User"):
        return self.uid == other.uid

    def __str__(self):
        return f"(uid:{self.uid})"

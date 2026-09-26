from typing import NamedTuple

# PURPOSE:
#   -StoredUser provides an abstraction for raw user data
#   -defines a clean name accessable shape of user related data
class StoredUser(NamedTuple):
    id : int
    username : str
    password : str
    balance : float
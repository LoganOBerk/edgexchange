from typing import NamedTuple

class StoredUser(NamedTuple):
    id : int
    username : str
    password : str
    balance : float

class StoredPortfolio(NamedTuple):
    id : int
    u_id : int
    name : str

class StoredStock(NamedTuple):
    id : int
    p_id : int
    ticker : str
    quantity : int

class StoredAccountData(NamedTuple):
    user : StoredUser
    portfolios : list[StoredPortfolio]
    stocks : list[StoredStock]
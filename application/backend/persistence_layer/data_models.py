from typing import NamedTuple
from collections import defaultdict


# PURPOSE:
#   -StoredUser provides an abstraction for raw user data
#   -defines a clean name accessable shape of user related data
class StoredUser(NamedTuple):
    id : int
    username : str
    password : str
    balance : float


# PURPOSE:
#   -StoredPortfolio provides an abstraction for raw portfolio data
#   -defines a clean name accessable shape of portfolio related data
class StoredPortfolio(NamedTuple):
    id : int
    u_id : int
    name : str


# PURPOSE:
#   -StoredStock provides an abstraction for raw stock data
#   -defines a clean name accessable shape of stock related data
class StoredStock(NamedTuple):
    id : int
    p_id : int
    ticker : str
    quantity : int


# PURPOSE:
#   -StoredAccount provides an abstraction for raw account data
#   -defines a clean name accessable shape of account related data
class StoredAccount(NamedTuple):
    user : StoredUser
    portfolios : list[StoredPortfolio]
    stocks : dict[int, StoredStock]


# PURPOSE:
#   -StoredAccountData provides an abstraction for StoredAccount formatting
#   -initializes StoredAccountData as a StoredAccount with grouped stocks for easy access
class StoredAccountData(StoredAccount):
    @staticmethod
    def group(holdings):
        stocks = defaultdict(list)
        for stock in holdings:
            stocks[stock.p_id].append(stock)

        return stocks
    
    def __new__(cls, user, portfolios, holdings):    
        return super().__new__(cls, user = user, portfolios = portfolios, stocks = cls.group(holdings))

    
        
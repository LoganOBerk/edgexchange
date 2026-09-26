from typing import NamedTuple
from collections import defaultdict

from .storeduser import StoredUser
from .storedportfolio import StoredPortfolio
from .storedstock import StoredStock

# PURPOSE:
#   -Stub provides an abstraction for the field declaration
#   -exists so StoredAggregate can keep NamedTuple's behavior with custom construction
class Stub(NamedTuple):
    user : StoredUser
    portfolios : list[StoredPortfolio]
    stocks : dict[int, list[StoredStock]]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if cls.__annotations__ != Stub.__annotations__:
            raise TypeError(
                f"{cls.__name__} fields have drifted from Stub: "
                f"{Stub.__annotations__} != {cls.__annotations__}"
            )


# PURPOSE:
#   -StoredAggregate provides an abstraction for the raw aggregate of all user data
#   -initializes StoredAggregate as an StoredAggregate with grouped stocks for easy access
class StoredAggregate(Stub):
    user : StoredUser
    portfolios : list[StoredPortfolio]
    stocks : dict[int, list[StoredStock]]

    @staticmethod
    def group(holdings):
        stocks = defaultdict(list)
        for stock in holdings:
            stocks[stock.p_id].append(stock)
        return stocks

    def __new__(cls, user, portfolios, holdings):
        return super().__new__(cls, user = user, portfolios = portfolios, stocks = cls.group(holdings))

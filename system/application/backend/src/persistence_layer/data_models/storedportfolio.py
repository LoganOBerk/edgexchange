from typing import NamedTuple

# PURPOSE:
#   -StoredPortfolio provides an abstraction for raw portfolio data
#   -defines a clean name accessable shape of portfolio related data
class StoredPortfolio(NamedTuple):
    id : int
    u_id : int
    name : str
from typing import NamedTuple

# PURPOSE:
#   -StoredStock provides an abstraction for raw stock data
#   -defines a clean name accessable shape of stock related data
class StoredStock(NamedTuple):
    id : int
    p_id : int
    ticker : str
    quantity : int

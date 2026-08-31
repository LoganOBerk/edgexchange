import time
import threading

from threading import Lock, Condition
from collections import defaultdict
from datetime import date


from common.errors import FetchingError, LiveCacheError
from common.constants import PRICE_REFRESH_INTERVAL, selfexp
from common.entropy import inject_volatility
from .externalapi import ExternalApi as eapi



cache = defaultdict(lambda : {"price" : None, "quote" : None, "quote_date" : None, "last_accessed" : None})
persistent_cache = defaultdict(lambda : {"sector" : None, "float" : None})

cache_lock = Condition(Lock())

# INPUT:
#    -ticker(str); ticker symbol to update
# OUTPUT: None
# PRECONDITION: None
# POSTCONDITION:
#    -cache; quote["price"] updated to price for ticker if quote exists
# RAISES: None
def sync_price(ticker : str) -> None:
    if read(ticker, "quote") is not None:
        cache[ticker]["quote"]["price"] = read(ticker, "price")


# INPUT:
#    -ticker(str); ticker symbol to update
#    -quote(dict); quote data to write
# OUTPUT: None
# PRECONDITION:
#    -ticker; must exist in cache
# POSTCONDITION:
#    -cache; quote and quote_date updated for ticker while keeping quote in sync
# RAISES: None
def write_quote(ticker : str, quote : dict) -> None:
    cache[ticker]["quote"] = quote
    cache[ticker]["quote_date"] = date.today()
    sync_price(ticker)
    


# INPUT:
#    -ticker(str); ticker symbol to update
#    -price(float); price to write
# OUTPUT: None
# PRECONDITION:
#    -ticker; must exist in cache
# POSTCONDITION:
#    -cache; price, and last_accessed updated for ticker while keeping quote in sync
# RAISES: None
def write_price(ticker : str, price : float) -> None:
    price += inject_volatility(price)
    cache[ticker]["price"] = price
    sync_price(ticker)


# INPUT:
#    -ticker(str); ticker symbol to look up
#    -value(str); field name to retrieve
# OUTPUT:
#    -result(any); value at cache[key][value], or None if key or field not found
# PRECONDITION: None
# POSTCONDITION: None
# RAISES: None
def read(ticker : str, value : str) -> any:
    return cache.get(ticker, {}).get(value)


# INPUT:
#    -ticker(str); ticker symbol to stamp
# OUTPUT: None
# PRECONDITION:
#    -ticker; must exist in cache
# POSTCONDITION:
#    -cache; last_accessed updated to current time for ticker
# RAISES: None
def stamp(ticker : str) -> None:
    cache[ticker]["last_accessed"] = time.time()

    
# INPUT:
#    -tickers(list[str]); ticker symbols to register in cache
# OUTPUT: None
# PRECONDITION: None
# POSTCONDITION:
#    -cache; all tickers in keys exist with default values, check stamp POSTCONDITION
# RAISES: None
def touch(tickers : list[str]) -> None:
    for ticker in tickers:
        _ = cache[ticker]
        stamp(ticker)


# INPUT:
#    -ticker(str); ticker symbol to remove
# OUTPUT: None
# PRECONDITION:
#    -ticker; must exist in cache
# POSTCONDITION:
#    -cache; ticker and all associated data removed
# RAISES: None
def rm(ticker : str) -> None:
    del cache[ticker]


# INPUT:
#    -ticker(str); ticker symbol to abort
# OUTPUT: None
# PRECONDITION:
#    -ticker; if not None and has no quote, must already exist in cache (e.g. via touch())
# POSTCONDITION:
#    -cache; if ticker exists with quote still unset, its entry is removed; otherwise no-op
# RAISES: None
def abort(ticker : str) -> None:
    if ticker and read(ticker, "quote") is None:
        rm(ticker)


# INPUT: None
# OUTPUT: None
# PRECONDITION: None
# POSTCONDITION:
#    -cache; quotes refreshed daily, tickers accessed within selfexp(PRICE_REFRESH_INTERVAL) are refreshed
#    -cache_lock; all waiters are notified on cache changes, a failed quote may cause a request to wait another run cycle or serve a slightly stale value for a cycle
# RAISES: None
def run():
    while True:
        latency = 0
        start = time.time()
        
        active_stocks = set()
        stale_quotes = set()

        with cache_lock:
            for ticker in cache.keys():
                active = read(ticker, "price") is None or read(ticker, "last_accessed") >= start - selfexp(PRICE_REFRESH_INTERVAL)
                quote_stale = read(ticker, "quote") is None or read(ticker, "quote_date") < date.today()

                if active:
                    active_stocks.add(ticker)

                if active and quote_stale:
                    stale_quotes.add(ticker)


        fetched_info = {}
        def fetch_info():
            nonlocal fetched_info
            try:

                fetched_info = eapi.get_stock_info(stale_quotes)

            except FetchingError as e:
                with cache_lock:
                    abort(e.ticker)
                    cache_lock.notify_all()

        t1 = threading.Thread(target = fetch_info)
        t1.start()


        fetched_prices = {}
        def fetch_prices():
            nonlocal fetched_prices
            fetched_prices = eapi.get_stock_prices(active_stocks)

        t2 = threading.Thread(target = fetch_prices)
        t2.start()

        t1.join()
        t2.join()


        with cache_lock:
            for ticker, quote in fetched_info.items():
                write_quote(ticker, quote)
                
            for ticker, price in fetched_prices.items():
                write_price(ticker, price)
                    
            cache_lock.notify_all()
            
        
        end = time.time()
        latency = end - start
        
        time.sleep(max(0, PRICE_REFRESH_INTERVAL - latency))

threading.Thread(target = run, daemon = True).start()



# PURPOSE:
#   -LiveCache provides a cache access abstraction
#   -allows system to store and re-access fresh stocks to reduce api calls 
class LiveCache:

    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.get_stock_price()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.get_stock_price()
    @staticmethod
    def get_stock_price(ticker : str) -> float:
        
        with cache_lock:
            touch([ticker])
            cache_lock.wait_for(lambda : read(ticker, "price") is not None)
            price = read(ticker, "price")

        return price


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.does_ticker_exist()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.does_ticker_exist()
    @staticmethod
    def does_ticker_exist(ticker : str) -> bool:
        exist = True

        try:

            if ticker not in cache:
                exist = eapi.does_ticker_exist(ticker)

        except FetchingError as e:
            raise LiveCacheError("Ticker search failed") from e

        return exist


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.get_float()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.get_float()
    @staticmethod
    def get_float(ticker : str) -> int:
        try:

            if persistent_cache[ticker]["float"] is None:
                persistent_cache[ticker]["float"] = eapi.get_float(ticker)

            max_shares = persistent_cache[ticker]["float"]

        except FetchingError as e:
            raise LiveCacheError("Float shares search failed") from e

        return max_shares


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.get_sector()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.get_sector()
    @staticmethod
    def get_sector(ticker : str) -> str:
        try:

            if persistent_cache[ticker]["sector"] is None:
                persistent_cache[ticker]["sector"] = eapi.get_sector(ticker)

            sector = persistent_cache[ticker]["sector"]

        except FetchingError as e:
            raise LiveCacheError("Failed to fetch stock sector") from e

        return sector


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.get_stock_info()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.get_stock_info()
    @staticmethod
    def get_stock_info(ticker : str) -> dict[str, dict]:
        with cache_lock:
            touch([ticker])
            cache_lock.wait_for(lambda: read(ticker, "quote") is not None)
            stock_info = read(ticker, "quote")

        return stock_info


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in ExternalApi.get_stock_prices()
    # RAISES: 
    #   -LiveCacheError; propagated from ExternalApi.get_stock_prices()
    @staticmethod
    def get_stock_prices(tickers : list[str]) -> dict[str, float]:
        
        ticker_package = {}

        with cache_lock:
            touch(tickers)
            for ticker in tickers:
                cache_lock.wait_for(lambda: read(ticker, "price") is not None)
                ticker_package[ticker] = read(ticker, "price")

        return ticker_package